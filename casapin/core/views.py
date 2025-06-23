from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Restaurante, Playa, Actividad, ImagenGaleria, LugarInteres, Movimiento, Reserva, Tarifa
from datetime import date, timedelta
from calendar import month_name
from collections import OrderedDict
from django.utils.text import slugify
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
import json

def home(request):
    return render(request, 'core/home.html')

def historia(request):
    return render(request, 'core/historia.html')

def galeria(request):
    categoria = request.GET.get('categoria')
    imagenes = ImagenGaleria.objects.all().order_by('-fecha_subida')
    if categoria:
        imagenes = imagenes.filter(categoria=categoria)
    return render(request, 'core/galeria.html', {
        'imagenes': imagenes,
        'categoria_actual': categoria
    })

def entorno(request):
    categoria = request.GET.get("categoria")
    lugares = LugarInteres.objects.all()
    if categoria:
        lugares = lugares.filter(categoria=categoria)

    categorias_disponibles = LugarInteres.objects.values_list('categoria', flat=True).distinct()

    # Extraer Casa Pin para centrar el mapa
    casa_pin = LugarInteres.objects.filter(nombre__iexact="Casa Pin").first()


    for lugar in lugares:
        lugar.es_casa_pin = lugar.nombre.lower() == "casa pin"

    return render(request, "core/entorno.html", {
        "lugares": lugares,
        "casa_pin": casa_pin,
        "categoria_activa": categoria,
        "categorias": categorias_disponibles,
    })

def reservas(request):
    return render(request, 'core/reservas.html')

def contacto(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        email = request.POST["email"]
        mensaje = request.POST["mensaje"]

        send_mail(
            f"Mensaje de {nombre}",
            mensaje,
            email,
            ["tu-email@ejemplo.com"],
            fail_silently=False,
        )

    return render(request, 'core/contacto.html')

def lista_restaurantes(request):
    restaurantes = Restaurante.objects.all()
    return render(request, 'core/restaurantes.html', {'restaurantes': restaurantes})

def lista_playas(request):
    playas = Playa.objects.all()
    return render(request, 'core/playas.html', {'playas': playas})

def lista_actividades(request):
    actividades = Actividad.objects.all()
    return render(request, 'core/actividades.html', {'actividades': actividades})


@staff_member_required
def dashboard_financiero(request):
    hoy = date.today()
    año_actual = hoy.year

    movimientos = Movimiento.objects.filter(fecha__year=año_actual)

    ingresos = movimientos.filter(tipo='ingreso').aggregate(total=Sum('importe'))['total'] or 0
    gastos = movimientos.filter(tipo='gasto').aggregate(total=Sum('importe'))['total'] or 0
    balance = ingresos - gastos

    meses = OrderedDict((month_name[i], 0) for i in range(1, 13))

    for mov in movimientos:
        nombre_mes = month_name[mov.fecha.month]
        if mov.tipo == 'ingreso':
            meses[nombre_mes] += mov.importe
        else:
            meses[nombre_mes] -= mov.importe

    contexto = {
        'ingresos': ingresos,
        'gastos': gastos,
        'balance': balance,
        'meses': {
            'keys': list(meses.keys()),
            'values': list(meses.values())
        },
        'año': año_actual,
    }

    return render(request, 'core/dashboard.html', contexto)


def eventos_reservas(request):
    reservas = Reserva.objects.all()
    eventos = []

    for r in reservas:
        eventos.append({
            "title": r.nombre,
            "start": r.fecha_inicio.isoformat(),
            "end": r.fecha_fin.isoformat(),
            "color": color_por_estado(r.estado)
        })

    return JsonResponse(eventos, safe=False)


def color_por_estado(estado):
    colores = {
        'reservado': '#f44336',  # rojo
        'disponible': '#4caf50',  # verde
        'mantenimiento': '#ff9800',  # naranja
    }
    return colores.get(estado, '#9e9e9e')


def disponibilidad(request):
    return render(request, 'core/disponibilidad.html')
def api_reservas(request):
    eventos = []
    for r in Reserva.objects.all():
        eventos.append({
            "title": f"Reservado",
            "start": r.fecha_inicio.isoformat(),
            "end": r.fecha_fin.isoformat(),
            "color": "#f44336"
        })
    return JsonResponse(eventos, safe=False)

@csrf_exempt
def calcular_precio(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return JsonResponse({'error': 'Fechas no válidas'}, status=400)

        fecha1 = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha2 = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        total = 0
        dias = []

        while fecha1 < fecha2:
            tarifa = Tarifa.objects.filter(fecha=fecha1).first()
            precio = tarifa.precio if tarifa else 120  # tarifa base
            total += precio
            dias.append({"fecha": str(fecha1), "precio": precio})
            fecha1 += timedelta(days=1)

        return JsonResponse({'total': total, 'detalle': dias})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def api_enviar_solicitud(request):
    if request.method == 'POST':
        datos = json.loads(request.body)

        # Guardar la reserva en la base de datos
        reserva = Reserva.objects.create(
            nombre=datos.get("nombre"),
            email=datos.get("email"),
            telefono=datos.get("telefono"),
            mensaje=datos.get("mensaje"),
            fecha_inicio=datos.get("checkin"),
            fecha_fin=datos.get("checkout"),
            estado="pendiente"
        )

        # Renderizar plantilla HTML de email
        html_content = render_to_string("emails/solicitud_admin.html", {
            "nombre": reserva.nombre,
            "email": reserva.email,
            "telefono": reserva.telefono,
            "fecha_inicio": reserva.fecha_inicio,
            "fecha_fin": reserva.fecha_fin,
            "mensaje": reserva.mensaje,
            "precio_total": "⚠️ Agrega cálculo si quieres mostrarlo"
        })

        # Crear y enviar correo al administrador
        email = EmailMultiAlternatives(
            subject=f"📩 Nueva solicitud de {reserva.nombre}",
            body="",  # Cuerpo plano vacío
            from_email="aaronferrerbarbas@gmail.com",
            to=["aaronferrerbarbas@gmail.com"],
            bcc=["d.martinredondo@gmail.com"]
        )
        email.attach_alternative(html_content, "text/html")
        import os
        print("AUTENTICANDO COMO:", settings.EMAIL_HOST_USER)
        print("CONTRASEÑA:", settings.EMAIL_HOST_PASSWORD)

        email.send()

        # Render del correo para el cliente
        html_cliente = render_to_string("emails/solicitud_cliente.html", {
            "nombre": reserva.nombre,
            "fecha_inicio": reserva.fecha_inicio,
            "fecha_fin": reserva.fecha_fin,
        })

        # Correo de confirmación al cliente
        email_cliente = EmailMultiAlternatives(
            subject="🌿 Hemos recibido tu solicitud – Casa Pin",
            body="",
            from_email="aaronferrerbarbas@gmail.com",  # ✅ Este sí está autenticado
            to=[reserva.email],
        )

        email_cliente.attach_alternative(html_cliente, "text/html")
        email_cliente.send()

        return JsonResponse({'ok': True})

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def api_enviar_contacto(request):
    if request.method == "POST":
        try:
            datos = json.loads(request.body)

            nombre = datos.get("nombre", "").strip()
            email = datos.get("email", "").strip()
            mensaje = datos.get("mensaje", "").strip()

            if not nombre or not email or not mensaje:
                return JsonResponse({"error": "Todos los campos son obligatorios."}, status=400)

            # Envío de correo al admin
            html_admin = render_to_string("emails/contacto_admin.html", {
                "nombre": nombre,
                "email": email,
                "mensaje": mensaje,
            })

            email_admin = EmailMultiAlternatives(
                subject=f"📨 Nuevo mensaje de contacto: {nombre}",
                body="",
                from_email="aaronferrerbarbas@gmail.com",
                to=["aaronferrerbarbas@gmail.com"],
                bcc=["d.martinredondo@gmail.com"],
            )
            email_admin.attach_alternative(html_admin, "text/html")
            email_admin.send()

            # Correo al cliente
            html_cliente = render_to_string("emails/contacto_cliente.html", {
                "nombre": nombre,
            })

            email_cliente = EmailMultiAlternatives(
                subject="🌿 Hemos recibido tu mensaje – Casa Pin",
                body="",
                from_email="aaronferrerbarbas@gmail.com",
                to=[email],
            )
            email_cliente.attach_alternative(html_cliente, "text/html")
            email_cliente.send()

            return JsonResponse({"ok": True})

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": "Hubo un problema al procesar el mensaje."}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def solicitud_reserva(request):
    return render(request, "core/solicitud_reserva.html")

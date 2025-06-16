from django.db.models import Sum
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .models import Restaurante
from .models import Playa
from .models import Actividad
from .models import ImagenGaleria
from .models import LugarInteres
from .models import Movimiento
from datetime import date
from calendar import month_name
from collections import OrderedDict
from django.utils.text import slugify
from django.http import JsonResponse
from .models import Reserva

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

    # Crear balance mensual
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

@staff_member_required
def vista_calendario(request):
    return render(request, 'core/calendario.html')
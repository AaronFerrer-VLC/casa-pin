from django.shortcuts import render
from django.db.models import Q
from .models import Restaurante
from .models import Playa
from .models import Actividad
from .models import ImagenGaleria
from .models import LugarInteres

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
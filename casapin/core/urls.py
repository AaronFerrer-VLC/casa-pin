from django.urls import path
from . import views
from .views import solicitud_reserva, lista_restaurantes, lista_playas, lista_actividades, dashboard_financiero, eventos_reservas, disponibilidad, api_reservas, calcular_precio, api_enviar_solicitud, api_enviar_contacto

urlpatterns = [
    path('', views.home, name='home'),
    path('historia/', views.historia, name='historia'),
    path('galeria/', views.galeria, name='galeria'),
    path('entorno/', views.entorno, name='entorno'),
    path('reservas/', views.reservas, name='reservas'),
    path('contacto/', views.contacto, name='contacto'),
    path('restaurantes/', lista_restaurantes, name='lista_restaurantes'),
    path('playas/', lista_playas, name='lista_playas'),
    path('actividades/', lista_actividades, name='lista_actividades'),
    path('dashboard/', dashboard_financiero, name='dashboard'),
    path('calendario/reservas/', eventos_reservas, name='eventos_reservas'),
    path('disponibilidad/', disponibilidad, name='disponibilidad'),
    path('api/reservas/', api_reservas, name='api_reservas'),
    path('api/calcular-precio/', calcular_precio, name='calcular_precio'),
    path('api/solicitud/', api_enviar_solicitud, name='api_enviar_solicitud'),
    path('api/enviar-contacto/', views.api_enviar_contacto, name='api_enviar_contacto'),
    path('solicitud/', views.solicitud_reserva, name='solicitud_reserva'),

]

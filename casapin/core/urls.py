from django.urls import path
from . import views
from .views import lista_restaurantes, lista_playas, lista_actividades, dashboard_financiero, eventos_reservas, vista_calendario

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
    path('calendario/', vista_calendario, name='calendario'),

]

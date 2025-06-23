from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from import_export.admin import ExportMixin
from .models import Restaurante, Playa, Actividad, ImagenGaleria, LugarInteres, Reserva, Movimiento, DashboardFinanciero, Tarifa

# Modelos sin personalización
admin.site.register(Restaurante)
admin.site.register(Playa)
admin.site.register(Actividad)
admin.site.register(ImagenGaleria)
admin.site.register(LugarInteres)

# Modelo Reserva con admin personalizado
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('nombre', 'notas')
    ordering = ('-fecha_inicio',)

# Modelo Movimiento con exportación
@admin.register(Movimiento)
class MovimientoAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'concepto', 'categoria', 'importe')
    list_filter = ('tipo', 'categoria', 'fecha')
    search_fields = ('concepto',)
    date_hierarchy = 'fecha'

@admin.register(DashboardFinanciero)
class DashboardFinancieroAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('dashboard'))  # redirige al dashboard real

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'precio', 'motivo')
    list_filter = ('fecha',)
    ordering = ('fecha',)

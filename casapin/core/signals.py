from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Restaurante, Playa, Actividad, LugarInteres

def sync_lugar(sender, instance, **kwargs):
    if not instance.latitud or not instance.longitud:
        return

    nombre = instance.nombre
    descripcion = getattr(instance, "descripcion", "")
    enlace = getattr(instance, "enlace", None)

    categoria_map = {
        Restaurante: "restaurante",
        Playa: "playa",
        Actividad: "actividad",
    }
    categoria = categoria_map.get(sender)

    LugarInteres.objects.update_or_create(
        nombre=nombre,
        categoria=categoria,
        defaults={
            "descripcion": descripcion,
            "latitud": instance.latitud,
            "longitud": instance.longitud,
            "enlace": enlace
        }
    )

def delete_lugar(sender, instance, **kwargs):
    categoria_map = {
        Restaurante: "restaurante",
        Playa: "playa",
        Actividad: "actividad",
    }
    categoria = categoria_map.get(sender)
    LugarInteres.objects.filter(nombre=instance.nombre, categoria=categoria).delete()

# Señales
@receiver(post_save, sender=Restaurante)
@receiver(post_save, sender=Playa)
@receiver(post_save, sender=Actividad)
def sync_lugar_post_save(sender, instance, **kwargs):
    sync_lugar(sender, instance, **kwargs)

@receiver(post_delete, sender=Restaurante)
@receiver(post_delete, sender=Playa)
@receiver(post_delete, sender=Actividad)
def delete_lugar_post_delete(sender, instance, **kwargs):
    delete_lugar(sender, instance, **kwargs)

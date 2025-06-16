from django.db import models

class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    valoracion = models.FloatField()
    enlace = models.URLField(blank=True, null=True)
    imagen = models.ImageField(upload_to='restaurantes/', blank=True, null=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Playa(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    descripcion = models.TextField()
    valoracion = models.FloatField(blank=True, null=True)
    imagen = models.ImageField(upload_to='playas/', blank=True, null=True)
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=[
        ("Naturaleza", "Naturaleza"),
        ("Cultura", "Cultura"),
        ("Aventura", "Aventura"),
    ])
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    ubicacion = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='actividades/', blank=True, null=True)
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

class ImagenGaleria(models.Model):
    CATEGORIAS = [
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
        ('naturaleza', 'Naturaleza'),
    ]

    titulo = models.CharField(max_length=100, blank=True)
    imagen = models.ImageField(upload_to='galeria/')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='interior')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo or f"{self.get_categoria_display()} ({self.id})"

class LugarInteres(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    categoria = models.CharField(max_length=50, choices=[
        ("naturaleza", "Naturaleza"),
        ("pueblo", "Pueblo"),
        ("playa", "Playa"),
        ("actividad", "Actividad"),
        ("casa", "Casa"),
        ("restaurante", "Restaurante"),
    ])
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre



class Reserva(models.Model):
        nombre = models.CharField(max_length=100)
        fecha_inicio = models.DateField()
        fecha_fin = models.DateField()
        ESTADO_CHOICES = [
            ('reservado', 'Reservado'),
            ('disponible', 'Disponible'),
            ('mantenimiento', 'Mantenimiento'),
        ]
        estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='reservado')
        notas = models.TextField(blank=True)

        def __str__(self):
            return f"{self.nombre} ({self.fecha_inicio} → {self.fecha_fin})"

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]

    fecha = models.DateField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    concepto = models.CharField(max_length=255)
    categoria = models.CharField(max_length=50, blank=True)
    importe = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.get_tipo_display()} – {self.concepto} ({self.fecha})"

    class Meta:
        ordering = ['-fecha']



class DashboardFinanciero(models.Model):
    class Meta:
        verbose_name = "📊 Dashboard financiero"
        verbose_name_plural = "📊 Dashboard financiero"
        managed = False  # Django no creará tabla en la base de datos

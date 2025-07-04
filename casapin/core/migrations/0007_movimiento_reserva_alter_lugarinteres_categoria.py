# Generated by Django 5.2.3 on 2025-06-16 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_actividad_latitud_actividad_longitud_playa_latitud_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(choices=[('ingreso', 'Ingreso'), ('gasto', 'Gasto')], max_length=10)),
                ('concepto', models.CharField(max_length=255)),
                ('categoria', models.CharField(blank=True, max_length=50)),
                ('importe', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('estado', models.CharField(choices=[('reservado', 'Reservado'), ('disponible', 'Disponible'), ('mantenimiento', 'Mantenimiento')], default='reservado', max_length=20)),
                ('notas', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='lugarinteres',
            name='categoria',
            field=models.CharField(choices=[('naturaleza', 'Naturaleza'), ('pueblo', 'Pueblo'), ('playa', 'Playa'), ('actividad', 'Actividad'), ('casa', 'Casa'), ('restaurante', 'Restaurante')], max_length=50),
        ),
    ]

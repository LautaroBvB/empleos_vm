# Generated by Django 5.1.6 on 2025-03-03 03:47

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import pagina.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='categorias/')),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='JornadaLaboral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='localidades/')),
            ],
        ),
        migrations.CreateModel(
            name='Modalidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Postulante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('dni', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'Solo números permitidos')])),
                ('caracteristica', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d+$', 'Solo números permitidos')])),
                ('numero', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d+$', 'Solo números permitidos')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contraseña', models.CharField(max_length=128)),
                ('archivo', models.FileField(upload_to=pagina.models.obtener_nombre_archivo, validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('dia', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('mes', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('año', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900)])),
                ('estado', models.CharField(choices=[('aprobado', 'Aprobado'), ('no_aprobado', 'No aprobado')], default='no_aprobado', max_length=15)),
                ('comentario', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Requisito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Rubro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Trabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('empresa', models.CharField(max_length=200)),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.TextField(blank=True, default='')),
                ('experiencia', models.BooleanField(default=False)),
                ('acerca_de', models.TextField()),
                ('direccion', models.CharField(max_length=255)),
                ('celular', models.CharField(max_length=15)),
                ('urgente', models.BooleanField(default=False)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='imagenes/trabajos_imagenes/')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.categoria')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.genero')),
                ('localidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.localidad')),
                ('modalidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.modalidad')),
                ('requisitos', models.ManyToManyField(to='pagina.requisito')),
                ('rubro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.rubro')),
                ('tipo_jornada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.jornadalaboral')),
            ],
        ),
    ]

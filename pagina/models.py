from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
import os

def obtener_nombre_archivo(instance, filename):
    # Se obtiene el número de DNI del postulante y lo usa como nombre de archivo
    nombre_archivo, extension = os.path.splitext(filename)
    return f"{instance.dni}{extension}"


class Rubro(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Postulante(models.Model):
    ESTADOS = [
        ('aprobado', 'Aprobado'),
        ('no_aprobado', 'No aprobado'),
    ]
    
    suscrito = models.BooleanField(default=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(
        max_length=15, unique=True, 
        validators=[RegexValidator(r'^\d+$', 'Solo números permitidos')]
    )
    caracteristica = models.CharField(
        max_length=10, 
        validators=[RegexValidator(r'^\d+$', 'Solo números permitidos')]
    )
    numero = models.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\d+$', 'Solo números permitidos')]
    )
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    archivo = models.FileField(upload_to=obtener_nombre_archivo, validators=[FileExtensionValidator(['pdf'])])
    dia = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    mes = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    año = models.PositiveIntegerField(validators=[MinValueValidator(1900)])

    estado = models.CharField(max_length=15, choices=ESTADOS, default='no_aprobado')  # Nuevo campo
    comentario = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.dni} ({self.estado})"




class Localidad(models.Model):
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='localidades/', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)

    def __str__(self):
        return self.nombre


class JornadaLaboral(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Modalidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Genero(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Requisito(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre


class Trabajo(models.Model):
    anonimo = models.BooleanField(default=False)
    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    tipo_jornada = models.ForeignKey(JornadaLaboral, on_delete=models.CASCADE)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    descripcion = models.TextField(blank=True, default="")
    experiencia = models.BooleanField(default=False)
    acerca_de = models.TextField()
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    celular = models.CharField(max_length=15)
    urgente = models.BooleanField(default=False)
    requisitos = models.ManyToManyField(Requisito)
    imagen = models.ImageField(upload_to='imagenes/trabajos_imagenes/', null=True, blank=True)
    fecha = models.DateField(default=timezone.now)
    destacado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.titulo} - {self.categoria}"

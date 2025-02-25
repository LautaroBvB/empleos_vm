from django.contrib import admin
from .models import Localidad, Requisito, Categoria, JornadaLaboral, Modalidad, Genero, Postulante, Rubro, Trabajo

# Registra los modelos en el admin
admin.site.register(Localidad)
admin.site.register(Categoria)
admin.site.register(JornadaLaboral)
admin.site.register(Modalidad)
admin.site.register(Genero)
admin.site.register(Postulante)
admin.site.register(Trabajo)
admin.site.register(Rubro)
admin.site.register(Requisito)
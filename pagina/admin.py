from django.contrib import admin
from .models import Localidad, Requisito, Categoria, JornadaLaboral, Modalidad, Genero, Postulante, Rubro, Trabajo

@admin.register(Postulante)
class PostulanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'email', 'estado', 'comentario')  # Campo 'email' agregado
    list_filter = ('estado',)
    actions = ['aprobar_postulantes', 'rechazar_postulantes']
    search_fields = ('nombre', 'apellido', 'dni')

    def aprobar_postulantes(self, request, queryset):
        queryset.update(estado='aprobado', comentario="Aprobado por el administrador")
    aprobar_postulantes.short_description = "Marcar como aprobado"

    def rechazar_postulantes(self, request, queryset):
        for postulante in queryset:
            if not postulante.comentario:
                postulante.comentario = "Rechazado sin comentario"
            postulante.estado = 'no aprobado'
            postulante.save()
    rechazar_postulantes.short_description = "Marcar como no aprobado"


# Registra los demás modelos
admin.site.register(Localidad)
admin.site.register(Categoria)
admin.site.register(JornadaLaboral)
admin.site.register(Modalidad)
admin.site.register(Genero)
admin.site.register(Trabajo)
admin.site.register(Rubro)
admin.site.register(Requisito)

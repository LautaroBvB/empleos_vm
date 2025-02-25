from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path('publicar/', views.publicar_trabajo, name='publicar_trabajo'),
    path('empleos/', views.listar_trabajos, name='listar_trabajos'),
    path('empleo/<int:trabajo_id>/', views.detalle_trabajo, name='detalle_trabajo'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/<int:categoria_id>/', views.detalle_categoria, name='detalle_categoria'),
    path('localidades/', views.listar_localidades, name='listar_localidades'),
    path('localidades/<int:localidad_id>/', views.detalle_localidad, name='detalle_localidad'),
    path('upload', views.upload_file, name='upload_file'),
    path('subir_cv', views.subir_cv, name='subir_cv'),
    path('formulario_exitoso/', views.formulario_exitoso, name='formulario_exitoso'),
    path('crear_trabajo/', views.crear_trabajo, name='crear_trabajo'),
]

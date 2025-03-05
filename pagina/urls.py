from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name='inicio'),
    path('publicar/', views.publicar_trabajo, name='publicar_trabajo'),
    path('trabajo_exitoso/', views.trabajo_exitoso, name='trabajo_exitoso'),
    path('subir_cv', views.subir_cv, name='subir_cv'),
    path('verificar_dni/', views.verificar_dni, name='verificar_dni'),
    path('verificar_email/', views.verificar_email, name='verificar_email'),
    path('formulario_exitoso/', views.formulario_exitoso, name='formulario_exitoso'),
    path('empleos/', views.listar_trabajos, name='listar_trabajos'),
    path('empleo/<int:trabajo_id>/', views.detalle_trabajo, name='detalle_trabajo'),
    path('localidad/<int:localidad_id>/', views.listar_trabajos_por_localidad, name='listar_trabajos_por_localidad'),
    path('categoria/<int:categoria_id>/', views.listar_trabajos_por_categoria, name='listar_trabajos_por_categoria'),
    path('verificar_postulacion/', views.verificar_postulacion, name="verificar_postulacion"),
    path('preguntas-frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    
]
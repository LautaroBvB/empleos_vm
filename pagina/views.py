from django.shortcuts import render
from .models import Trabajo, Localidad, Categoria, JornadaLaboral, Modalidad, Genero, Postulante
from django.http import JsonResponse
from .forms import TrabajoForm, PostulanteForm
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from datetime import date
from django.contrib.auth.hashers import check_password

def preguntas_frecuentes(request):
    return render(request, 'preguntas_frecuentes.html')

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

def contacto(request):
    return render(request, 'contacto.html')



def verificar_postulacion(request):
    estado = None
    comentario = None
    error = None

    if request.method == 'POST':
        dni = request.POST.get('dni')
        contraseña = request.POST.get('contraseña')

        try:
            postulante = get_object_or_404(Postulante, dni=dni)
            if check_password(contraseña, postulante.contraseña):
                estado = postulante.estado
                comentario = postulante.comentario
            else:
                error = "Contraseña incorrecta."
        except:
            error = "DNI no encontrado."

    return render(request, 'verificar_postulacion.html', {
        'estado': estado,
        'comentario': comentario,
        'error': error
    })


def inicio(request):
    categorias = Categoria.objects.all()
    return render(request, 'inicio.html', {'categorias': categorias})

def publicar_trabajo(request):
    if request.method == "POST":
        form = TrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("trabajo_exitoso")
    else:
        form = TrabajoForm()
    return render(request, "publicar_trabajo.html", {"form": form})


def trabajo_exitoso(request):
    return render(request, 'trabajo_exitoso.html')

def subir_cv(request):
    if request.method == 'POST':
        form = PostulanteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('formulario_exitoso')
    else:
        form = PostulanteForm()
    return render(request, 'subir_cv.html', {'form': form})

def verificar_dni(request):
    dni = request.GET.get('dni', None)
    existe = Postulante.objects.filter(dni=dni).exists()
    return JsonResponse({'exists': existe})

def verificar_email(request):
    email = request.GET.get('email', None)
    existe = Postulante.objects.filter(email=email).exists()
    return JsonResponse({'exists': existe})

def formulario_exitoso(request):
    return render(request, 'formulario_exitoso.html')

def listar_trabajos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    trabajos = Trabajo.objects.filter(categoria=categoria).order_by('-fecha')
    ahora = timezone.now().date()

    for trabajo in trabajos:
        dias = (ahora - trabajo.fecha).days
        if dias == 0:
            trabajo.dias_publicado = "Publicado hoy"
        elif dias == 1:
            trabajo.dias_publicado = "Publicado ayer"
        else:
            trabajo.dias_publicado = f"Publicado hace {dias} días"

    return render(request, 'listar_categorias.html', {'categoria': categoria, 'trabajos': trabajos})

def listar_trabajos_por_localidad(request, localidad_id):
    localidad = get_object_or_404(Localidad, id=localidad_id)
    trabajos = Trabajo.objects.filter(localidad=localidad).order_by('-fecha')
    ahora = timezone.now().date()

    for trabajo in trabajos:
        dias = (ahora - trabajo.fecha).days
        if dias == 0:
            trabajo.dias_publicado = "Publicado hoy"
        elif dias == 1:
            trabajo.dias_publicado = "Publicado ayer"
        else:
            trabajo.dias_publicado = f"Publicado hace {dias} días"

    return render(request, 'listar_localidades.html', {'localidad': localidad, 'trabajos': trabajos})


def listar_trabajos(request):
    trabajos = Trabajo.objects.all().order_by('-fecha')
    ahora = timezone.now().date()

    localidades_seleccionadas = request.GET.getlist('localidad')
    categorias_seleccionadas = request.GET.getlist('categoria')
    jornadas_seleccionadas = request.GET.getlist('jornada')
    modalidades_seleccionadas = request.GET.getlist('modalidad')
    generos_seleccionados = request.GET.getlist('genero')
    urgente = request.GET.get('urgente')
    vacantes = request.GET.get('vacantes')
    sin_experiencia = request.GET.get('sin_experiencia')

    if localidades_seleccionadas:
        trabajos = trabajos.filter(localidad__id__in=localidades_seleccionadas)
    if categorias_seleccionadas:
        trabajos = trabajos.filter(categoria__id__in=categorias_seleccionadas)
    if jornadas_seleccionadas:
        trabajos = trabajos.filter(tipo_jornada__id__in=jornadas_seleccionadas)
    if modalidades_seleccionadas:
        trabajos = trabajos.filter(modalidad__id__in=modalidades_seleccionadas)
    if generos_seleccionados:
        trabajos = trabajos.filter(genero__id__in=generos_seleccionados)
    if urgente:
        trabajos = trabajos.filter(urgente=True)
    if vacantes:
        trabajos = trabajos.filter(cantidad__gt=1)
    if sin_experiencia:
        trabajos = trabajos.filter(experiencia=False)

    for trabajo in trabajos:
        dias = (ahora - trabajo.fecha).days
        trabajo.dias_publicado = "Publicado hoy" if dias == 0 else f"Publicado hace {dias} días"

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        trabajos_data = [
            {
                "id": trabajo.id,
                "titulo": trabajo.titulo,
                "empresa": trabajo.empresa,
                "dias_publicado": trabajo.dias_publicado,
                "imagen": trabajo.imagen.url if trabajo.imagen else None,
                "tipo_jornada": trabajo.tipo_jornada.nombre,
                "descripcion": trabajo.descripcion[:100] + "...",
            }
            for trabajo in trabajos
        ]
        return JsonResponse({"trabajos": trabajos_data})

    localidades = Localidad.objects.all()
    categorias = Categoria.objects.all()
    jornadas = JornadaLaboral.objects.all()
    modalidades = Modalidad.objects.all()
    generos = Genero.objects.all()

    return render(request, 'listar_trabajos.html', {
        'trabajos': trabajos,
        'localidades': localidades,
        'categorias': categorias,
        'jornadas': jornadas,
        'modalidades': modalidades,
        'generos': generos
    })

def detalle_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)

    trabajos_localidad = Trabajo.objects.filter(localidad=trabajo.localidad)
    trabajos_categoria = Trabajo.objects.filter(categoria=trabajo.categoria)

    trabajos_similares = Trabajo.objects.filter(
        categoria=trabajo.categoria
    ).exclude(id=trabajo_id).order_by('-fecha')[:5]

    for t in trabajos_similares:
        dias = (date.today() - t.fecha).days
        if dias == 0:
            t.dias_publicado = "Publicado hoy"
        elif dias == 1:
            t.dias_publicado = "Publicado ayer"
        else:
            t.dias_publicado = f"Publicado hace {dias} días"

    dias_publicado = (date.today() - trabajo.fecha).days
    if dias_publicado == 0:
        dias_publicado_texto = "Publicado hoy"
    elif dias_publicado == 1:
        dias_publicado_texto = "Publicado ayer"
    else:
        dias_publicado_texto = f"Publicado hace {dias_publicado} días"

    return render(request, 'detalle_trabajo.html', {
        'trabajo': trabajo,
        'trabajos_localidad': trabajos_localidad,
        'trabajos_categoria': trabajos_categoria,
        'trabajos_similares': trabajos_similares,
        'dias_publicado': dias_publicado_texto
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Trabajo, Localidad
from .forms import TrabajoForm, PostulanteForm
from django.utils import timezone
from datetime import date
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

def crear_trabajo(request):
    if request.method == 'POST':
        form = TrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')  # Redirige a la lista de trabajos, por ejemplo
    else:
        form = TrabajoForm()
    return render(request, 'crear_trabajo.html', {'form': form})


def formulario_exitoso(request):
    return render(request, 'formulario_exitoso.html')

def subir_cv(request):
    if request.method == 'POST':
        form = PostulanteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('formulario_exitoso')
    else:
        form = PostulanteForm()
    return render(request, 'subir_cv.html', {'form': form})


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        return JsonResponse({'fileUrl': file_url})  # Retorna la URL del archivo cargado
    return JsonResponse({'error': 'No file uploaded'}, status=400)


def inicio(request):
    categorias = Categoria.objects.all()
    return render(request, 'inicio.html', {'categorias': categorias})

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



def listar_categorias(request):
    categorias = Trabajo.objects.values_list('categoria', flat=True).distinct()
    return render(request, 'listar_categorias.html', {'categorias': categorias})

def listar_localidades(request):
    localidades = Trabajo.objects.values_list('localidad', flat=True).distinct()
    return render(request, 'listar_localidades.html', {'localidades': localidades})


def detalle_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    trabajos_categoria = Trabajo.objects.filter(categoria=categoria)
    return render(request, 'detalle_categoria.html', {'categoria': categoria, 'trabajos_categoria': trabajos_categoria})

def detalle_localidad(request, localidad_id):
    localidad = get_object_or_404(Localidad, id=localidad_id)
    trabajos_localidad = Trabajo.objects.filter(localidad=localidad)
    return render(request, 'detalle_localidad.html', {'localidad': localidad, 'trabajos_localidad': trabajos_localidad})


def listar_trabajos(request):
    trabajos = Trabajo.objects.all()
    ahora = timezone.now().date()

    for trabajo in trabajos:
        dias = (ahora - trabajo.fecha).days

        if dias == 0:
            trabajo.dias_publicado = "Publicado hoy"
        elif dias == 1:
            trabajo.dias_publicado = "Publicado ayer"
        else:
            trabajo.dias_publicado = f"Publicado hace {dias} días"

    return render(request, 'listar_trabajos.html', {'trabajos': trabajos})


def publicar_trabajo(request):
    if request.method == "POST":
        form = TrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")  # Cambia "home" por la URL de redirección tras publicar
    else:
        form = TrabajoForm()
    return render(request, "publicar_trabajo.html", {"form": form})

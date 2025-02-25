from django import forms
from .models import Trabajo, Postulante

class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = [
            'titulo', 'empresa', 'categoria', 'cantidad', 'localidad', 
            'tipo_jornada', 'modalidad', 'genero', 'descripcion', 
            'experiencia', 'acerca_de', 'rubro', 'direccion', 'celular', 
            'urgente', 'requisitos', 'imagen'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'acerca_de': forms.Textarea(attrs={'rows': 3}),
        }


class PostulanteForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput)

    # Nuevos campos
    dia = forms.IntegerField(min_value=1, max_value=31)
    mes = forms.IntegerField(min_value=1, max_value=12)
    año = forms.IntegerField(min_value=1900)
    
    # Campos con tipo "number" en el HTML
    dni = forms.CharField(widget=forms.NumberInput(attrs={'type': 'number'}))
    caracteristica = forms.CharField(widget=forms.NumberInput(attrs={'type': 'number'}))
    numero = forms.CharField(widget=forms.NumberInput(attrs={'type': 'number'}))

    class Meta:
        model = Postulante
        fields = ['archivo', 'nombre', 'apellido', 'dni', 'caracteristica', 'numero', 'email', 'contraseña', 'confirmar_contraseña', 'dia', 'mes', 'año']

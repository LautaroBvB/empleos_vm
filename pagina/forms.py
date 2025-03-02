from django import forms
from .models import Trabajo, Postulante
from django_select2.forms import Select2MultipleWidget
import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

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
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
            'tipo_jornada': forms.Select(attrs={'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'experiencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acerca_de': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rubro': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.NumberInput(attrs={'class': 'form-control'}),
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requisitos': Select2MultipleWidget(attrs={'class': 'form-control', 'rows': 3}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }
        



class PostulanteForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput)

    # Nuevos campos
    dia = forms.IntegerField(min_value=1, max_value=31)
    mes = forms.IntegerField(min_value=1, max_value=12)
    año = forms.IntegerField(min_value=1900)

    # Campos con tipo "number" en el HTML
    dni = forms.CharField(
        widget=forms.NumberInput(attrs={'type': 'number'}),
        validators=[RegexValidator(r'^\d+$', 'Solo números permitidos')]
    )
    caracteristica = forms.CharField(widget=forms.NumberInput(attrs={'type': 'number'}))
    numero = forms.CharField(widget=forms.NumberInput(attrs={'type': 'number'}))

    class Meta:
        model = Postulante
        fields = ['archivo', 'nombre', 'apellido', 'dni', 'caracteristica', 'numero', 'email', 'contraseña', 'confirmar_contraseña', 'dia', 'mes', 'año']

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        confirmar_contraseña = cleaned_data.get("confirmar_contraseña")

        if contraseña != confirmar_contraseña:
            self.add_error('confirmar_contraseña', 'Las contraseñas no coinciden')

        # Validación de fecha
        dia = cleaned_data.get("dia")
        mes = cleaned_data.get("mes")
        año = cleaned_data.get("año")
        if dia and mes and año:
            try:
                datetime.datetime(año, mes, dia)
            except ValueError:
                self.add_error('dia', 'Fecha inválida')

        return cleaned_data

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if Postulante.objects.filter(dni=dni).exists():
            raise ValidationError("El DNI ya está registrado.")
        return dni

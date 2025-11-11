from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Perfil, Resena

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        exclude = ['user', 'calificacion_promedio']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'sobre_mi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'nivel_academico': forms.Select(attrs={'class': 'form-control'}),
            'disponible_para_citas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telefono_estudiante': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_profesional': forms.EmailInput(attrs={'class': 'form-control'}),
            'horarios_atencion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['nombre_paciente', 'puntuacion', 'comentario']
        widgets = {
            'nombre_paciente': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'puntuacion': forms.HiddenInput(),
            'comentario': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu reseña...'}),
        }


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'nombre_completo',
            'foto_perfil',
            'sobre_mi',
            'nivel_academico',
            'carnet_de_estudiante',
            'telefono_estudiante',
            'correo_profesional',
            'horarios_atencion',
            'disponible_para_citas'
        ]

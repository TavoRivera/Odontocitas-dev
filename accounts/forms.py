
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

class UserEditForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Dejar en blanco para no cambiar la contraseña.")
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

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

    def clean_foto_perfil(self):
        foto_perfil = self.cleaned_data.get('foto_perfil', False)
        
        # Si el usuario intenta limpiar la imagen existente
        if foto_perfil is False:
            # Si el perfil ya tiene una foto y NO es la de por defecto, no se le permite borrarla
            if self.instance.pk and self.instance.foto_perfil and 'default_profile.png' not in self.instance.foto_perfil.url:
                 # Mantenemos la foto actual
                return self.instance.foto_perfil

        # Si no se sube una foto nueva
        if not foto_perfil:
            # Y el perfil es nuevo o aún tiene la foto por defecto
            if not self.instance.pk or 'default_profile.png' in self.instance.foto_perfil.url:
                raise forms.ValidationError(
                    "La foto de perfil es obligatoria. Por favor, sube una imagen para continuar.", 
                    code='required'
                )

        return foto_perfil

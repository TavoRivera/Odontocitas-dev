from django import forms
from django.core.exceptions import ValidationError
from .models import Cita, Oferta
import datetime
from django.utils import timezone

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 150.00, A convenir, etc.'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'titulo': 'Título del Tratamiento',
            'descripcion': 'Descripción Detallada',
            'precio': 'Precio (C$)',
            'categoria': 'Categoría del Servicio',
            'imagen': 'Foto Principal (Opcional)'
        }

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['nombre_paciente', 'telefono_paciente', 'email_paciente', 'fecha_atencion', 'consulta']
        widgets = {
            'fecha_atencion': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'nombre_paciente': forms.TextInput(attrs={'placeholder': 'Tu nombre completo', 'class': 'form-control'}),
            'telefono_paciente': forms.TextInput(attrs={'placeholder': 'Tu número de teléfono', 'class': 'form-control'}),
            'email_paciente': forms.EmailInput(attrs={'placeholder': 'tu@email.com (Opcional)', 'class': 'form-control'}),
            'consulta': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe brevemente tu consulta (Opcional)', 'class': 'form-control'}),
        }
        labels = {
            'nombre_paciente': 'Nombre Completo',
            'telefono_paciente': 'Teléfono',
            'email_paciente': 'Correo Electrónico',
            'fecha_atencion': 'Fecha y Hora Deseada',
            'consulta': 'Consulta Adicional',
        }

    def clean_fecha_atencion(self):
        """
        Validador personalizado para el campo de fecha y hora.
        """
        fecha = self.cleaned_data.get('fecha_atencion')

        if fecha:
            # 1. No se puede agendar en el pasado
            if fecha < timezone.now():
                raise ValidationError("No puedes agendar una cita en una fecha u hora pasada.")

            # 2. Validar que no sea domingo (weekday() de Lunes=0 a Domingo=6)
            if fecha.weekday() == 6:
                raise ValidationError("No se pueden agendar citas en día domingo. Por favor, elige otro día.")

            # 3. Validar que la hora esté entre las 8 AM y las 4 PM (16:00)
            if not (8 <= fecha.hour < 16):
                raise ValidationError("El horario de atención es de 8:00 AM a 4:00 PM. Por favor, elige una hora válida.")

        return fecha

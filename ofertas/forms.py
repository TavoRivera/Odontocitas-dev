from django import forms
from .models import Oferta, Cita
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['nombre_paciente', 'telefono_paciente', 'email_paciente', 'fecha_atencion', 'consulta']
        labels = {
            'nombre_paciente': 'Nombre completo del paciente',
            'telefono_paciente': 'Tu número de teléfono',
            'email_paciente': 'Tu correo electrónico (Opcional)',
            'fecha_atencion': 'Indica la fecha y hora que deseas ser atendido(a)',
            'consulta': 'Describe brevemente qué necesitas (Opcional)',
        }
        widgets = {
            'nombre_paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'email_paciente': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_atencion': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'  # <-- ¡CLASE AÑADIDA!
                }
            ),
            'consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_fecha_atencion(self):
        fecha = self.cleaned_data.get('fecha_atencion')
        if fecha:
            # 1. No se puede agendar en el pasado.
            if fecha < timezone.now():
                raise ValidationError("No puedes agendar una cita en el pasado.", code='past_date')
            
            # 2. No se pueden agendar citas los domingos (domingo es 6 en weekday(), 0 en JS).
            if fecha.weekday() == 6:
                raise ValidationError("No se pueden agendar citas los domingos.", code='sunday')

            # 3. Horario de atención de 8 AM a 4 PM (16:00).
            if not (datetime.time(8, 0) <= fecha.time() < datetime.time(16, 0)):
                raise ValidationError("El horario de atención es de 8:00 AM a 4:00 PM.", code='time_out_of_range')

        return fecha

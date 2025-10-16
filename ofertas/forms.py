from django import forms
from .models import Oferta

class OfertaForm(forms.ModelForm):
    class Meta:
        model = Oferta
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'imagen', 'disponible']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

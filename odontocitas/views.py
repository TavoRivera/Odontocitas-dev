from django.shortcuts import render
from ofertas.models import Oferta

def index(request):
    # Ahora, solo se muestran las ofertas de estudiantes que están disponibles para citas.
    ofertas_recientes = Oferta.objects.filter(estudiante__disponible_para_citas=True).order_by('-fecha_creacion')[:3]
    
    context = {
        'ofertas_recientes': ofertas_recientes
    }
    
    return render(request, 'index.html', context)

from django.shortcuts import render
from ofertas.models import Oferta

def index(request):
    # CORRECCIÓN: Se quita el filtro 'disponible=True' para mostrar las ofertas más recientes.
    # Esto asegura que siempre se muestren las últimas ofertas creadas en la página de inicio.
    ofertas_recientes = Oferta.objects.order_by('-fecha_creacion')[:3]
    
    context = {
        'ofertas_recientes': ofertas_recientes
    }
    
    return render(request, 'index.html', context)

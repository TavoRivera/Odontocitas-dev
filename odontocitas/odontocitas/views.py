from django.shortcuts import render
from ofertas.models import Oferta

def index(request):
    # Obtener las 3 ofertas más recientes
    ofertas_recientes = Oferta.objects.order_by('-fecha_creacion')[:3]
    
    context = {
        'ofertas_recientes': ofertas_recientes
    }
    
    return render(request, 'index.html', context)

def handler404(request, exception):
    """
    Vista personalizada para manejar los errores 404 (Página no encontrada).
    """
    return render(request, '404.html', status=404)

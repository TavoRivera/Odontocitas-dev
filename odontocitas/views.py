from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from ofertas.models import Oferta
from accounts.models import Perfil

def index(request):
    # Obtener las 3 ofertas más recientes de estudiantes disponibles
    ofertas_recientes = Oferta.objects.filter(estudiante__disponible_para_citas=True).order_by('-fecha_creacion')[:3]
    
    # Obtener los 3 estudiantes mejor calificados y disponibles
    estudiantes_destacados = Perfil.objects.filter(disponible_para_citas=True).order_by('-calificacion_promedio')[:3]
    
    context = {
        'ofertas_recientes': ofertas_recientes,
        'estudiantes_destacados': estudiantes_destacados,
    }
    
    return render(request, 'index.html', context)

@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

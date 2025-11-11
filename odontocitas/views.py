from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from ofertas.models import Oferta

def index(request):
    # Ahora, solo se muestran las ofertas de estudiantes que están disponibles para citas.
    ofertas_recientes = Oferta.objects.filter(estudiante__disponible_para_citas=True).order_by('-fecha_creacion')[:3]
    
    context = {
        'ofertas_recientes': ofertas_recientes
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

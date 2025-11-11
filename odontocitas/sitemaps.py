from django.contrib import sitemaps
from django.urls import reverse
from ofertas.models import Oferta
from accounts.models import Perfil

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'lista_ofertas', 'lista_estudiantes']

    def location(self, item):
        return reverse(item)

class OfertaSitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Oferta.objects.filter(activa=True)

    def lastmod(self, obj):
        return obj.fecha_creacion

class EstudianteSitemap(sitemaps.Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Perfil.objects.filter(rol='Estudiante', usuario__is_active=True)

    def location(self, obj):
        return reverse('detalle_estudiante', args=[obj.usuario.username])

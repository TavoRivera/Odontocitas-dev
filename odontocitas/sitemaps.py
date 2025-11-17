from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from accounts.models import Perfil
from ofertas.models import Oferta

class PerfilSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Perfil.objects.filter(disponible_para_citas=True)

    def lastmod(self, obj):
        # Asumiendo que el modelo User tiene un campo `date_joined` o similar
        return obj.user.date_joined

    def location(self, obj):
        return reverse('detalle_estudiante', args=[obj.user.username])

class OfertaSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Oferta.objects.all()

    def lastmod(self, obj):
        # Asumiendo que Oferta tiene un campo de fecha de modificación/creación
        return obj.fecha_creacion

    def location(self, obj):
        return reverse('detalle_oferta', args=[obj.id])

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return ['index', 'lista_estudiantes', 'lista_ofertas']

    def location(self, item):
        return reverse(item)

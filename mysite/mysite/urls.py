"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from odontocitas.odontocitas import views

# Importaciones para las nuevas vistas de estudiantes
from accounts.views import lista_estudiantes, detalle_estudiante

# Importaciones para servir archivos de medios en desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('ofertas/', include('ofertas.urls')),
    path('', views.index, name='index'),

    # Rutas para la lista y detalle de estudiantes
    path('estudiantes/', lista_estudiantes, name='lista_estudiantes'),
    path('estudiantes/<int:user_id>/', detalle_estudiante, name='detalle_estudiante'),
]

# Añadir la configuración para servir archivos de medios (como fotos de perfil)
# durante el desarrollo.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'odontocitas.odontocitas.views.handler404'

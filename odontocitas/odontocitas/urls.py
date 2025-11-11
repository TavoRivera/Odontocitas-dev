"""
URL configuration for odontocitas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import views from the correct apps
from odontocitas.views import index as home_view
from accounts.views import lista_estudiantes, detalle_estudiante, eliminar_resena

urlpatterns = [
    # Core
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Main homepage

    # App-specific URLs
    path('accounts/', include('accounts.urls')), # For login, logout, register, profile_edit
    path('ofertas/', include('ofertas.urls')),

    # Public-facing student and review URLs (imported from accounts.views)
    path('estudiantes/', lista_estudiantes, name='lista_estudiantes'),
    path('estudiante/<int:user_id>/', detalle_estudiante, name='detalle_estudiante'),
    path('resena/eliminar/<int:resena_id>/', eliminar_resena, name='eliminar_resena'),
]

# Add static and media files for development server
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import views from the correct apps
from odontocitas.views import index as home_view
from accounts.views import lista_estudiantes, detalle_estudiante, eliminar_resena

urlpatterns = [
    # Core Admin and Home Page
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),

    # Include app-specific URLs
    # 'accounts.urls' are namespaced and will handle /accounts/login, /accounts/register, etc.
    path('accounts/', include('accounts.urls')),
    path('ofertas/', include('ofertas.urls')),

    # Public-facing URLs that were causing NoReverseMatch errors.
    # These are now correctly placed in the root URLconf.
    path('estudiantes/', lista_estudiantes, name='lista_estudiantes'),
    path('estudiante/<int:user_id>/', detalle_estudiante, name='detalle_estudiante'),
    path('resena/eliminar/<int:resena_id>/', eliminar_resena, name='eliminar_resena'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

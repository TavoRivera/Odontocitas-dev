from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # Incluye las URLs de autenticación por defecto de Django (login, logout, cambio de contraseña, etc.)
    # Vivirán bajo el prefijo /accounts/ -> /accounts/login/, /accounts/logout/, etc.
    path('', include('django.contrib.auth.urls')),

    # Rutas personalizadas para la gestión de cuentas
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Rutas para la administración de usuarios (solo superusuarios)
    path('users/', views.lista_usuarios, name='lista_usuarios'),
    path('users/edit/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('users/delete/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('resena/eliminar/<int:resena_id>/', views.eliminar_resena, name='eliminar_resena'),
]

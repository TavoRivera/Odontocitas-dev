from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('users/', views.lista_usuarios, name='lista_usuarios'),
    path('users/edit/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('users/delete/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('', include('django.contrib.auth.urls')),
]

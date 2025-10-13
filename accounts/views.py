from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegistrationForm, PerfilForm, UserEditForm
from .models import Perfil
from ofertas.models import Oferta # Importar el modelo Oferta

def superuser_check(user):
    return user.is_superuser

@user_passes_test(superuser_check)
def lista_usuarios(request):
    users = User.objects.all()
    return render(request, 'registration/lista_usuarios.html', {'users': users})

@user_passes_test(superuser_check)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@user_passes_test(superuser_check)
def editar_usuario(request, user_id):
    edited_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=edited_user)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UserEditForm(instance=edited_user)
    return render(request, 'registration/editar_usuario.html', {'form': form, 'edited_user': edited_user})

@user_passes_test(superuser_check)
def eliminar_usuario(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('lista_usuarios')
    return render(request, 'registration/eliminar_usuario.html', {'user_to_delete': user_to_delete})


@login_required
def edit_profile(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        perfil = Perfil(user=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'registration/edit_profile.html', {'form': form})

# --- Vistas para el listado y detalle de estudiantes (perfiles) ---

def lista_estudiantes(request):
    """Muestra la lista de todos los perfiles de estudiantes."""
    perfiles = Perfil.objects.all()
    return render(request, 'estudiantes/lista_estudiantes.html', {'perfiles': perfiles})

def detalle_estudiante(request, user_id):
    """Muestra el perfil detallado de un estudiante y sus ofertas."""
    perfil = get_object_or_404(Perfil, user_id=user_id)
    # Obtener las ofertas publicadas por ese usuario
    ofertas = Oferta.objects.filter(creador=perfil.user)
    return render(request, 'estudiantes/detalle_estudiante.html', {'perfil': perfil, 'ofertas': ofertas})

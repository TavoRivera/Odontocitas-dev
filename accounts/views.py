
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .forms import RegistrationForm, PerfilForm, UserEditForm, ResenaForm
from .models import Perfil, Resena
from ofertas.models import Oferta

def superuser_check(user):
    return user.is_superuser

@user_passes_test(superuser_check)
def lista_usuarios(request):
    users_list = User.objects.all().order_by('username')
    query = request.GET.get('q')
    if query:
        users_list = users_list.filter(
            Q(username__icontains=query) | Q(email__icontains=query) |
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).distinct()
    return render(request, 'registration/lista_usuarios.html', {'users': users_list})

@user_passes_test(superuser_check)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'El usuario "{user.username}" ha sido creado exitosamente.')
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
            messages.success(request, f'El usuario "{edited_user.username}" ha sido actualizado.')
            return redirect('lista_usuarios')
    else:
        form = UserEditForm(instance=edited_user)
    return render(request, 'registration/editar_usuario.html', {'form': form, 'edited_user': edited_user})

@user_passes_test(superuser_check)
def eliminar_usuario(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'El usuario "{username}" ha sido eliminado.')
        return redirect('lista_usuarios')
    return render(request, 'registration/eliminar_usuario.html', {'user_to_delete': user_to_delete})

@login_required
def edit_profile(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado.')
            return redirect('edit_profile')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'registration/edit_profile.html', {'form': form})

def lista_estudiantes(request):
    perfiles = Perfil.objects.filter(user__is_superuser=False)
    return render(request, 'estudiantes/lista_estudiantes.html', {'perfiles': perfiles})

def detalle_estudiante(request, user_id):
    perfil = get_object_or_404(Perfil, user_id=user_id)
    ofertas = Oferta.objects.filter(estudiante=perfil)
    resenas = Resena.objects.filter(estudiante=perfil, activa=True).order_by('-fecha_creacion')
    
    resena_enviada = request.session.pop('resena_enviada', False)
    total_resenas = resenas.count()

    if request.method == 'POST':
        resena_form = ResenaForm(request.POST)
        if resena_form.is_valid():
            nueva_resena = resena_form.save(commit=False)
            nueva_resena.estudiante = perfil
            nueva_resena.save()
            request.session['resena_enviada'] = True
            # --- ¡CORRECCIÓN! El argumento correcto es user_id, no estudiante_id ---
            return redirect('detalle_estudiante', user_id=user_id)
    else:
        resena_form = ResenaForm()

    contexto = {
        'perfil': perfil,
        'ofertas': ofertas,
        'resenas': resenas,
        'resena_form': resena_form,
        'resena_enviada': resena_enviada,
        'total_resenas': total_resenas,
    }
    
    return render(request, 'estudiantes/detalle_estudiante.html', contexto)

# --- ¡NUEVA VISTA! ---
@require_POST
@user_passes_test(superuser_check)
def eliminar_resena(request, resena_id):
    # Busca la reseña, si no existe, devuelve un error 404
    resena = get_object_or_404(Resena, id=resena_id)
    
    # Guarda el ID del perfil de estudiante para la redirección
    user_id_redirect = resena.estudiante.user.id
    
    # Elimina la reseña
    resena.delete()
    
    # Envía un mensaje de éxito
    messages.success(request, "La reseña ha sido eliminada correctamente.")
    
    # Redirige de vuelta a la página del perfil del estudiante
    return redirect('detalle_estudiante', user_id=user_id_redirect)

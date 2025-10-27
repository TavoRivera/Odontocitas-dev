from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Oferta, CATEGORIAS_CHOICES, Cita
from .forms import OfertaForm, CitaForm
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

def lista_ofertas(request):
    """
    Muestra una lista de todas las ofertas, con capacidad de búsqueda y filtrado.
    """
    mostrar_todos = request.GET.get('mostrar_todos') == 'true'
    ofertas = Oferta.objects.filter(disponible=True)

    if not mostrar_todos:
        ofertas = ofertas.filter(estudiante__disponible_para_citas=True)

    query = request.GET.get('q')
    categoria_seleccionada = request.GET.get('categoria')

    if query:
        ofertas = ofertas.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )

    if categoria_seleccionada:
        ofertas = ofertas.filter(categoria=categoria_seleccionada)
        
    ofertas = ofertas.order_by('-fecha_actualizacion')

    categorias = CATEGORIAS_CHOICES

    context = {
        'ofertas': ofertas,
        'categorias': categorias,
        'query_actual': query,
        'categoria_seleccionada': categoria_seleccionada,
        'mostrar_todos': mostrar_todos,
    }
    
    return render(request, 'ofertas/lista_ofertas.html', context)

def detalle_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.oferta = oferta
            cita.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = CitaForm()
    min_datetime = timezone.now().strftime('%Y-%m-%dT%H:%M')
    form.fields['fecha_atencion'].widget.attrs['min'] = min_datetime

    context = {
        'oferta': oferta,
        'form': form,
    }
    return render(request, 'ofertas/detalle_oferta.html', context)

@login_required
def crear_oferta(request):
    if not hasattr(request.user, 'perfil'):
        messages.warning(request, 'Acción no permitida. Debes tener un perfil para poder crear un tratamiento.')
        return redirect('lista_ofertas')

    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.estudiante = request.user.perfil
            oferta.save()
            messages.success(request, f'El tratamiento "{oferta.titulo}" se ha creado exitosamente.')
            return redirect('mis_ofertas')
    else:
        form = OfertaForm()
        
    return render(request, 'ofertas/crear_oferta.html', {'form': form})


@login_required
def mis_ofertas(request):
    try:
        perfil_usuario = request.user.perfil
        ofertas_del_usuario = Oferta.objects.filter(estudiante=perfil_usuario).order_by('-fecha_actualizacion')
    except AttributeError:
        ofertas_del_usuario = []

    return render(request, 'ofertas/mis_ofertas.html', {'ofertas': ofertas_del_usuario})

@login_required
def eliminar_oferta(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk, estudiante=request.user.perfil)

    if request.method == 'POST':
        oferta.delete()
        messages.success(request, f'El tratamiento "{oferta.titulo}" ha sido eliminado.')
        return redirect('mis_ofertas')

    return render(request, 'ofertas/confirmar_eliminacion.html', {'oferta': oferta})

@login_required
def editar_oferta(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk, estudiante=request.user.perfil)

    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES, instance=oferta)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'El tratamiento "{oferta.titulo}" ha sido actualizado.')
            return redirect('mis_ofertas')

    else:
        form = OfertaForm(instance=oferta)

    context = {
        'form': form,
        'oferta': oferta
    }
    return render(request, 'ofertas/editar_oferta.html', context)

@login_required
def lista_solicitudes_citas(request):
    """
    Muestra al estudiante las citas solicitadas, separadas en pendientes y atendidas.
    """
    if not hasattr(request.user, 'perfil'):
        messages.error(request, 'No tienes un perfil de estudiante para ver esta página.')
        return redirect('lista_ofertas')

    # Usamos select_related para optimizar la consulta y evitar N+1 queries
    todas_las_citas = Cita.objects.filter(oferta__estudiante=request.user.perfil).select_related('oferta').order_by('-fecha_creacion')

    citas_pendientes = todas_las_citas.filter(atendida=False)
    citas_atendidas = todas_las_citas.filter(atendida=True)

    context = {
        'citas_pendientes': citas_pendientes,
        'citas_atendidas': citas_atendidas,
    }
    return render(request, 'ofertas/lista_solicitudes.html', context)

@login_required
@require_POST # Asegura que esta vista solo acepte peticiones POST
def marcar_cita_atendida(request, cita_id):
    """ Marca una cita como atendida. """
    cita = get_object_or_404(Cita, pk=cita_id, oferta__estudiante=request.user.perfil)
    cita.atendida = True
    cita.save()
    messages.success(request, f"La cita para '{cita.nombre_paciente}' ha sido marcada como atendida.")
    return redirect('lista_solicitudes')

@login_required
@require_POST # Asegura que esta vista solo acepte peticiones POST
def eliminar_cita(request, cita_id):
    """ Elimina una solicitud de cita. """
    cita = get_object_or_404(Cita, pk=cita_id, oferta__estudiante=request.user.perfil)
    nombre_paciente = cita.nombre_paciente
    cita.delete()
    messages.success(request, f"La solicitud de cita de '{nombre_paciente}' ha sido eliminada.")
    return redirect('lista_solicitudes')

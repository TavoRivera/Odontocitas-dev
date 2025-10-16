from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Oferta, CATEGORIAS_CHOICES
from .forms import OfertaForm
from django.db.models import Q

def lista_ofertas(request):
    """
    Muestra una lista de todas las ofertas, con capacidad de búsqueda y filtrado.
    """
    ofertas = Oferta.objects.filter(disponible=True).order_by('-fecha_actualizacion')
    
    query = request.GET.get('q')
    categoria_seleccionada = request.GET.get('categoria')

    if query:
        ofertas = ofertas.filter(
            Q(titulo__icontains=query) | Q(descripcion__icontains=query)
        )

    if categoria_seleccionada:
        ofertas = ofertas.filter(categoria=categoria_seleccionada)
        
    categorias = CATEGORIAS_CHOICES

    context = {
        'ofertas': ofertas,
        'categorias': categorias,
        'query_actual': query,
        'categoria_seleccionada': categoria_seleccionada,
    }
    
    return render(request, 'ofertas/lista_ofertas.html', context)

def detalle_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    return render(request, 'ofertas/detalle_oferta.html', {'oferta': oferta})

@login_required
def crear_oferta(request):
    if not hasattr(request.user, 'perfil'):
        messages.warning(request, 'Para crear un tratamiento, primero debes completar tu perfil de estudiante.')
        return redirect('edit_profile')

    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.estudiante = request.user.perfil
            oferta.save()
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
        # Si el usuario no tiene perfil, la lista de ofertas estará vacía
        ofertas_del_usuario = []

    return render(request, 'ofertas/mis_ofertas.html', {'ofertas': ofertas_del_usuario})

@login_required
def eliminar_oferta(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk, estudiante=request.user.perfil)

    if request.method == 'POST':
        oferta.delete()
        return redirect('mis_ofertas')

    return render(request, 'ofertas/confirmar_eliminacion.html', {'oferta': oferta})

@login_required
def editar_oferta(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk, estudiante=request.user.perfil)

    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES, instance=oferta)
        
        if form.is_valid():
            form.save()
            return redirect('mis_ofertas')

    else:
        form = OfertaForm(instance=oferta)

    context = {
        'form': form,
        'oferta': oferta
    }
    return render(request, 'ofertas/editar_oferta.html', context)

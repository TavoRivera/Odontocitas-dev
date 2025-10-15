from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# --- ¡CORRECCIÓN! Se importa la constante directamente ---
from .models import Oferta, ImagenOferta, CATEGORIAS_CHOICES
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
        
    # --- ¡CORRECCIÓN! Se usa la constante importada ---
    categorias = CATEGORIAS_CHOICES

    context = {
        'ofertas': ofertas,
        'categorias': categorias,
        'query_actual': query,
        'categoria_seleccionada': categoria_seleccionada,
    }
    
    return render(request, 'ofertas/lista_ofertas.html', context)

# --- El resto de las vistas no cambia ---

def detalle_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    return render(request, 'ofertas/detalle_oferta.html', {'oferta': oferta})

@login_required
def crear_oferta(request):
    # ... (código sin cambios)
    if not hasattr(request.user, 'perfil'):
        return redirect('lista_ofertas')

    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.estudiante = request.user.perfil
            oferta.save()
            
            images = request.FILES.getlist('imagenes')
            for image in images:
                ImagenOferta.objects.create(oferta=oferta, imagen=image)
            
            return redirect('mis_ofertas')
    else:
        form = OfertaForm()
        
    return render(request, 'ofertas/crear_oferta.html', {'form': form})


@login_required
def mis_ofertas(request):
    # ... (código sin cambios)
    try:
        perfil_usuario = request.user.perfil
        ofertas_del_usuario = Oferta.objects.filter(estudiante=perfil_usuario).order_by('-fecha_actualizacion')
    except AttributeError:
        ofertas_del_usuario = []

    return render(request, 'ofertas/mis_ofertas.html', {'ofertas': ofertas_del_usuario})

@login_required
def eliminar_oferta(request, pk):
    # ... (código sin cambios)
    oferta = get_object_or_404(Oferta, pk=pk, estudiante=request.user.perfil)

    if request.method == 'POST':
        oferta.delete()
        return redirect('mis_ofertas')

    return render(request, 'ofertas/confirmar_eliminacion.html', {'oferta': oferta})

@login_required
def editar_oferta(request, pk):
    # ... (código sin cambios)
    oferta = get_object_or_404(Oferta, pk=pk, estudiante=request.user.perfil)

    if request.method == 'POST':
        form = OfertaForm(request.POST, request.FILES, instance=oferta)
        
        if form.is_valid():
            form.save()

            images_to_delete_ids = request.POST.getlist('delete_images')
            if images_to_delete_ids:
                ImagenOferta.objects.filter(id__in=images_to_delete_ids, oferta=oferta).delete()

            new_images = request.FILES.getlist('imagenes')
            for image in new_images:
                ImagenOferta.objects.create(oferta=oferta, imagen=image)
            
            return redirect('mis_ofertas')

    else:
        form = OfertaForm(instance=oferta)

    context = {
        'form': form,
        'oferta': oferta
    }
    return render(request, 'ofertas/editar_oferta.html', context)

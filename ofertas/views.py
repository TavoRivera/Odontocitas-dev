from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Oferta
from .forms import OfertaForm

def lista_ofertas(request):
    ofertas = Oferta.objects.all()
    return render(request, 'ofertas/lista_ofertas.html', {'ofertas': ofertas})

@login_required
def crear_oferta(request):
    if request.method == 'POST':
        form = OfertaForm(request.POST)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.creador = request.user
            oferta.save()
            return redirect('lista_ofertas')
    else:
        form = OfertaForm()
    return render(request, 'ofertas/crear_oferta.html', {'form': form})

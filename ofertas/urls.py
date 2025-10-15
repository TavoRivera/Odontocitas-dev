from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ofertas, name='lista_ofertas'),
    # Ruta para ver el detalle de una oferta específica
    path('<int:oferta_id>/', views.detalle_oferta, name='detalle_oferta'),
    path('crear/', views.crear_oferta, name='crear_oferta'),
    path('mis-ofertas/', views.mis_ofertas, name='mis_ofertas'),
    path('<int:pk>/eliminar/', views.eliminar_oferta, name='eliminar_oferta'),
    path('<int:pk>/editar/', views.editar_oferta, name='editar_oferta'),
]

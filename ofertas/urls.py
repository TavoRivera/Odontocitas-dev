from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ofertas, name='lista_ofertas'),
    path('<int:oferta_id>/', views.detalle_oferta, name='detalle_oferta'),
    path('crear/', views.crear_oferta, name='crear_oferta'),
    path('mis-ofertas/', views.mis_ofertas, name='mis_ofertas'),
    path('<int:pk>/eliminar/', views.eliminar_oferta, name='eliminar_oferta'),
    path('<int:pk>/editar/', views.editar_oferta, name='editar_oferta'),
    path('mis-solicitudes/', views.lista_solicitudes_citas, name='lista_solicitudes'),
    # URLs para las acciones de las citas
    path('cita/<int:cita_id>/marcar-atendida/', views.marcar_cita_atendida, name='marcar_cita_atendida'),
    path('cita/<int:cita_id>/eliminar/', views.eliminar_cita, name='eliminar_cita'),
]

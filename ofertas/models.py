from django.db import models
from accounts.models import Perfil

# --- ¡CORRECCIÓN! Se mueve la lista fuera de la clase ---
CATEGORIAS_CHOICES = [
    ('limpieza', 'Limpieza Dental'),
    ('blanqueamiento', 'Blanqueamiento Dental'),
    ('extraccion', 'Extracción Dental'),
    ('endodoncia', 'Endodoncia'),
    ('ortodoncia', 'Ortodoncia'),
]

class Oferta(models.Model):
    # La lista de categorías ya no está aquí.

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    estudiante = models.ForeignKey(
        Perfil, on_delete=models.CASCADE, related_name='ofertas')
    precio = models.CharField(
        max_length=100,
        help_text='Indica un precio p.e. 100.00 o escribe "A convenir", "Gratis", etc.'
    )
    # El campo 'choices' sigue funcionando porque la constante está en el mismo módulo.
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIAS_CHOICES,
        help_text='Selecciona la categoría del servicio que ofreces.'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class ImagenOferta(models.Model):
    oferta = models.ForeignKey(
        Oferta, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='ofertas_fotos/')

    def __str__(self):
        return f"Imagen para la oferta: {self.oferta.titulo}"

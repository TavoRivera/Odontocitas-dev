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
    # ... (el resto de tus campos de Oferta)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='ofertas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    # Ahora usamos la lista de choices que está fuera de la clase
    categoria = models.CharField(max_length=100, choices=CATEGORIAS_CHOICES, default='limpieza')
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Cita(models.Model):
    nombre_paciente = models.CharField(max_length=255)
    telefono_paciente = models.CharField(max_length=20)
    email_paciente = models.EmailField(blank=True, null=True)
    fecha_atencion = models.DateTimeField(blank=True, null=True)
    consulta = models.TextField(blank=True, null=True)
    atendida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita para {self.nombre_paciente} el {self.fecha_atencion.strftime('%d/%m/%Y') if self.fecha_atencion else 'fecha pendiente'}"

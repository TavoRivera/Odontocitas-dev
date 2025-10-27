from django.db import models
from accounts.models import Perfil
from django.utils import timezone

# --- ¡CORRECCIÓN! Se mueve la lista fuera de la clase ---
CATEGORIAS_CHOICES = [
    ('odontologia_general', 'Odontología General y Preventiva'),
    ('odontologia_restauradora', 'Odontología Restauradora'),
    ('endodoncia', 'Endodoncia'),
    ('periodoncia', 'Periodoncia'),
    ('prostodoncia', 'Prostodoncia (Rehabilitación Oral)'),
    ('cirugia_oral', 'Cirugía Oral Básica'),
    ('ortodoncia', 'Ortodoncia'),
]

class Oferta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    estudiante = models.ForeignKey(
        Perfil, on_delete=models.CASCADE, related_name='ofertas')
    precio = models.CharField(
        max_length=100,
        help_text='Indica un precio p.e. 100.00 o escribe "A convenir", "Gratis", etc.'
    )
    categoria = models.CharField(
        max_length=50,
        choices=CATEGORIAS_CHOICES,
        help_text='Selecciona la categoría del servicio que ofreces.'
    )
    imagen = models.ImageField(upload_to='ofertas_fotos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Cita(models.Model):
    oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, related_name='citas')
    nombre_paciente = models.CharField(max_length=255)
    telefono_paciente = models.CharField(max_length=20)
    email_paciente = models.EmailField(blank=True, null=True)
    # --- CAMPO CORREGIDO CON VALOR POR DEFECTO ---
    fecha_atencion = models.DateTimeField(
        default=timezone.now, 
        help_text="Fecha y hora propuesta por el paciente para la cita."
    )
    consulta = models.TextField(blank=True, null=True)
    atendida = models.BooleanField(default=False)  # Campo para marcar si la cita fue atendida
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.nombre_paciente} para '{self.oferta.titulo}'"

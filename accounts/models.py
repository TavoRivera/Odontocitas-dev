from django.db import models
from django.contrib.auth.models import User

# Modelo para las habilidades que se pueden asignar a un perfil
class Habilidad(models.Model):
    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255, null=True, blank=True)
    # Campo para la ubicación como "Los Angeles, CA"
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    # Campo para la escuela como "Metropolitan School of Dentistry"
    escuela = models.CharField(max_length=100, null=True, blank=True)
    carnet_de_estudiante = models.CharField(max_length=50, null=True, blank=True)
    # Biografía del estudiante
    sobre_mi = models.TextField(null=True, blank=True)
    
    # --- Nuevos campos basados en el diseño ---
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', default='fotos_perfil/default.png')
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    habilidades = models.ManyToManyField(Habilidad, blank=True)

    def __str__(self):
        # Esto ayuda a identificar el perfil en el panel de administrador
        return f'Perfil de {self.user.username}'

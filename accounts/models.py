
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255, null=True, blank=True)

    # --- Información Académica ---
    NIVEL_ACADEMICO_CHOICES = [
        ('1_ANO', '1er Año'),
        ('2_ANO', '2do Año'),
        ('3_ANO', '3er Año'),
        ('4_ANO', '4to Año'),
        ('5_ANO', '5to Año'),
        ('EGRESADO', 'Egresado/Pasante'),
        ('ESPECIALISTA', 'Especialista'),
    ]
    nivel_academico = models.CharField(
        max_length=20,
        choices=NIVEL_ACADEMICO_CHOICES,
        null=True,
        blank=True
    )

    carnet_de_estudiante = models.ImageField(upload_to='carnets_estudiante/', null=True, blank=True, help_text="Sube una imagen de tu carnet de estudiante para verificación.")
    
    # --- Biografía ---
    sobre_mi = models.TextField(null=True, blank=True)

    # --- Información de Contacto y Horarios ---
    telefono_estudiante = models.CharField(max_length=20, null=True, blank=True)
    correo_profesional = models.EmailField(max_length=255, null=True, blank=True)
    horarios_atencion = models.TextField(null=True, blank=True, help_text="Ej: Lunes a Viernes de 9am a 5pm")
    disponible_para_citas = models.BooleanField(default=True)

    # --- Campos de Diseño Original ---
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', default='fotos_perfil/default.png')
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'

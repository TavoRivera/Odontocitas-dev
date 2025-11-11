
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

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

    @property
    def es_estudiante(self):
        """
        Determina si el perfil corresponde a un estudiante activo.
        Se considera estudiante si su nivel académico está entre 1er y 5to año.
        """
        student_levels = ['1_ANO', '2_ANO', '3_ANO', '4_ANO', '5_ANO']
        return self.nivel_academico in student_levels

class Resena(models.Model):
    estudiante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='resenas')
    nombre_paciente = models.CharField(max_length=100, help_text="Tu nombre (se mostrará públicamente)")
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Puntuación de 1 a 5 estrellas."
    )
    comentario = models.TextField(help_text="Escribe tu reseña aquí.")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True, help_text="Las reseñas no activas no se mostrarán públicamente.")

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f'Reseña de {self.nombre_paciente} para {self.estudiante.user.username} - {self.puntuacion} estrellas'

@receiver(post_save, sender=Resena)
def actualizar_calificacion_promedio(sender, instance, created, **kwargs):
    """
    Actualiza la calificación promedio del perfil del estudiante cada vez que
    se crea o actualiza una reseña.
    """
    perfil_estudiante = instance.estudiante
    
    # Recalcular el promedio de las reseñas activas
    nueva_calificacion = Resena.objects.filter(estudiante=perfil_estudiante, activa=True).aggregate(
        promedio=Avg('puntuacion')
    )['promedio']

    if nueva_calificacion is not None:
        perfil_estudiante.calificacion_promedio = round(nueva_calificacion, 2)
    else:
        # Si no hay reseñas activas, se resetea a un valor por defecto (ej. 5.0)
        perfil_estudiante.calificacion_promedio = 5.00
    
    perfil_estudiante.save()

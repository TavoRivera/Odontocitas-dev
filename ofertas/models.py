from django.db import models
from django.contrib.auth.models import User

class Oferta(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

from django.contrib import admin
from .models import Perfil, Resena

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre_completo', 'nivel_academico', 'calificacion_promedio', 'disponible_para_citas')
    search_fields = ('user__username', 'nombre_completo', 'correo_profesional')
    list_filter = ('nivel_academico', 'disponible_para_citas')
    ordering = ('user__username',)

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'nombre_paciente', 'puntuacion', 'fecha_creacion', 'activa')
    list_filter = ('estudiante', 'puntuacion', 'fecha_creacion', 'activa')
    search_fields = ('estudiante__user__username', 'nombre_paciente', 'comentario')
    actions = ['aprobar_resenas']

    def aprobar_resenas(self, request, queryset):
        queryset.update(activa=True)
    aprobar_resenas.short_description = "Aprobar reseñas seleccionadas"

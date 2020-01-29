"""Administrador de los Modelos de Circulos"""

 # Django
from django.contrib import admin

# Models
from cride.circles.models import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Modelo de Administrador de Circulos"""
    list_display =(
        'slug_name','name',
        'is_public','verified',
        'is_limited',
        'members_limit'
        )
    search_fields=('slug_name','name')
    list_filter=('is_public','verified','is_limited')

    actions  = ['make_verified','make_unverified'] # Colocamos en esta variable una lista de las acciones que nosotros creamos.
    
    def make_verified(self,request,queryset):
        """Cambia círculos a verificados"""
        queryset.update(verified=True) # Actualizamos el campo de verified del query que le mandamos del modelo Circle.

    make_verified.short_description = 'Marcar circulos seleccionados a verificados' 

    def make_unverified(self,request,queryset):
        """Cambia círculos a no verificados"""
        queryset.update(verified=False)

    make_unverified.short_description = 'Marcar circulos seleccionados a no verificados' 
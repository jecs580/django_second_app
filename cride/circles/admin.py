"""Administrador de los Modelos de Circulos"""

 # Django
from django.contrib import admin

#Models
from cride.circles.models import Circle

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Modelo de Administrador de Circulos"""
    list_display =('slug_name','name','is_public','verified','is_limited','members_limit')
    search_fields=('slug_name','name')
    list_filter=('is_public','verified','is_limited')
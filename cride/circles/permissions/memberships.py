"""Clase de permisos para membresias."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership

class IsActiveCircleMember(BasePermission):
    """Permite acceso solo a miembros del círculo
    
    Espere que las vistas que implementan este permiso tengan asignado un atributo 'círculo'
    """
    def has_permission(self,request,view):
        """verifica que el usuario es un miembro activo del círculo"""
        circle=view.circle
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
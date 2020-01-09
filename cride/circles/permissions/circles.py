"""Clases de permiso de círculos."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership
class IsCircleAdmin(BasePermission):
    """Permite acceso solo a los administradores"""
    def has_object_permission(self,request,view,obj): # El obj es el objecto que ya trajo en viewset que es circulo
        """Verificar que el usuario sea miembro del obj(del circulo)"""
        try:
            Membership.objects.get(
            user=request.user,
            circle=obj,
            is_admin=True,
            is_active=True # Para evitar que unusuario este inactivo, y sea admin.
            )
        except Membership.DoesNotExist:
            return False
        return True
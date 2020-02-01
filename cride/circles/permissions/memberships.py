"""Clase de permisos para membresias."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """Permite acceso solo a miembros del círculo

    Espere que las vistas que implementan este permiso tengan asignado un atributo 'círculo'
    """
    def has_permission(self, request, view):
        """verifica que el usuario es un miembro activo del círculo"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):
    """Permite acceso solo a miembros propietarios."""
    def has_permission(self, request, view):
        """Deje que el permiso de objeto otorgue acceso"""
        obj = view.get_object()
        return self.hast_object_permission(request, view, obj)

    def hast_object_permission(self, request, view, obj):
        """permite acceso solo si el miembro solicitante es el propietario."""
        return request.user == obj.user  # Si el solicitante es la misma persona en la url

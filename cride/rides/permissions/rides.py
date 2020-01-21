"""Permisos para Viajes."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsRideOwner(BasePermission):
    """Verifica que la solicitud del usuario es sobre el viaje creado."""

    def has_object_pemission(self,request,view,obj): # El obj es de tipo ride.
        """Verifica que la solicitud del usuario sea el creador del viaje."""
        return request.user==obj.offered_by
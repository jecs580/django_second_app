"""Permisos de Usuario"""

# Django REST Framework
from rest_framework.permissions import BasePermission

class IsAccountOwner(BasePermission):
    """Permite acceso solo a los objetos propiedad del usuario solicitante"""

    def has_object_permission(self,request,view,obj):
        """Comprueba que obj y usuario son iguales"""
        return request.user == obj # El obj Se usara el objecto que se le coloca en la url, por que se aplicara en retrieve y requiere un username. 
        # -Retornara True o False, si es False no tendra permiso y si es True si tendra.
        # -Este return compara y devuelve directamente, actua como retorno y como un condicional(if)
"""Serializador de Membresias"""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.circles.models import Membership

# Serializers
from cride.users.serializers import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Serializador del modelo de Membresias."""
    
    user=UserModelSerializer(read_only=True) # Con este campo cambiamos de que solo muetre el id del usuario, a que nos muestre los datos que colocamos en el serializador, de este modo anidamos el usuario que a su vez tiene los datos de perfil
    joined_at=serializers.DateTimeField(
        source='created', # Colocamos el nombre real del campo del modelo
        read_only=True # Especificamos que solo sea de lectura para que no se pueda modificar.
    )
    invited_by=serializers.StringRelatedField() # El metodo StringRelatedField nos devuelve el valor del  metodo str que colocamos en el modelo, por defecto sin especficar este campo se mostrara el id del objecto relacionado.No especificamos que sea solo de lectura por que mas abajo lo hacemos
    class Meta:
        """Clase Meta."""
        model=Membership
        fields=(
            'user', # Esto solo nos dara un id, podriamos mejorarlo para que nos traiga los datos del perfil del miembro
            'is_admin',
            'is_active',
            'used_invitations',
            'remaining_invitations',
            'invited_by',
            'rides_taken',
            'rides_offered',
            'joined_at' # Este campo lo creamos en el serializer a partir del campo created del modelo
        )
        read_only_fields=(
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken',
            'rides_offered'
        ) # No colocamos joined_at por que al principio de la clase lo colocamos particularmente
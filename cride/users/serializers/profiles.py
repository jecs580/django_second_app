"""Serializador del Perfil"""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.users.models import Profile

class ProfileModelSerializer(serializers.ModelSerializer):
    """Serializador del modelo de perfil"""
    
    class Meta:
        """Clase meta"""
        model= Profile
        fields=(
            'picture',
            'biography',
            'rides_taken',
            'rides_offered',
            'reputation',
        ) # Los campos que queremos mostrar.
        read_only_fields=(
            'rides_taken',
            'rides_offered',
            'reputation'
        ) # Estos datos son solo de lectura, para que nadie pueda editarlos.
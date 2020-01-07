"""Serializadores de Circulos para las ViewSet"""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de Circulo"""

    class Meta:
        """Clase Meta"""
        model=Circle
        fields=(
            'id','name','slug_name',
            'about','picture','rides_offered',
            'rides_taken','is_public','is_limited',
            'members_limit'
            )

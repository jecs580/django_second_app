"""Serializadores de Circulos para las ViewSet"""

# Django REST Framework
from rest_framework import serializers

# Model
from cride.circles.models import Circle

class CircleModelSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de Circulo"""
    # Usamos estos campos opciones que pueden mandar en el request.
    members_limit=serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=3200
    ) # Cambiamos el valor del members_limit de nos proporciona a para que el numero sea 10 como minimo
    is_limited=serializers.BooleanField(
        default=False
    )

    class Meta:
        """Clase Meta"""
        model=Circle
        fields=(
            'id','name','slug_name',
            'about','picture','rides_offered',
            'rides_taken','is_public','is_limited',
            'members_limit'
            ) # Campos con los que trabajara el serializer para todas las acciones.
        read_only_fields=(
            'is_public',
            'verified',
            'rides_offered',
            'rides_taken'
        ) # Son campos que no pueden cambiar, solo podran los admin

    def validate(self,data):
        """Se asegura de que members_limit y is_limited esten presentes
        o ninguno este presente.
        """
        members_limit=data.get('members_limit',None) # Usamos get por el motivo de que no envien el dato y lo colocamos como None(ninguna)
        is_limited=data.get('is_limited',False)
        if is_limited^bool(members_limit):
            raise serializers.ValidationError('Si el círculo es limitado,debe proveer un límite de miembros')
        return data
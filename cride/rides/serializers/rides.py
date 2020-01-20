"""Serializador de Viajes"""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.rides.models import Ride
from cride.circles.models import Membership

# Utilities
from django.utils import timezone
from datetime import timedelta

class RideModelSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Ride."""

    class Meta:
        """Clase Meta."""
        model=Ride
        fields='__all__' # Proporciona todos los campos del modelo
        read_only_fields=(
            'offered_by',
            'offered_in',
            'rating'
        )

class CreateRideSerializer(serializers.ModelSerializer):
    """Serializador para crear viajes"""

    offered_by=serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats=serializers.IntegerField(min_value=1,max_value=15)

    class Meta:
        """Clase Meta."""
        model=Ride
        exclude=('offered_in','passengers','rating','is_active') # Traera todos los campos a excepcion de los que coloquemos en tupla exclude
    def validate_departure_date(self,data):
        """Verifica que fecha no haya pasado."""
        min_date=timezone.now() + timedelta(minutes=10)
        if data< min_date:
            raise serializers.ValidationError(
                'La hora de salida debe ser al menos pasando los próximos 20 minutos'
            )
        return data

    def validate(self,data):
        """Validar.
        Verifica que la persona que ofrece los viajes es miembro
         y también el mismo usuario que realiza la solicitud
        """

        if self.context['request'].user != data['offered_by']:
            raise serializers.ValidationError('No se permiten viajes ofrecidos en nombre de otros.')
        user=data['offered_by']
        circle=self.context['circle']
        try:
            membership=Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
                )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('El usuario no es un miebro activo del circulo.')
        self.context['membership']= membership
        if data['arrival_date']<= data['departure_date']:
            raise serializers.ValidationError('La fecha de llegada tiene que suceder despues de la fecha de salida.')
        return data

    def create(self,data):
        """Crea un viaje y actualiza las estadisticas."""
        circle=self.context['circle']

        ride=Ride.objects.create(**data,offered_in=circle)

        # Circle
        circle.rides_offered += 1
        circle.save()
        # Membership
        membership=self.context['membership']
        membership.rides_offered +=1
        membership.save()
        #Profile
        profile= data['offered_by'].profile
        profile.rides_offered+=1
        profile.save()
        return ride

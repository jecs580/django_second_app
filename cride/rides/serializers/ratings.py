"""Seriazador de Calificaciones."""

# Django
from django.db.models import Avg

# Django REST Framework
from rest_framework import serializers

# Models
from cride.rides.models import Rating


class CreateRideRatingSerializer(serializers.ModelSerializer):
    """Serializador de Calificaciones de Viajes."""

    rating = serializers.IntegerField(min_value=1, max_value=5)
    comments = serializers.CharField(required=False)

    class Meta:
        """Clase meta"""
        model = Rating
        fields = ('rating', 'comments')

    def validate(self, data):
        """Verifica que la califacacion no se haya emitido antes."""

        user = self.context['request'].user
        ride = self.context['ride']  # O tambien podiamos colocar self.context['view'].get_object(),
        # en caso de que no lo coloquemos al contexto
        if not ride.passengers.filter(pk=user.pk).exists():  # Vericamos que solo los pasajeros del viaje
            # puedan califcar el viaje
            raise serializers.ValidationError('El usuario no es un pasajero')

        q = Rating.objects.filter(
            circle=self.context['circle'],
            ride=ride,
            rating_user=user
        )
        if q.exists():
            raise serializers.ValidationError('¡La calificación ya ha sido emitida!')
        return data

    def create(self, data):
        """Crea Califacion."""
        offered_by = self.context['ride'].offered_by
        Rating.objects.create(
            circle=self.context['circle'],
            ride=self.context['ride'],
            rating_user=self.context['request'].user,
            rated_user=offered_by,
            **data  # Traemos los demas campos que necesita el modelo desde los datos que son enviados por la vista.
        )

        # Promedio de las calificaciones de un viaje
        ride_avg = round(
            Rating.objects.filter(
                circle=self.context['circle'],
                ride=self.context['ride']
            ).aggregate(Avg('rating'))['rating__avg'],  # Sacamos el promedio y guardamos el valor de la
            # llave  rating_avg que es el promedio.
            1  # Nro de decimales que tomara
        )

        self.context['ride'].rating = ride_avg
        self.context['ride'].save()

        user_avg = round(
            Rating.objects.filter(
                rated_user=offered_by
            ).aggregate(Avg('rating'))['rating__avg'],
            1
        )
        offered_by.profile.reputation = user_avg
        offered_by.profile.save()
        return self.context['ride']

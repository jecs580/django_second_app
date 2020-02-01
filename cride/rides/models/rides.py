""" Modelo de Viajes """

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Ride(CRideModel):
    """Modelo de Viajes"""

    offered_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)  # Quien lo ofrece
    offered_in = models.ForeignKey('circles.Circle', on_delete=models.SET_NULL, null=True)  # En que circulo es ofrecido

    passengers = models.ManyToManyField('users.User', related_name='pasajeros')  # Pasajeros de los viajes

    available_seats = models.PositiveSmallIntegerField(default=1)  # Asientos disponibles.
    comments = models.TextField(blank=True)  # Comentarios

    departure_location = models.CharField(max_length=255)  # Lugar de Partida
    departure_date = models.DateTimeField()  # Fecha y hora de la Partida
    arrival_location = models.CharField(max_length=255)  # Lugar de llegada
    arrival_date = models.DateTimeField()  # Fecha y hora de llegada

    rating = models.FloatField(null=True)  # Calificacion del viaje, por defecto no tendra calificacion hasta
    # realizar el viaje

    is_active = models.BooleanField(
        'estado de activo',
        default=True,
        help_text='Se usa para deshabilitar el viaje o marcarlo como terminado'
    )

    def __str__(self):
        return '{_from} a {to} | {day} {i_time} - {f_time}'.format(
            _from=self.departure_location,
            to=self.arrival_location,
            day=self.departure_date.strftime('%a %d , %b'),  # Retornamos el dia de la semana, el numero
            # del mes, y el mes.
            i_time=self.departure_date.strftime('%I:%M %p'),  # Hora de partida en formato AM/PM
            f_time=self.arrival_date.strftime('%I:%M %p')  # Hora de llegada en formato AM/PM
        )

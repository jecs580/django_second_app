"""Modelo de Calificaciones"""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Rating(CRideModel):
    """Calificacion de Viajes.

    Los Rates son entidades que almacenan la calificación
    de un usuario dado a un viaje, varía de 1 a 5 y afecta
    la reputación general del usuario.
    """

    ride = models.ForeignKey(
        'rides.Ride',
        on_delete=models.CASCADE,  # Si se borra el viaje se borraran los datos relacionados con Rating.
        related_name='paseo_calificado'
    )
    circle = models.ForeignKey(
        'circles.Circle',
        on_delete=models.CASCADE,  # Si se borra el circulo se borraran los datos relacionados con Rating.
    )

    # Estos 2 valores son nulos porque existe la posibilidad que no se califiquen los viajes ni a los usuarios.
    # Calificacion por Usuario
    rating_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text='Usuarios que emiten la calificacion',
        related_name='calificacion_usuario'
    )

    # Usuario Calificado
    rated_user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        help_text='Usuario que recibe la calificacion',
        related_name='usuario_calificado'
    )

    comments = models.TextField(blank=True)
    rating = models.IntegerField(default=1)

    def __str__(self):
        return '@{} califico {} a @{}'.format(
            self.rating_user.username,
            self.rating,
            self.rated_user.username  # Como el campo es de tipo User podemos devolver los atributos de ese objeto.
        )

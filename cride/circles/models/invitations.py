"""Modelo de invitacion de ciculo"""

# Django REST Framework
from django.db import models

# Utilities
from cride.utils.models import CRideModel

# Manager
from cride.circles.managers import InvitationManager


# Una vez ejecutado el test, django destruira la base de datos de prueba.
class Invitation(CRideModel, models.Model):
    """Invitacion de Circulo

    Una invitación de círculo es un texto aleatorio que actúa
    como un código único que otorga acceso a un círculo específico.
    Estos códigos son generados por usuarios que ya son miembros del
    círculo y tienen un valor de "remaining_invitations" mayor que 0
    """
    code = models.CharField(max_length=50, unique=True)  # Codigo que se generara con la clase Manager.
    issued_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='Miembro del círculo que proporciona la invitación',
        related_name='emitido_por'
    )  # Quien hizo la hizo la invitacion
    used_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,  # Una invitacion puede ser usada o no por un usuario
        help_text='Usuario que usó el código para ingresar al círculo'
    )  # El usuario que invitado y que uso el codigo
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)  # Si la invitacion fue usada. Con la ayuda de used_by
    used_at = models.DateTimeField(blank=True, null=True)  # La fecha en que se uso el codigo, colocamos
    # nulos por que puede hacer invitaciones sin usarse.

    # Manager
    objects = InvitationManager()  # Redefinimos el manager en la variable por defecto object.

    def __str__(self):
        """Retorna el codigo y el circulo."""
        return '#{}: {}'.format(self.circle.slug_name, self.code)

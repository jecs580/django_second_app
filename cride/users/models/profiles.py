""""Modelo de Perfil"""

# Django
from django.db import models

# Utilidades
from cride.utils.models import CRideModel

class Profile(CRideModel):
    """Modelo de Perfil
    Un perfil contiene datos públicos de un usuario, como biografía, imagen y estadísticas.
    """
    user=models.OneToOneField('users.User',on_delete=models.CASCADE) # Si users se elimina, se elimina profile
    picture=models.ImageField(
        'foto de perfil',
        upload_to='users/pictures/', # indica la ruta donde se cargaran las imagenes de perfil
        blank=True, null=True
    )
    biography=models.TextField(max_length=500,blank=True)

    # Estadisticas
    rides_taken=models.PositiveIntegerField(default=0)
    rides_offered=models.PositiveIntegerField(default=0)
    reputation=models.FloatField(
        default=5.0, # Un usuario sin ninguna calificacion tiene la mejor reputacion
        help_text='Reputación del usuario basada en los viajes realizados y ofrecidos'
    )

    def __str__(self):
        """Retorna la representacion en string que se coloco en el model User creado """
        return str(self.user) # Si estas usando el modelo User que trae por defecto debes retornar el nombre del campo que quieres ya que por defecto el modelo User no trae el str.


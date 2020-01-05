"""Modelo de Membresias para usuarios con circulos"""

# Django REST Framework
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Membership(CRideModel,models.Model):
    """Modelo de Membresias
    
        Una membresía es la tabla que mantiene la relación entre un usuario y un círculo.
    """
    user = models.ForeignKey('users.User',on_delete=models.CASCADE) # Relacionamos con el usuario simplemente llamando al archivo y su clase, no tenemos que colocar la ruta donde se encuentra.
    profile = models.ForeignKey('users.Profile',on_delete=models.CASCADE)
    # Podriamos usar solo Profile puesto que un profile esta relacionado con un usuario, pero para hacer accesible los datos, colocamos cada relacion.
    circle =models.ForeignKey('circles.Circle',on_delete=models.CASCADE) # Esta relacion si es necesario para crear el modelo muchos a muchos

    is_admin=models.BooleanField(
        'Administrador de Circulo',
        default=False,
        help_text="Los administradores de los círculos pueden actualizar los datos de los círculos y administrar sus miembros") # Este campo indica si el miembro del circulo es administrador. Un administrador puede borrar, editar a los miembros del circulo.

    # Invitaciones

    # El campo PositiveSmallIngeterField al igual que el PositiveIngeter acepta valores enteros positivos, pero este posee un menor rango.
    used_invitations=models.PositiveSmallIntegerField('invitaciones usadas',default=0) # Son las invitaciones que que uso un miebro para invitar a otra perfiles
    remaining_invitations=models.PositiveSmallIntegerField('invitaciones sobrantes',default=0) # Son las invitaciones que le quedan para invitar.
    invited_by=models.ForeignKey(
        'users.User',
        null=True, # Este campo es True para el caso en que el usuario haya creado el circulo
        on_delete=models.SET_NULL, # Cambiamos la forma del on_delete, por que queremos que cuando el que te invito, se elimine, el invitado no se borre.
        related_name='invited_by', # Este atributo se lo usa normalmente cuando tienes 2 campos que relacionen a un mismo modelo, en ese caso a User, por lo tanto que queremos que en la base de datos se cree una la relacion con el nuevo nombre "invited_by"
        )
        # Statistics
    rides_taken=models.PositiveIntegerField('Viajes tomados',default=0) # Indica cuantos viajes tomo dentro del circulo un miembro
    rides_offered=models.PositiveIntegerField('Viajes ofrecidos',default=0) # Indica cuantos viajes a ofrecido dentro del circulo

    # Estados
    # Usamos este campo para no tener que borar un miembro y perder los datos que nos podria servirnos para analiticas en un futuro.
    is_active=models.BooleanField(
        'Estado de activo',
        default=True,
        help_text="solo los usuarios activos pueden interactuar en los círculos"
    ) 
    def __str__(self):
        """Retorna un username y su circulo"""
        return '@{} en #{}'.format(self.user.username,self.circle.slug_name)



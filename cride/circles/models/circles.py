"""Modelo de Circulos"""

#Django
from django.db import models

#Utilitis
from cride.utils.models import CRideModel

class Circle(CRideModel):
    """Modelo de Circulos
    
    Un círculo es un grupo privado donde los viajes son ofrecidos y llevados por sus miembros. Para unirse a
    un círculo, un usuario debe recibir un código de invasión único de un miembro del círculo existente
    """
    name = models.CharField('Nombre del Circulo',max_length=140)
    slug_name=models.SlugField(unique=True,) # Slug es como un identificador para modelos que no sean de personas. En el modelo de personas o User el slug es el username
    about= models.CharField('Descripcion del Circulo', max_length=255)
    picture=models.ImageField(upload_to='circles/pictures',blank=True, null=True)

    #Estidisticas
    rides_offered=models.PositiveIntegerField(default=0)
    rides_taken=models.PositiveIntegerField(default=0)
    
    verified=models.BooleanField(
        'Verificacion de Circulo', # Esto permite sabes si el ciculo es oficial
        default=False,
        help_text='Los círculos verificados también se conocen como comunidades oficiales.')
    is_public=models.BooleanField(default=True,
        help_text= 'Los círculos públicos se enumeran en la página principal para que todos sepan sobre su existencia.'    
    )
    is_limited=models.BooleanField(
        'Limitado',
        default=False,
        help_text='Los círculos limitados pueden crecer hasta un número fijo de miembros.')
    members_limit=models.PositiveIntegerField(default=0,
        help_text='Si el círculo es limitado, este será el límite en el número de miembros.'
        )

    def __str__(self):
        """Retorna el nombre de Circulo"""
        return  self.name

    class Meta(CRideModel.Meta):
        """"Clase Meta"""
        ordering=['-rides_taken','-rides_offered']

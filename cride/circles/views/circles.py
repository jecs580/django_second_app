"""Vista de Circulos usando ViewSets."""

# Django REST Framework
from rest_framework import viewsets

# Models
from cride.circles.models import Circle # Esta llamada es de la forma de modulo, todos los archivo dentro del folder funcionan como uno. Y asi solo podemos llamarlo por su clase.

# Serializers
from cride.circles.serializers import CircleModelSerializer
class CircleViewSet(viewsets.ModelViewSet): # El modelViewSet incluye las acciones de listar,crear,recuperar, actualizar,actualizacion parcial y eliminar objetos,hereda de GenericAPIView.
    """Conjunto de vistas de Circulos"""
    queryset=Circle.objects.all() # Datos que usara.
    serializer_class= CircleModelSerializer

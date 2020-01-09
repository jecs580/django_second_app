"""Vista de Circulos usando ViewSets."""

# Django REST Framework
from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated

# Permissions
from cride.circles.permissions.circles import IsCircleAdmin

# Models
from cride.circles.models import Circle,Membership # Esta llamada es de la forma de modulo, todos los archivo dentro del folder funcionan como uno. Y asi solo podemos llamarlo por su clase.

# Serializers
from cride.circles.serializers import CircleModelSerializer

# class CircleViewSet(viewsets.ModelViewSet): # El modelViewSet incluye las acciones de listar,crear,recuperar, actualizar,actualizacion parcial y eliminar objetos,hereda de GenericAPIView.
class CircleViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet): # Usamos las clases que hereda ModelViewSet, con la ecepcion del destroy, con esto, nadie podra borar un circulo
    """Conjunto de vistas de Circulos"""

    #queryset=Circle.objects.all()   # Datos que usara. Esto solo se coloca si no reescribes el metodo "get_queryset"
    serializer_class= CircleModelSerializer
    # permission_classes=([IsAuthenticated]) Antes de usar get_permissions

    def get_queryset(self):
        """Restringe la lista a solo públicos"""
        queryset=Circle.objects.all() # Traemos todos los datos de circles
        if self.action=='list':
            return queryset.filter(is_public=True) # Adicionamos un filtro mas para, mostrar solo los publicos
        return queryset # Retorna todo el query si la accion no es list. Esto se usara para las demas acciones como update,retrieve,etc.
    
    def get_permissions(self):
        """Asigna permisos en función de la acción."""
        permissions=[IsAuthenticated]
        if self.action in ['update','partial_update']:
            permissions.append(IsCircleAdmin) # En caso de que un usuario quiera actualizar un circulo debe ser admin del circulo
        return [permission() for permission in permissions]

    def perform_create(self,serializer):
        """Asigna un admin de circulo al que crea el circulo"""
        circle=serializer.save()
        user=self.request.user # Usamos el user que viene de request una vez que se loguee.
        profile=user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True, # Le colocamos que es administrador del circle
            remaining_invitations=10 # Como admin le asignamos mas invitaciones.
        )
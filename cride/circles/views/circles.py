"""Vista de Circulos usando ViewSets."""

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Permissions
from cride.circles.permissions.circles import IsCircleAdmin

# Models
from cride.circles.models import Circle, Membership  # Esta llamada es de la forma de modulo, todos los
# archivo dentro del folder funcionan como uno. Y asi solo podemos llamarlo por su clase.

# Serializers
from cride.circles.serializers import CircleModelSerializer

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


# class CircleViewSet(viewsets.ModelViewSet): # El modelViewSet incluye las acciones de listar,crear,
# recuperar, actualizar,actualizacion parcial y eliminar objetos,hereda de GenericAPIView.
class CircleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):  # Usamos las clases que hereda ModelViewSet, con la ecepcion
    # del destroy, con esto, nadie podra borar un circulo
    """Conjunto de vistas de Circulos"""

    # queryset=Circle.objects.all()   # Datos que usara. Esto solo se coloca si no reescribes el metodo
    #  "get_queryset"
    serializer_class = CircleModelSerializer
    # permission_classes=([IsAuthenticated]) Antes de usar get_permissions
    lookup_field = 'slug_name'  # Variable para especificar las busquedas, actualizaciones y eliminar objetos.
    # Si no definimos esta variable,por defecto se colocara con el campo pk.

    # Filters.- Estos filtros se aplican despues del filtro que colocamos en el modelo

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]  # Habilitamos los tipos de filtros
    # que tendrá nuestra vista.
    search_fields = ('slug_name', 'name')  # Campos por los que hara la busqueda.En la url colocamos la cadena
    # a buscar, de esta manera los buscara por cada campo hasta encotrar resultados, si no encuentra ninguno.
    #  no devolvera nada.
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'members_limit')  # Campos por los
    # que se podra orderan, en la url colocamos el nombre del campo que deseas que se ordene.
    #  Por defecto si solo colocamos el nombre lo ordenara de manera descendente (A-Z), siquieres
    #  que sea de manera descendente(Z-A) se debe colocar el signo menos antes del campo a buscar en la url
    ordering = (
        '-members__count',  # Podemos ordenar usando querys, para scar el nro de miembros y mostrarlos
        # desde el que tenga mas hasta el q tenga menos miembros.
        '-rides_offered',
        '-rides_taken'
        )

    # Usando DjangoFilters
    filter_fields = ('verified', 'is_limited')  # Colocamos campos que contengan un valor especifico.
    # La diferencia con seach_fields es que como llave colocamos el campo a buscar.Algo que mencionar es que
    # los campos Booleanos podemos buscarlos con True - False o 1 - 0

    def get_queryset(self):
        """Restringe la lista a solo públicos"""
        queryset = Circle.objects.all()  # Traemos todos los datos de circles
        if self.action == 'list':
            return queryset.filter(is_public=True)  # Adicionamos un filtro mas para, mostrar solo los
            # publicos
        return queryset  # Retorna todo el query si la accion no es list. Esto se usara para las demas
        # acciones como update,retrieve,etc.

    def get_permissions(self):
        """Asigna permisos en función de la acción."""
        permissions = [IsAuthenticated]  # No colocamos comillas por que es una clase que se coloca.
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)  # En caso de que un usuario quiera actualizar un circulo debe
            # ser admin del circulo
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Asigna un admin de circulo al que crea el circulo"""
        circle = serializer.save()
        user = self.request.user  # Usamos el user que viene de request una vez que se loguee.
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,  # Le colocamos que es administrador del circle
            remaining_invitations=10  # Como admin le asignamos mas invitaciones.
        )

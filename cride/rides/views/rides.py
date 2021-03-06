""" Vista de Viajes"""

# Django REST Framework
from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Serializers
from cride.rides.serializers import (
    CreateRideSerializer,
    RideModelSerializer,
    JoinRideSerializer,
    EndRideSerializer,
    CreateRideRatingSerializer,
)

# Models
from cride.circles.models import Circle

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner, IsNotRideOwner

# Utilities
from django.utils import timezone
from datetime import timedelta


class RideViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet
                  ):

    """Conjunto de vistas para Viajes"""

    # serializer_class = CreateRideSerializer # Este serializador era para todas las acciones. Pero queremos
    #  tener para cada accion un serializador diferente.
    # permission_classes = [IsAuthenticated, IsActiveCircleMember] # Permiso cuando no sobre-escribimos el
    #  metodo get_permissions.
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('departure_date', 'arrival_date', 'available_seats')  # La manera en como estara ordena
    # inicialmente, si quieres cambiarlo se usa el ordering_fields
    ordering_fields = ('departure_date', 'arriva_date', 'available_seats')  # Campos por los que se podra
    # ordenar, debemos mandar en la peticion el campo y el orden ascendente o descendente con el signo menos
    # encaso de que sea descente.
    search_fields = ('departure_location', 'arrival_location')  # Campos por los que se podra hacer busquedas,
    # debemos mandarle el valor del campo

    def dispatch(self, request, *args, **kwargs):
        """Verifica que exista el circulo."""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Asigna permisos basados en la accion que realicen."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update', 'finish']:
            permissions.append(IsRideOwner)
        if self.action == 'join':
            permissions.append(IsNotRideOwner)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """Agrega circle al contexto de serializador."""
        context = super(RideViewSet, self).get_serializer_context()  # Traemos los datos del metodo original.
        context['circle'] = self.circle  # Añadimos al contexto el objecto circulo
        return context
    # TODO mandar un pullrequest para el accion de actualizar y join

    def get_serializer_class(self):
        """Retorna un serializador basado en la action."""
        if self.action == 'create':
            return CreateRideSerializer
        if self.action in ['update', 'join']:
            return JoinRideSerializer
        if self.action == 'finish':
            return EndRideSerializer
        if self.action == 'rate':
            return CreateRideRatingSerializer
        return RideModelSerializer

    def get_queryset(self):
        """Retorna los viajes del círculo activo."""
        if self.action != 'finish':
            set_value = timezone.now()+timedelta(minutes=10)  # Colocamos una fecha desde la fecha actual+ 10 min
            # para que devuelve los viajes que empiezen en esa hora.
            return self.circle.ride_set.filter(  # Traemos los viajes del circulo que es enviado en la URL
                departure_date__gte=set_value,  # Query que trae las fechas que sean mayor o igual(__gte) a algo
                is_active=True,
                available_seats__gte=1
            )
        return self.circle.ride_set.all()  # Cuando la accion es finish, traemos todos los viajes que
        # se crearon del circulo

    @action(detail=True, methods=['post'])  # Es de detalle por que a travez de un vieje especifico
    # se ejutara una logica.
    def join(self, request, *args, **kwargs):
        """Añade usuario solicitante para viajar."""
        ride = self.get_object()  # Traemos al ride(viaje) que se coloco en la url.
        # TODO usar el metodo get_serializer_class. --Ya se corrigio
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={'passenger': request.user.pk},  # Enviamos el id del objeto User.
            context={'ride': ride, 'circle': self.circle},  # Eliminamos los datos que ya venian en el context.¿?
            partial=True
        )
        serializer.is_valid(raise_exception=True)  # Valida los campos que son Enviamos y devueltos
        # verificando su validez, en caso que no sea validos. Al colocar raise_exception=True esto mostrara
        # al cliente los errores que ocurrieron. Desde datos Json.
        ride = serializer.save()
        data = RideModelSerializer(ride).data  # Mostraramos de nuevo los datos del viaje
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        """Llama a los propietarios para terminar un viaje."""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={'is_active': False, 'current_time': timezone.now()},  # Traemos la fecha actual en la envia el post.
            context=self.get_serializer_context(),
            partial=True  # Cuando mandamos partial= True logramos solo actualizar campos especificos del
            # modelos, por otro lado tambien podemos enviar otros tipos de datos, pero solo tomara los que
            # estan en el modelos(is_active). Y los actualizara al instancia de ride que enviamos tambien.
        )
        serializer.is_valid(raise_exception=True)  # Valida los campos que son Enviamos y devueltos
        # verificando su validez, en caso que no sea validos. Al colocar raise_exception=True esto mostrara
        # al cliente los errores que ocurrieron. Desde datos Json.
        ride = serializer.save()
        data = RideModelSerializer(ride).data  # Mostraramos de nuevo los datos del viaje
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def rate(self, request, *args, **kwargs):
        """Califacion de viaje."""
        ride = self.get_object()
        context = self.get_serializer_context()
        context['ride'] = ride
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_201_CREATED)

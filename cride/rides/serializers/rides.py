"""Serializador de Viajes"""

# Django REST Framework
from rest_framework import serializers

# Models
from cride.rides.models import Ride
from cride.circles.models import Membership
from cride.users.models import User

# Utilities
from django.utils import timezone
from datetime import timedelta

# Serializers
from cride.users.serializers import UserModelSerializer
 

class RideModelSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Ride."""
    offered_by=UserModelSerializer(read_only=True)
    offered_in=serializers.StringRelatedField()
    passengers=UserModelSerializer(read_only=True,many=True)

    class Meta:
        """Clase Meta."""
        model=Ride
        fields='__all__' # Proporciona todos los campos del modelo
        read_only_fields=(
            'offered_by',
            'offered_in',
            'rating'
        )
    def update(self,instance,data): # El campo data en la documentacion esta como validate_data, pero podemos llamarlo como querramos.
        """Permite actualizaciones solo antes de la fecha de salida."""
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError("Los viajes en curso no se pueden modificar.")
        return super(RideModelSerializer,self).update(instance,data)

class CreateRideSerializer(serializers.ModelSerializer):
    """Serializador para crear viajes"""

    offered_by=serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats=serializers.IntegerField(min_value=1,max_value=15)

    class Meta:
        """Clase Meta."""
        model=Ride
        exclude=('offered_in','passengers','rating','is_active') # Traera todos los campos a excepcion de los que coloquemos en tupla exclude
    def validate_departure_date(self,data):
        """Verifica que fecha no haya pasado."""
        min_date=timezone.now() + timedelta(minutes=10)
        if data< min_date:
            raise serializers.ValidationError(
                'La hora de salida debe ser al menos pasando los próximos 20 minutos'
            )
        return data

    def validate(self,data):
        """Validar.
        Verifica que la persona que ofrece los viajes es miembro
         y también el mismo usuario que realiza la solicitud
        """

        if self.context['request'].user != data['offered_by']: # Verificamos que el usuario pasado en el contexto dentro de request sea igual a la persona que trae por defecto igualmente desde el request¿?.  
            raise serializers.ValidationError('No se permiten viajes ofrecidos en nombre de otros.')
        user=data['offered_by']
        circle=self.context['circle']
        try:
            membership=Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
                )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('El usuario no es un miembro activo del circulo.')
        self.context['membership']= membership
        if data['arrival_date']<= data['departure_date']:
            raise serializers.ValidationError('La fecha de llegada tiene que suceder despues de la fecha de salida.')
        return data

    def create(self,data):
        """Crea un viaje y actualiza las estadisticas."""
        circle=self.context['circle']

        ride=Ride.objects.create(**data,offered_in=circle)

        # Circle
        circle.rides_offered += 1
        circle.save()
        # Membership
        membership=self.context['membership']
        membership.rides_offered +=1
        membership.save()
        #Profile
        profile= data['offered_by'].profile
        profile.rides_offered+=1
        profile.save()
        return ride
class JoinRideSerializer(serializers.ModelSerializer):
    """Serializador para unirse a viajes."""

    passenger = serializers.IntegerField()

    class Meta:
        """Clase Meta."""
        model=Ride
        fields=('passenger',)

    def validate_passenger(self,data):
        """Verifica que el pasajero existe y es miembro del circulo."""
        try:
            user=User.objects.get(pk=data)
        except User.DoesNotExist:
            raise serializers.ValidationError('Pasajero erroneo.')
        circle=self.context['circle']
        try:
            membership=Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
                )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('El usuario no es un miembro activo del circulo.')
        # Si quieres validar que exista un objecto lo podemos hacer de 2 formas una usando un try/expept con el query 'get' En la exception mandamos el <nombre modelo>.DoesNotExist: como tipo de exception. La otra es usando un if con el query filter y verificamos si existen los datos con el 'exists'.
        self.context['user']=user # Colocamos en el contexto el objeto user validado.
        self.context['member']=membership
        return data
    
    def validate(self,data):
        """Verifica que los viajes permitan nuevos pasajeros."""
        ride=self.context['ride']
        if ride.departure_date <= timezone.now():
            raise serializers.ValidationError("No puedes unirte a este paseo ahora.")
        if ride.available_seats < 1:
            raise serializers.ValidationError("¡El viaje ya está lleno!")
        if ride.passengers.filter(pk=self.context['user'].pk).exists():
            raise serializers.ValidationError('El pasajero ya está en este viaje.')
        return data

    def update(self,instance,data):
        """Agrega pasajeros al viaje y actualiza las estadísticas."""
        ride=self.context['ride']
        user=self.context['user']

        ride.passengers.add(user) # Agregamos a nuestro campo Relacionado el pasajero

        # Profile
        profile=user.profile
        profile.rides_taken+=1
        profile.save() # Actualizamos los datos del perfil y lo guardamos

        # Membership
        member=self.context['member']
        member.rides_taken+=1
        member.save()

        # Circle
        circle=self.context['circle']
        circle.rides_taken+=1
        circle.save()
        return ride
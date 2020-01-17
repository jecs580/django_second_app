"""Serializador de Membresias"""
 # Django
from django.utils import timezone

# Django REST Framework
from rest_framework import serializers

# Models
from cride.circles.models import Membership, Invitation

# Serializers
from cride.users.serializers import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Serializador del modelo de Membresias."""
    
    user=UserModelSerializer(read_only=True) # Con este campo cambiamos de que solo muetre el id del usuario, a que nos muestre los datos que colocamos en el serializador, de este modo anidamos el usuario que a su vez tiene los datos de perfil
    joined_at=serializers.DateTimeField(
        source='created', # Colocamos el nombre real del campo del modelo
        read_only=True # Especificamos que solo sea de lectura para que no se pueda modificar.
    )
    invited_by=serializers.StringRelatedField() # El metodo StringRelatedField nos devuelve el valor del  metodo str que colocamos en el modelo, por defecto sin especficar este campo se mostrara el id del objecto relacionado.No especificamos que sea solo de lectura por que mas abajo lo hacemos
    class Meta:
        """Clase Meta."""
        model=Membership
        fields=(
            'user', # Esto solo nos dara un id, podriamos mejorarlo para que nos traiga los datos del perfil del miembro
            'is_admin',
            'is_active',
            'used_invitations',
            'remaining_invitations',
            'invited_by',
            'rides_taken',
            'rides_offered',
            'joined_at' # Este campo lo creamos en el serializer a partir del campo created del modelo
        )
        read_only_fields=(
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken',
            'rides_offered'
        ) # No colocamos joined_at por que al principio de la clase lo colocamos particularmente

class AddMemberSerializer(serializers.Serializer):
    """Añade miembro serializado.
    
    Manejar la adición de un nuevo miembro a un círculo.
    El objeto circulo debe proporcionarse en el contexto
    """

    invitation_code  =serializers.CharField(min_length=8)
    user=serializers.HiddenField(default=serializers.CurrentUserDefault()) # Campo que no se valida en la entrada de usuario, solo se valida de manera interna, ademas podemos agragar un valor por defecto . Este dato es traido gracias que le mandamos el 'request':request(el valor de la llave debe ser exactamente request de otro modo saldra error. ), de esta forma podra obtener mas informacion

     # Validaciones por campo
    def validate_user(self,data):
        """Verifique que el usuario no sea miembro."""

        circle=self.context['circle'] # Asignamos el valor que enviamos en el contexto.
        user=data # data ya es una instancia del objecto User. que fue causada al darle el CurrentDefault()
        # Ademas no colocamos data['user'] por que la validacion solo trae el user por usar validaciones por objeto.
        q=Membership.objects.filter(
            circle=circle,
            user=user
        )
        if q.exists():
            raise serializers.ValidatorError('El usuario ya es miembro de este circulo')
        return data
    def validate_invitation_code(self,data):
        """Verifica que el código exista y que está relacionado con el círculo."""
        try:
            invitation =Invitation.objects.get(
                code=data,
                circle=self.context['circle'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Codigo de invitacion invalido')    
        self.context['invitation']= invitation # Agregamos a nuetro contexto la invitacion valida con todos sus campos. Podriamos seguir usando invitation_code pero no sabemos si es valida, para asegurar esto lo agregamos al contexto.
        return data
    
    # Validacion general
    def validate(self,data):
        """ Verifica si el círculo es capaz de aceptar un nuevo miembro."""
        circle=self.context['circle']
        if circle.is_limited  and circle.members.count() >= circle.members_limit:  # Si el circulo es limitado y el numero de miembros es mayor o igual al numero limite de miembros ya exedio el limite.
            raise serializers.ValidationError('EL circulo ha alcanzado su limite de miembros :`()')
        return data

    def create(self,data):
        """Crea un nuevo miembro del circulo."""
        circle=self.context['circle']
        invitation= self.context['invitation']
        user=data['user']

        now=timezone.now()
        
        # Creacion del Miembro
        member=Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            invited_by=invitation.issued_by # Traemos al miebro quien lo invito por medio del objeto invitation
        )

        # Uddate Invitation
        invitation.used_by=user
        invitation.used=True
        invitation.used_at=now
        invitation.save()

        # Update issuer data
        issuer =Membership.objects.get(user=invitation.issued_by,circle=circle)
        issuer.used_invitations +=1 # Actualizamos los datos de invitaciones usadas sumandolas +1 cada vez que se use sus invitaciones de la persona que lo invito
        issuer.remaining_invitations -=1 # Decrementamos el numero de invitaciones que tiene la persona que lo invito
        issuer.save()
        return member

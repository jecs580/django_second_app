"""Vistas de miembros del círculo"""

# Django REST Framework
from rest_framework import mixins, viewsets,status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from cride.circles.models import Circle,Membership,Invitation


# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember, IsSelfMember

# Serializers
from cride.circles.serializers import MembershipModelSerializer,AddMemberSerializer

class MembershipViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    """Conjunto de vistas de miembros de círculo."""
    serializer_class=MembershipModelSerializer
    def dispatch(self,request,*args,**kwargs):
        """Verifica que exista el circulo."""

        slug_name=kwargs['slug_name'] # Es el nombre de la llave que mandamos en la url

        # Creamos una nueva variable para obtener el circulo requerido
        self.circle=get_object_or_404(
            Circle,
            slug_name=slug_name
        ) # Esto es equivalente a usar: 
        # try: Circle.objects.get(slug_name=slug_name)
        # exception: Circle.DoesNotExist:
        #   Http404("<algun mensaje>") # Con la diferencia de que con este metodo podremos personalizar el raise que se envia.
        return super(MembershipViewSet,self).dispatch(request,*args,**kwargs) # Dejamos que se ejecute en metodo dispath por defecto y lo retornamos ambos.
        # Ahora cada que se ejecute esta clase que sea instanciada hara primeramente la verificacion del circulo
    def get_permissions(self):
        """Asigna permisos basados en la accion"""
        permissions=[IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActiveCircleMember)
        if self.action=='invitations':
            permissions.append(IsSelfMember)
        return [p() for p in permissions]
    def get_queryset(self):
        """Returna los miembros del circulo"""

        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )

    def get_object(self):
        """Retorna el miembro del círculo utilizando el nombre de usuario del usuario"""
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'], # Obtenemos el valor de username atravez de la url que enviemos desde un cliente la llave es pk por que para mixin se obtiene un objeto con identificado, pero como el username tambien funciona como indentificador, lo cambiamos, pero el el nombre de la llave es la misma
            circle=self.circle,
            is_active=True
        )
    
    def perform_destroy(self,instance):
        """Desabilita la membresia"""
        instance.is_active=False # En vez de eliminar al miembro simplemente colocamos el campo is_active a False para que las demas vistas esten bloqueeadas por no tener el permiso.
        instance.save()

    @action(detail=True,methods=['get'])
    def invitations(self,request,*args,**kwargs):
        """Recuperar el desglose de invitaciones de un miembro
        
        Devolverá una lista que contiene todos los miembros 
        que han usado sus invitaciones y otra lista que contiene 
        las invitaciones que aún no se han usado.
        """
        member=self.get_object() # Obtenemos el objeto de detalle (el miembro)
        invited_members=Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True
        ) # Trae a los miembro que fueron invitados por el usuario colocado en la url
        
        unsed_invitations=Invitation.objects.filter(
            circle=self.circle,
            issued_by=request.user,
            used=False,

        ).values_list('code') # Invitaciones no utilizadas.Colocamos values_list('code') para que nos lista solo los valores de codigo. Esta lista es un poco rara.

        diff=member.remaining_invitations-len(unsed_invitations) # Sacamos la difencia del numero invitaciones que le quedan por usar, contra las invitaciones que envio pero no son usadas. Esto es para generar el codigo de invitaciones. por que por defecto seran el numero maximo.
        invitations=[x[0] for x in unsed_invitations] # La lista que nos devolvia el unsed_invitations tenian de elementos tuplas. Pero no nosotros solo queremos los codigos, entonces recoremos la lista y la llenamos en otra pero con los los elemento de la tupla.
        for i in range(0,diff): # recorre el for mietras diff sea mayor a cero. En otras palabras si ya gasto todas sus invitaciones restantes y tiene las invitaciones no son usadas no entrara al for.
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    circle=self.circle
                ).code # Solo devolvemos el codigo para que se pueda agregar a la lista de strings.
            )
            # Este for solo se activara cuando la primera vez que consulte, y cuando se le aumenten un numero de ivitaciones.
        data={
            'used_invitations': MembershipModelSerializer(invited_members,many=True).data,
            'invitations':invitations
        }
        return Response(data)

    def create(self,request,*args,**kwargs):
        """Maneja la creación de miembros desde el código de invitación."""
        serializer=AddMemberSerializer(
            data=request.data, # Cambiamos los datos recibidos(Json) a un diccionario
            context={'circle':self.circle,'request':request} # Los serializers tabien pueden recibir otros datos ademas de la data, para esto usamos la variable context, mandamos request para que el serializer pueda saber el usuario de la peticion.
        )
        serializer.is_valid(raise_exception=True)
        member=serializer.save()
        data=self.get_serializer(member).data # No usamos el serializer AddMemberSerializer. Si no el serializador que se coloco en la variable serializer_class puesto que ya esta personalizado para mostrar con mas detalle
        return Response(data, status=status.HTTP_201_CREATED)
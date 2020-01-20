""" Vista de Viajes"""

# Django REST Framework
from rest_framework import mixins,viewsets
from rest_framework.generics import get_object_or_404

# Serializers
from cride.rides.serializers import CreateRideSerializer

# Models
from cride.circles.models import Circle

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

class RideViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """Conjunto de vistas para Viajes"""

    serializer_class=CreateRideSerializer
    permissions_clasess=[IsAuthenticated,IsActiveCircleMember]

    def dispatch(self,request,*args,**kwargs):
        """Verifica que exista el circulo."""
        slug_name=kwargs['slug_name'] 
        self.circle=get_object_or_404(Circle,slug_name=slug_name)
        return super(RideViewSet,self).dispatch(request,*args,**kwargs)
    
    def get_serializer_context(self):
        """Agrega circle al contexto de serializador."""
        context= super(RideViewSet,self).get_serializer_context() # Traemos los datos del metodo original.
        context['circle']=self.circle # Añadimos al contexto el objecto circulo
        return context

    
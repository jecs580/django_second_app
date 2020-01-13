"""Vistas de miembros del círculo"""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Models
from cride.circles.models import Circle
from cride.circles.models import Membership
# Serializers
from cride.circles.serializers import MembershipModelSerializer

class MembershipViewSet(
    mixins.ListModelMixin,
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

    def get_queryset(self):
        """Returna los miembros del circulo"""

        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )
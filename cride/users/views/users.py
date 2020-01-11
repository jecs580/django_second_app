"""Vista de Usuarios"""

# Django REST Framework
from rest_framework import status,viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
# Serializers
from cride.users.serializers import (UserLoginSerializer,
                                    UserModelSerializer,
                                    UserSignSerializer,
                                    AccountVerificationSerializer)

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from cride.users.permissions import IsAccountOwner
# Models
from cride.users.models.users import User
class UserViewSet(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    """Conjunto de vistas de Usuarios.
    
    Maneja registro de usuarios,inicio de sesion y verficacion de cuenta.
    """
    # Estas 3 variables son necesarias para el Retrieve. que por defecto vienen con None en GenericViewSet.
    queryset=User.objects.filter(is_active=True, is_client=True) # QuerySet base para usar el minins.
    serializer_class =UserModelSerializer 
    lookup_field="username" # En la url para acciones que en objectos en vez de colocar el pk que trae por defecto colocaremos el username
    def get_permissions(self):
        """Asigna permisos en función de la acción."""
        if self.action in ['signup','login','verify']:
            permissions=[AllowAny] # No colocamos comillas por que es una clase que se coloca.
        elif self.action=='retrieve':
            permissions=[IsAuthenticated,IsAccountOwner] # Permitira la vista solo si esta autenticado y el usuario que quiere recuperar es el propietario
        else:
            permissions=[IsAuthenticated]
        return [permission() for permission in permissions]
    @action(detail=False,methods=['post'])
    def signup(self,request): # El nombre es cualquiera, es importante que el nombre del metodo que tenemos aqui  que sea el que queremos en la url. Algo asi users/signup
        """Registro de usuarios"""
        serializer=UserSignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #Solo devolvemos el user por que primero el usuario tiene que verificar su email.
        user=serializer.save()
        data=UserModelSerializer(user).data
        return Response(data,status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self,request):# El nombre es cualquiera, es importante que el nombre del metodo que tenemos aqui  que sea el que queremos en la url. Algo asi users/signup
        """Inicio de sesion de usuarios"""
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user,token=serializer.save() # Devuelve 2 valores por que el meetodo create del serializador retorna 2 valores
        data={
            'user':UserModelSerializer(user).data, #Volvemos los datos de user, a datos nativos de Python (De un Model a un Diccionario)
            'access_token':token            
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False,methods=['post'])
    def verify(self,request):# El nombre es cualquiera, es importante que el nombre del metodo que tenemos aqui  que sea el que queremos en la url. Algo asi users/signup
        """Verificacion de cuenta."""
        serializer=AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #Solo devolvemos el user por que primero el usuario tiene que verificar su email.
        serializer.save()
        data={'message':'¡Felicidades, ahora ve a compartir algunos paseos!'}
        return Response(data,status=status.HTTP_200_OK)


# class UserLoginAPIView(APIView):
#     """"Vista de la API para inicio de sesión del usuario."""
    
#     def post(self,request,*args,**kwargs):
#         """"Maneja la solicitud HTTP POST"""
#         serializer=UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user,token=serializer.save() # Devuelve 2 valores por que el meetodo create del serializador retorna 2 valores
#         data={
#             'user':UserModelSerializer(user).data, #Volvemos los datos de user, a datos nativos de Python (De un Model a un Diccionario)
#             'access_token':token            
#         }
#         return Response(data, status=status.HTTP_201_CREATED)


# class UserSignUpAPIView(APIView):
#     """Vista para registro de Usuarios"""
    
#     def post(self,request,*args,**kwargs):
#         """"Maneja la solicitud HTTP POST"""
#         serializer=UserSignSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         #Solo devolvemos el user por que primero el usuario tiene que verificar su email.
#         user=serializer.save()
#         data=UserModelSerializer(user).data
#         return Response(data,status=status.HTTP_201_CREATED)

# class AccountVerificationAPIView(APIView):
#     """vista para verificación de cuenta"""
    
#     def post(self,request,*args,**kwargs):
#         """"Maneja la solicitud HTTP POST"""
#         serializer=AccountVerificationSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         #Solo devolvemos el user por que primero el usuario tiene que verificar su email.
#         serializer.save()
#         data={'message':'¡Felicidades, ahora ve a compartir algunos paseos!'}
#         return Response(data,status=status.HTTP_200_OK)

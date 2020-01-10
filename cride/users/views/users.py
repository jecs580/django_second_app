"""Vista de Usuarios"""

# Django REST Framework
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
# Serializers
from cride.users.serializers import (UserLoginSerializer,
                                    UserModelSerializer,
                                    UserSignSerializer,
                                    AccountVerificationSerializer)

# Models

class UserViewSet(viewsets.GenericViewSet):
    """Conjunto de vistas de Usuarios.
    
    Maneja registro de usuarios,inicio de sesion y verficacion de cuenta.
    """
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

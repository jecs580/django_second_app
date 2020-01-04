"""Vista de Usuarios"""

# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Serializers
from cride.users.serializers import (UserLoginSerializer,
                                    UserModelSerializer,
                                    UserSignSerializer,
                                    AccountVerificationSerializer)

# Models

class UserLoginAPIView(APIView):
    """"Vista de la API para inicio de sesión del usuario."""
    
    def post(self,request,*args,**kwargs):
        """"Maneja la solicitud HTTP POST"""
        serializer=UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user,token=serializer.save() # Devuelve 2 valores por que el meetodo create del serializador retorna 2 valores
        data={
            'user':UserModelSerializer(user).data, #Volvemos los datos de user, a datos nativos de Python (De un Model a un Diccionario)
            'access_token':token            
        }
        return Response(data, status=status.HTTP_201_CREATED)

class UserSignUpAPIView(APIView):
    """Vista para registro de Usuarios"""
    
    def post(self,request,*args,**kwargs):
        """"Maneja la solicitud HTTP POST"""
        serializer=UserSignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #Solo devolvemos el user por que primero el usuario tiene que verificar su email.
        user=serializer.save()
        data=UserModelSerializer(user).data
        return Response(data,status=status.HTTP_201_CREATED)

class AccountVerificationAPIView(APIView):
    """vista para verificación de cuenta"""
    
    def post(self,request,*args,**kwargs):
        """"Maneja la solicitud HTTP POST"""
        serializer=AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #Solo devolvemos el user por que primero el usuario tiene que verificar su email.
        serializer.save()
        data={'message':'¡Felicidades, ahora ve a compartir algunos paseos!'}
        return Response(data,status=status.HTTP_200_OK)

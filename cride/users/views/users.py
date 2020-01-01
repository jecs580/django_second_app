"""Vista de Usuarios"""

# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Serializers
from cride.users.serializers import (UserLoginSerializer,UserModelSerializer)

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
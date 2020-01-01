"""Serializadores de Usuarios"""

# Django
from django.contrib.auth import authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from cride.users.models import User

# Esto es una manera mas simple de serializar un modelo. En vez de colocar crear campos que queremos de un modelo, simplemente le indicamos a django que modelos usaremos con la subclse Meta. Ojo debes enviar ModelSerializer y no Serializer.
class UserModelSerializer(serializers.ModelSerializer):
    """Serializador del modelo de Usuarios"""

    class Meta:
        """Clase Meta"""
        model=User
        fields=('username','first_name','last_name','email','phone_number')

class UserLoginSerializer(serializers.Serializer):
    """Serializador de inicio de sesion de  Usuarios"""

    email=serializers.EmailField()
    password=serializers.CharField(min_length=8, max_length=64)

    # Este metodo corre despues de las validaciones de cada campo, y por defecto los campos son requeridos
    def validate(self, data): # El metodo self nos ayuda a obtener los atributos de la clase.
        """Verifica las credenciales"""
        user=authenticate(username=data['email'], password=data['password']) # data es del tipo diccionario
        if not user:
            raise serializers.ValidationError("Credenciales Invalidas")
        self.context['user'] = user # Añadimos al contexto el usuario logado para el metod create
        return data

    # Este metodo se llamara despues del metodo validated.
    def create(self,data):
        """Genera o recupera un nuevo token"""
        token,created =Token.objects.get_or_create(user=self.context['user']) 
        # Devolvemos un token o lo creamos, se usa este metodo cuando ya tienes algunos usuarios creados y que no tengan un token.Cada ves q nos loguemos el token no cambiara.
        return self.context['user'], token.key 
        # Retornamos el usuario y 


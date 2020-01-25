"""Serializadores de Usuarios"""

# Django
from django.contrib.auth import authenticate,password_validation
from django.core.validators import RegexValidator
from django.conf import settings

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from cride.users.models import User
from cride.users.models import Profile

# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer

# Tasks
from cride.taskapp.tasks import send_confirmation_email

# Esto es una manera mas simple de serializar un modelo. En vez de colocar crear campos que queremos de un modelo, simplemente le indicamos a django que modelos usaremos con la subclse Meta. Ojo debes enviar ModelSerializer y no Serializer.
class UserModelSerializer(serializers.ModelSerializer):
    """Serializador del modelo de Usuarios"""

    profile=ProfileModelSerializer(read_only=True) # Sobre escribimos el campo perfil para que nos devuelva todos los datos del perfil  por la relacion OneToOneField, por defecto solo traeria el id del perfil. Esto es posible por que profile. El atributo read_only permite que los datos del perfil solo puedan leerse, desde la  PUT or PATCH {{host}}/users/{{user}}/. En el caso de que quisieramos modificar los datos del perfil mandamos los datos desde del perfil al serializer de perfil desde la vista.(Serializers Anidados)
    class Meta:
        """Clase Meta"""

        model=User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile' # Campo que se trae por la relacion OneToOneField 
            )


class UserSignSerializer(serializers.Serializer):
    """Serializador de registro de usuarios
    Maneja la validación de datos de registro y la creación de usuarios y su perfil
    """
    # For Users
    email=serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username=serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())])
    # phone_number
    phone_regex=RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El número de teléfono debe ingresarse en el formato: +999999999. Se permiten hasta 15 dígitos.'
    )
    phone_number = serializers.CharField(validators=[phone_regex])
    # password
    password=serializers.CharField(min_length=8,max_length=64)
    password_confirmation=serializers.CharField(min_length=8,max_length=64)
    # Name
    first_name=serializers.CharField(min_length=2,max_length=30)
    last_name=serializers.CharField(min_length=2,max_length=30)

    def validate(self,data):
        """Verifica que coincidan los passwords"""
        password=data['password']
        password_confirmation=data['password_confirmation']
        if password!=password_confirmation:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(password) # Validadores de contraseña por Django, igual lanza exepciones en el caso de que falle algo
        return data
    def create(self,data):
        """Creacion de un nuevo usuario y un perfil"""
        data.pop('password_confirmation')
        user=User.objects.create_user(**data, is_verified=False,is_client=True) # El create_user es la manera mas directa de crear usuarios
        Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk) # Para que se ejecute nuestro metodo de manera asincrona llamamos al metodo .delay y luego colocamos los parametros que requiere nuestro metodo.
        # De esta manera la tarea se ejecutara en segundo plano pero las demas lineas continuaran ejecutandose.
        return user



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
        if not user.is_verified:
            raise serializers.ValidationError("La cuenta aun no esta verificada") # Esto ademas envia un codigo de estado "400" al cliente
        self.context['user'] = user # Añadimos al contexto el usuario logado para el metod create
        return data

    # Este metodo se llamara despues del metodo validated.
    def create(self,data):
        """Genera o recupera un nuevo token"""
        token,created =Token.objects.get_or_create(user=self.context['user']) 
        # Devolvemos un token o lo creamos, se usa este metodo cuando ya tienes algunos usuarios creados y que no tengan un token.Cada ves q nos loguemos el token no cambiara.
        return self.context['user'], token.key 
        # Retornamos el usuario y el token

class AccountVerificationSerializer(serializers.Serializer):
    """Serializador de Verificador de cuenta"""
    token=serializers.CharField()
    def validate_token(self,data):
        """Verifica si el token es valido"""
        try:
            payload=jwt.decode(data,settings.SECRET_KEY,algorithms=['HS256'])
        except jwt.ExpiredSignatureError: # En la documentacion nos indica que coloquemos exceptions, pero en los ejemplos nos muestra que podemos obviar el exceptions y simplemente colocar el nombre de la excepcion.
            raise serializers.ValidationError('El enlace de verificacion ha expirado')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Token Invalido')  # Verificaion con las demas expeciones usando la clase base que heredan todas las excepciones.
        if payload['type']!='email_confirmation':
            raise serializers.ValidationError('Token Invalido')
        self.context['payload']=payload
        return data

    def save(self):
        """Actualizar el estado verificado del usuario"""
        payload=self.context['payload']
        user=User.objects.get(username=payload['user'])
        user.is_verified=True
        user.save()
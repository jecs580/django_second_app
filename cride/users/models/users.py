""""Modelo de Usuarios"""
# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Utilities
from cride.utils.models import CRideModel

class User(CRideModel,AbstractUser):
    """"Modelo de Usuarios
    Extiende de Abstract User de la clase Django, cambiando el valor del campo username por email y agregando campos extras.
    """ 
    email = models.EmailField('direccion de correo', unique=True, error_messages={'unique':'Ya existe un usuario con el correo electronico'}) # El atributo "error_message" crea mensajes de error en el caso de ocurra un error acerca de los otros atributos del campo

    phone_regex=RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='El número de teléfono debe ingresarse en el formato: +999999999. Se permiten hasta 15 dígitos.'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    USERNAME_FIELD = 'email'  # Nombre del campo que queremos cambiar(de username a email)
    REQUIRED_FIELDS= ['username','first_name','last_name'] # Colocamos los campos requeridos al momento de crear un usuario. 

    is_client=models.BooleanField('cliente', default=True, help_text=('Ayuda a distinguir fácilmente a los usuarios y realizar consultas. ','Los clientes son el tipo principal de usuario.')) # Los parentesis en el atributo help_text es como una concatenacion de textos de ayuda.
    is_verified=models.BooleanField('verified',default=True, help_text=('Establece en verdadero cuando el usuario haya verificado su dirección de correo electrónico'))
    def __str__(self):
        """Regresa el username"""
        return self.username

    def get_short_name(self):
        """Retorna username"""
        return self.username # Este funcion por defecto te trae el campo first_name.
"""Manejador de invitaciones de circulo."""

# Django
from django.db import models

# Utilities
import random
from string import ascii_uppercase, digits  # Traemos el alfabeto en mayusculas y todos los digitos 0-9  en strings.


class InvitationManager(models.Manager):  # El BaseManager, trae todos los metodos para los querys.
    """Manejador de invitaciones.

    Usado para manejar la creacion de codigos.
    """
    CODE_LENGTH = 10  # variable global para el tamaño del code

    def create(self, **kwargs):  # Sobre-escribimos el metodo create que viene para los querys.
        """Maneja la creacion de codigos"""
        pool = ascii_uppercase+digits+'.-'  # Variable que almacena: ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.- como cadena
        code = kwargs.get('code',  # Si en la creacion no colocan el campo 'code' con valor,lo generemos con
        # el random. Si confiaramos que el codigo fue llenado usariamos kwargs['code'] directamente.
        ''.join(random.choices(pool, k=self.CODE_LENGTH))  # Sacamos una lista aleatorioa de 10 elementos
        # luego lo convertimos a un string.
        )
        while self.filter(code=code).exists():  # Entrara al while si el codigo que se coloco o se acaba de
            # generar es igual a los anteriores codigos ya existentes.
            code = ''.join(random.choices(pool, k=self.CODE_LENGTH))  # Generara otro codigo difente hasta
            # que sea distinto de los anteriores.
        kwargs['code'] = code  # Finalmente reasignamos el valor de 'code'.
        return super(InvitationManager, self).create(**kwargs)  # Una vez que ejecute la generacion de codigo
        # mandamos a que se ejecute el metodo como estaba creado normalmente.

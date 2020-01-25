"""Tareas de Celery."""
# Django
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives

# Utilities
import jwt
import time
from datetime import timedelta

# Celery
from celery.decorators import task

# Models
from cride.users.models import User

def gen_verification_token(user): 
        """Crea un token JWT que el usuario pueda usar para verificar su cuenta"""
        # El self se utiliza para que la funcion pueda usar los atributos de la clase.
        exp_date=timezone.now()+timedelta(days=3)
        payload={
            'user':user.username,
            'exp':int(exp_date.timestamp()),
            'type':'email_confirmation' #Creamos una variable que especifique de que es el token, se lo usa cuando tu proyecto genera mas JWT en otras aplicaciones y no queremos que se confundan.
        }
        token=jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')
        return token.decode() # regresamos el token en cadena

@task(name='send_confirmation_email', max_retries=3) # Especificamos que estas son tareas de celery, Este decorator recibira el nombre de la tarea, y la otra es el maximo numero de veces que intentara ejecutar la tarea en caso de que ocurra errores
def send_confirmation_email(user_pk): # Quitamos self del metodo por que ya no estan dentro de una clase, Cuando usamos celery en funciones es recomendado no enviar datos complejos como instancias de clases. Es mejor usar solo datos nativos como enteros, strings,etc.
        """Envia un enlace de verificación de cuenta a usuario dado
            Enviando un email al usuario para verificar la cuenta
        """
        for i in range(30):
            time.sleep(1)
            print("Durmiendo zZZ")
        user = User.objects.get(pk=user_pk) # Obtenemos el usuario por su pk
        verification_token=gen_verification_token(user)
        subject='Bienvenido @{}! Verifica tu cuenta para empezar a usar Comparte-Ride'.format(user.username)
        from_email='Comparte Ride <noreply@comparteride.com>'
        content = render_to_string(
            'emails/users/account_verification.html',
            {'token': verification_token, 'user': user}
        ) # Esta variable se usara en caso de que el usario no pueda interpretar el contenido html que se le envio, # El metodo render_to_string(), ayuda a no tener otra variable en caso de que no funcione el html
        
        # html_content = '<p>This is an <strong>important</strong> message.</p>' # Esta variable era del contenido con html pero con la otra variable matamos 2 pajaros de un tiro.

        msg = EmailMultiAlternatives(
            subject, 
            content, 
            from_email, 
            [user.email] # Lista de direcciones de correos a enviar
        ) # El EmailMultiAlternative se utiliza para enviar emails que contengan un contenido de html,
        msg.attach_alternative(
            content # En esta variable agregas la variable con el html pero enviamos content, que posee los 2.
            , "text/html")
        msg.send()
        # Usaremos los JWT para enviar la informacion del usuario sin necesidad de guardarlo en la base de datos.

""" Pruebas de invitacion. """

# Django
from django.test import TestCase

# Model
from cride.circles.models import Invitation,Circle
from cride.users.models import User

class InvitationsManagerTestCase(TestCase):
    """Caso de prueba de manejador de invitaciones."""

    def setUp(self):
        """Configuración de caso de prueba.
        
        Creamos instancias de los modelos para las pruebas,
        estas intancias no se registraran en la base datos
        simplemente usaran el comportamiento que pasaria al momento ejecutar
        el metodo de prueba.
        """
        self.user=User.objects.create(
            first_name='PruebaJorge',
            last_name='Prueba',
            email='prueba@gmail.com',
            username='pruebajorge',
            password='12394085lp'
        )

        self.circle=Circle.objects.create(
            name='Circulo de Test',
            slug_name='circle_test',
            about='Este es un circulo para realizar pruebas usando TestCase',
            verified=True
        )


    def test_code_generation(self):
        """Los códigos aleatorios deben generarse automáticamente.
        
        Verificando que los al crear una invitacion se generen los codigos de invitacion
        en el caso de que el que creo la invitacion no lo envie.
        """
        invitation=Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code) # Verificamos que el campo de codigo no este vacio

    def test_code_usage(self):
        """Si se proporciona un código, no hay necesidad de crear uno nuevo.
        
        Comprobamos que el codigo que se envio este registrado y pueda usarse.
        """
        code='hola mundo'
        invitation=Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code,code) # Si el codigo que colocamos no es igual al que deberia estar en la instacia de invitations del campo code, django nos mostrara en donde fallo al ejecutar las pruebas.

    def test_code_generation_if_duplicated(self):
        """Si se proporciona un codigo que no es unico,un nuevo codigo debe ser generado."""

        code=Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
        ).code # Almacenamos de una nueva instancia de invitacion el campo code

         # Creamos otra invitacion usando el anterior codigo.
        invitation=Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertNotEqual(code,Invitation.code)  # Verificamos que el codigo nuevo no sea el mismo que creamos anteriormente, tiene que generar un nuevo.

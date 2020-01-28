""" Pruebas de invitacion. """

# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework import status
# Django
from django.test import TestCase

# Model
from cride.circles.models import Invitation,Circle,Membership
from cride.users.models import User,Profile
from rest_framework.authtoken.models import Token


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

class MemberInvitationsAPITestCase(APITestCase):
    """Caso de prueba de la API de Invitación de miembro.
    
    Los metodos que crearemos seran para hacer pruebas a los EndPoints
    """
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
        self.profile=Profile.objects.create(user=self.user)
        self.circle=Circle.objects.create(
            name='Circulo de Test',
            slug_name='circle_test',
            about='Este es un circulo para realizar pruebas usando TestCase',
            verified=True
        )

        self.membership=Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10
        )

        # Auth
        # Para acceder a todos nuestros EndPoints generaremos la autenticacion
        self.token=Token.objects.create(user=self.user).key # Generamos un token para el usuario de pruebas
        
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token)) # Mandamos al atributo "client" la autorizacion del token
    
        # Url
        self.url='/circles/{}/members/{}/invitations/'.format(
            self.circle.slug_name,
            self.user.username
        ) # No olvidemos de colocar el "/" al final de la URL

    def test_response_success(self):
        """Verificar solicitud exitosa.
        
        Verificamos el EndPoit de Invitaciones
        """

        request=self.client.get(self.url) # self.client.<metodo>() es un atributo que viene incorporado desde APIClient. El request no solo enviara los datos sino que tambien traera los datos de la respuesta.
        self.assertEqual(request.status_code,status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verifica que se genere la invitación si no existía previamente."""

        # Las invitaciones en la BD deber ser 0
        self.assertEqual(Invitation.objects.count(),0) # Traemos el numero de registros de Invitaciones que existen de prueba.Por defecto tienen estar vacio

        # Llamar a la URL de invitaciones para miembros.Esto registara 10 nuevas invitaciones
        request=self.client.get(self.url)
        self.assertEqual(request.status_code,status.HTTP_200_OK)

        # Verifica que se hayan creado nuevas invitaciones
        invitations=Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(invitations.count(),self.membership.remaining_invitations) # Comparamos que el numero de datos encontrados sea igual al numero de invitaciones que le quedan al usuario.
        import pdb ; pdb.set_trace()
        for invitation in invitations:
            self.assertIn(invitation.code,request.data['invitations'])

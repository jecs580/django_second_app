"""Vista de Usuarios"""

# Django REST Framework
from rest_framework import status,viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.circles.serializers import CircleModelSerializer
from cride.users.serializers import (UserLoginSerializer,
                                    UserModelSerializer,
                                    UserSignSerializer,
                                    AccountVerificationSerializer)

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from cride.users.permissions import IsAccountOwner
# Models
from cride.users.models.users import User # Importacion por archivo, se podria por modulo siempre y cuando lo tengas definido en el __init__ del directorio models de la app
from cride.circles.models import Circle # Importacion de tipo modulo, tambien se puede por archivo

class UserViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin
    ):
    """Conjunto de vistas de Usuarios.
    
    Maneja registro de usuarios,inicio de sesion y verficacion de cuenta.
    """
    # Esta clase permiti hacer GET, PUT, PATCH para un usuario especifico. 
    # Estas 3 variables son necesarias para el Retrieve. que por defecto vienen con None en GenericViewSet.
    queryset=User.objects.filter(is_active=True, is_client=True) # QuerySet base para usar el minins.
    serializer_class =UserModelSerializer 
    lookup_field="username" # En la url para acciones que en objectos en vez de colocar el pk que trae por defecto colocaremos el username
    def get_permissions(self):
        """Asigna permisos en función de la acción."""
        if self.action in ['signup','login','verify']:
            permissions=[AllowAny] # No colocamos comillas por que es una clase que se coloca.
        elif self.action in ['retrieve','update','partial_update']:
            permissions=[IsAuthenticated,IsAccountOwner] # Permitira la vista solo si esta autenticado y el usuario que quiere recuperar es el propietario
        else:
            permissions=[IsAuthenticated]
        return [permission() for permission in permissions]

    def retrieve(self,request,*args,**kwargs): # No queremos cambiar el comportamiento normal del metodo, solo agregarle una funcionalidad extra.
        """Agrega datos adicionales a la respuesta"""
        response=super(UserViewSet,self).retrieve(request,*args,**kwargs) # Primero recuperamos la respuesta que genera el metodo por defecto retrieve.
        circles=Circle.objects.filter(
            members=request.user, # Este campo esta definido en circle, y recibe un user
            membership__is_active=True # Trae las membresias en las que el usuario esta activo
            )
        data ={
            'user':response.data,
            'circle': CircleModelSerializer(circles, many=True).data # Mandamos los circulos serilizados con many=True por que podria estar en mas de un circulo.
        }
        response.data=data
        return response

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

    @action(detail=True,methods=['put','patch']) #Mandamos detail=True por que queremos actualizar un modelo a traves de otro modelo desde un path o put que creamos.
    def profile(self,request,*args,**kwargs): # Esta vista solo se permitira para el dueño de la cuenta.Esta vista tendra un path que sera despues la ruta de actualizar user <path update user>/profile/ para que actualice algo especifico 
        """Actualiza datos de perfil"""
        user=self.get_object()
        profile=user.profile
        partial=request.method=='PATH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial # Este campo permite saber al serializer que sera parcial. Por defecto el serializer pensara que una actualizacion total. Para ambas peticiones no nos devolvera error si no mandamos nada, por que ningun dato es requerido
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data=UserModelSerializer(user).data # Usamos UserModelSerializer por que el serializer tendra un campo llamado profile
        return Response(data)

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

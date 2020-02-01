"""Urls de Circulos"""

# Django
from django.urls import path, include

# #Views
# from cride.circles.views import list_circles, create_circle


# urlpatterns=[
#     path('circles/',list_circles),
#     path('circles/create/',create_circle)
# ]

# Django REST Framework
from rest_framework.routers import DefaultRouter  # Proporciona una vista raiz que devuelve una determinada respuesta.
# View
from .views import circles as circle_views  # Importamos el archivo de vistas de Circulos
from .views import memberships as membership_views

router = DefaultRouter()
router.register(
    r'circles',  # Ruta raiz que buscara
    circle_views.CircleViewSet,  # Vista relacioanada
    basename='circle'
    )  # Recibe una expresion regular que especifican la ruta raiz de nuestro path
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-9_]+)/members',
    membership_views.MembershipViewSet,
    basename='membership'
)  # Ruta para los miembros de un circulo especifico. El slug_name que se le envia loa manda como un
# diccionario con la llave de 'slug_name' a eso se le llama kargs.Si estas usando la vista para recuperar
# un objecto membership, el nombre del miembro seria otro kwargs. que se asigna al diccionario
urlpatterns = [
    path('', include(router.urls))
]

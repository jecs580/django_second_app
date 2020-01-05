"""Urls de Circulos"""

#Django
from django.urls import path,include

# #Views
# from cride.circles.views import list_circles, create_circle


# urlpatterns=[
#     path('circles/',list_circles),
#     path('circles/create/',create_circle)
# ]

# Django REST Framework
from rest_framework.routers import DefaultRouter # Proporciona una vista raiz que devuelve una determinada respuesta.
# View
from .views import circles as circle_views # Importamos el archivo de vistas de Circulos

router=DefaultRouter()
router.register(
    r'circles', # Ruta raiz que buscara
    circle_views.CircleViewSet, # Vista relacioanada
    basename='circle'
    ) # Recibe una expresion regular que especifican la ruta raiz de nuestro path

urlpatterns=[
    path('', include(router.urls))
]
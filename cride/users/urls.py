"""Urls de Usuarios"""

#Django
from django.urls import path, include

# Django REST Framework
from rest_framework.routers import DefaultRouter

#Views
# from cride.users.views import (
#     UserLoginAPIView,
#     UserSignUpAPIView,
#     AccountVerificationAPIView) # Importaciones usando vistas basadas en clases para login,verify and signup

from .views import users as user_views # Importamos el archivo user.No es necesario especificar las clase por que solo usara una clase para todas las vistas que necesitemos.



router=DefaultRouter()
router.register(r'users',user_views.UserViewSet,basename='users')

urlpatterns=[
    # Paths que usaban vistas basdas en clases
    # path('users/login/',UserLoginAPIView.as_view(),name='login'),     
    # path('users/signup/',UserSignUpAPIView.as_view(),name='signup'),     
    # path('users/verify/',AccountVerificationAPIView.as_view(),name='verify'),     
    
    path('',include(router.urls))
]
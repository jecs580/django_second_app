"""Administrador de modelos de usuario"""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Importacion para poder mostrar el modelo personalizado de
# User desde el admin

# Models
from cride.users.models import User, Profile


# Esta clase debemos registrarlo, pero no con el @admin.register(<Model>), puesto que el modelo User ya viene
# registrado por defecto, asi que debemos es sobre-escribirlo.
class CustomeUserAdmin(UserAdmin):
    """Admistrador del modelo de User"""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client')
    list_filter = ('is_client', 'is_staff', 'created', 'modified')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Administrador del modelo Profile"""
    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    serch_fields = ('user__username', 'user__email', 'user__firstname', 'user__last_name')
    list_filter = ('reputation',)  # Nota: si tienes un solo campo a filtrar coloca un coma para que django
    # reconozca que es un tupla, de otro modo te saldra error.


admin.site.register(User, CustomeUserAdmin)  # Con esta declaracion sobre-escribimos el Admin de User,
# mandandole el nuevo modelo, y nuestra clase con las preferencias sobre como listar y como filtrar

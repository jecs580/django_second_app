"""Serializador de Circulos"""
# Django REST Framework
from rest_framework import serializers

class CircleSerializer(serializers.Serializer):
     """Serializador de Circulos"""
     # Para mostrar una lista de circulos en formato Json o XML
     name = serializers.CharField()
     slug_name=serializers.SlugField()
     rides_taken=serializers.IntegerField()
     rides_offered=serializers.IntegerField()
     members_limit=serializers.IntegerField()

class CreateCircleSerializer(serializers.Serializer):
     """Creacion de serializador de circulos"""
     name=serializers.CharField(max_length=140)
     slug_name=serializers.SlugField(max_length=40)
     about=serializers.CharField(max_length=255,
          required=False # por defecto el required es True.
     ) # Esto tambien podria ser un textField por que puede tener una gran cantidad de caracteres, pero DRF no posee el campo, pero para complementar esto DRF no tiene un limite de caracteres.
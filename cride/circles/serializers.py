"""Serializador de Circulos"""
# Django REST Framework
from rest_framework import serializers

class CircleSerializer(serializers.Serializer):
     """Serializador de Circulos"""
     name = serializers.CharField()
     slug_name=serializers.SlugField()
     rides_taken=serializers.IntegerField()
     rides_offered=serializers.IntegerField()
     members_limit=serializers.IntegerField()

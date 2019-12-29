"""Vistas de Circulos"""

# Django
# from django.http import JsonResponse  ; Respuesta que devuevle datos en formato Json

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models
from cride.circles.models import Circle

# Serializers
from cride.circles.serializers import (CircleSerializer,CreateCircleSerializer)
@api_view(['GET'])
def list_circles(request):
    """Lista los Circulos"""
    circles=Circle.objects.filter(is_public=True)
    # data=[]
    # for circle in circles:
    #     serializer=CircleSerializer(circle)
    #     data.append(serializer.data)
    serializer=CircleSerializer(circles,many=True)
    return Response(serializer.data)
    # return JsonResponse(data,safe=False); Retorna los datos en Json, el atributo safe =True indica que los datos que se mandaran es un diccionario, si colocas en False, aceptara otros tipos de datos, por defecto safe esta en True.
@api_view(['POST'])
def create_circle(request):
    """Creacion de circulos"""
    serializer=CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True) # Para validar los campos, por defecto no se tiene atributos, si colocas el atributo raise_exception=True, devolvera una respuesta de 400 al cliente, tambien devolvera un json con los errores que ocurrieron.
    data=serializer.data
    circle=Circle.objects.create(**data) # Desempaquetara todos las llave y valores que trae data.
    return Response(CircleSerializer(circle).data) # Response se encargara de convertirlo a Json.

"""Vistas de Circulos"""

#Django
# from django.http import JsonResponse  ; Respuesta que devuevle datos en formato Json

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

#Models
from cride.circles.models import Circle

@api_view(['GET'])
def list_circles(request):
    """Lista los Circulos"""
    circles=Circle.objects.filter(is_public=True)
    data=[]
    for circle in circles:
        data.append({
            'name':circle.name,
            'slug_name':circle.slug_name,
            'rides_taken':circle.rides_taken,
            'rides_offered':circle.rides_offered,
            'members_limit':circle.members_limit,
        })
    return Response(data)
    # return JsonResponse(data,safe=False); Retorna los datos en Json, el atributo safe =True indica que los datos que se mandaran es un diccionario, si colocas en False, aceptara otros tipos de datos, por defecto safe esta en True.
@api_view(['POST'])
def create_circle(request):
    """Creacion de circulos"""
    name=request.data['name']
    slug_name=request.data['slug_name']
    about=request.data.get('about','') # Esta forma de traer los datos de request nos ayuda para asignar un valor nosostros en caso de que no contenga nada el valor. Por lo general se usa cuando colocamos campos opcionales.
    circle = Circle.objects.create(name=name,slug_name=slug_name,about=about)
    data={
        'name':circle.name,
        'slug_name':circle.slug_name,
        'rides_taken':circle.rides_taken,
        'rides_offered':circle.rides_offered,
        'members_limit':circle.members_limit,
    }
    return Response(data)

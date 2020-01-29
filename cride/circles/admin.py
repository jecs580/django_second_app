"""Administrador de los Modelos de Circulos"""

 # Django
from django.contrib import admin
from django.http import HttpResponse

# Utilities
from django.utils import timezone
from datetime import timedelta,datetime
import csv
# Models
from cride.circles.models import Circle
from cride.rides.models import Ride

@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Modelo de Administrador de Circulos"""
    list_display =(
        'slug_name','name',
        'is_public','verified',
        'is_limited',
        'members_limit'
        )
    search_fields=('slug_name','name')
    list_filter=('is_public','verified','is_limited')

    actions  = ['make_verified','make_unverified','download_today_rides'] # Colocamos en esta variable una lista de las acciones que nosotros creamos.
    
    def make_verified(self,request,queryset):
        """Cambia círculos a verificados"""
        queryset.update(verified=True) # Actualizamos el campo de verified del query que le mandamos del modelo Circle.

    make_verified.short_description = 'Marcar circulos seleccionados a verificados' 

    def make_unverified(self,request,queryset):
        """Cambia círculos a no verificados"""
        queryset.update(verified=False)

    make_unverified.short_description = 'Marcar circulos seleccionados a no verificados' 

    def download_today_rides(self,request,queryset):
        """Regresa los viajes de hoy"""
        now=timezone.now()
        start=datetime(now.year,now.month,now.day,0,0,0)
        end=start + timedelta(days=1)
        rides=Ride.objects.filter(
            offered_in__in=queryset.values_list('id'),
            departure_date__gte=start, # start <= departure_date <= end 
            departure_date__lte=end
        ).order_by('departure_date') # Mandamos los datos ordenamos por la fecha de salida
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rides.csv"' # Descargara el archivo que cree.

        writer = csv.writer(response)
        writer.writerow([
            'id',
            'passengers',
            'departure_location',
            'departure_date',
            'arrival_location',
            'arrival_date',
            'rating'
        ])
        for ride in rides:
            writer.writerow([
                ride.pk,
                ride.passengers.count(), # Le mostramos la cantidad de pasajeros
                ride.departure_location,
                str(ride.departure_date),
                ride.arrival_location,
                str(ride.arrival_date),
                ride.rating
            ])
        return response
    download_today_rides.short_description = 'Descargar los viajes de hoy'
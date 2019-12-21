"""Django models utilitis"""

# Django
from django.db import models

# Todos los modelos heredaran de este
class CrideModel(models.Model):
    create=models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Fecha y hora en la cual el objeto fue creado'
    )
    modified=models.DateTimeField(
    'modified at',
    auto_now=True,
    help_text='Fecha y hora en la cual el objeto fue ultimamente modificado'
    )
    class Meta:
        abstract = True
        get_latest_by ='created'
        ordering =['-created', '-modified'] # Especificamos como queremos que lo ordene, le mandamos otro campo en el particular caso de que se creen al mismo tiempo dos objetos.
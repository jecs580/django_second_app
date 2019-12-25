# Generated by Django 3.0.1 on 2019-12-25 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Fecha y hora en la cual el objeto fue creado', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Fecha y hora en la cual el objeto fue ultimamente modificado', verbose_name='modified at')),
                ('name', models.CharField(max_length=140, verbose_name='Nombre del Circulo')),
                ('slug_name', models.SlugField(unique=True)),
                ('about', models.CharField(max_length=255, verbose_name='Descripcion del Circulo')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='circles/pictures')),
                ('rides_offered', models.PositiveIntegerField(default=0)),
                ('rides_taken', models.PositiveIntegerField(default=0)),
                ('verified', models.BooleanField(default=False, help_text='Los círculos verificados también se conocen como comunidades oficiales.', verbose_name='Verificacion de Circulo')),
                ('is_public', models.BooleanField(default=True, help_text='Los círculos públicos se enumeran en la página principal para que todos sepan sobre su existencia.')),
                ('is_limited', models.BooleanField(default=False, help_text='Los círculos limitados pueden crecer hasta un número fijo de miembros.', verbose_name='Limitado')),
                ('members_limit', models.PositiveIntegerField(default=0, help_text='Si el círculo es limitado, este será el límite en el número de miembros.')),
            ],
            options={
                'ordering': ['-rides_taken', '-rides_offered'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]

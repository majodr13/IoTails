# Generated by Django 5.1.6 on 2025-03-16 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_app', '0002_sensordata_mascota_owneremail'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensordata',
            name='estado_puerta',
            field=models.CharField(choices=[('abierta', 'abierta'), ('cerrada', 'cerrada')], default='cerrada', max_length=20),
        ),
    ]

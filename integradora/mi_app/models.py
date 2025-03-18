from django.db import models

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=50, choices=[("Perro", "Perro"), ("Gato", "Gato")])
    raza = models.CharField(max_length=100, null=True, blank=True)
    problemas_medicos = models.TextField(blank=True, null=True)
    calle = models.CharField(max_length=200, blank=True, null=True)
    colonia = models.CharField(max_length=100, blank=True, null=True)
    numero_exterior = models.CharField(max_length=10, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)
    ownerEmail = models.EmailField(default="example@email.com")

    def __str__(self):
        return self.nombre

class SensorData(models.Model):
    temperatura = models.FloatField()
    humedad = models.FloatField()
    estado_puerta = models.CharField(max_length=20)
    bpm = models.IntegerField(null=True, blank=True)   # <- BPM ahora opcional
    spo2 = models.IntegerField(null=True, blank=True)  # <- SpO2 ahora opcional
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SensorData ({self.fecha.strftime('%d/%m/%Y %H:%M:%S')})"


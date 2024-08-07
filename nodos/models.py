from django.db import models

# Create your models here.
class Nodo(models.Model):
    id_nodo=models.AutoField(primary_key=True)
    codigo= models.CharField(max_length=6)
    latitud_qr1 = models.DecimalField(max_digits=10, decimal_places=7,default=0.0)  # Cambiado de latitud a latitud_qr1
    longitud_qr1 = models.DecimalField(max_digits=10, decimal_places=7,default=0.0)  # Cambiado de longitud a longitud_qr1
    latitud_qr2 = models.DecimalField(max_digits=10, decimal_places=7,default=0.0)  # Nuevo campo latitud_qr2
    longitud_qr2 = models.DecimalField(max_digits=10, decimal_places=7,default=0.0)  # Nuevo campo longitud_qr2
    altitud=models.DecimalField(max_digits=10, decimal_places=7)
    decripcion=models.CharField(max_length=20)
    
    def __str__(self):
        return self.codigo
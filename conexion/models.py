from django.db import models
from nodos.models import Nodo

class Conexion(models.Model):
    id_nodo_origen = models.ForeignKey(Nodo, on_delete=models.CASCADE, related_name="conexiones_salientes")
    id_nodo_destino= models.ForeignKey(Nodo, on_delete=models.CASCADE, related_name="conexiones_entrantes")
    distancia= models.FloatField()

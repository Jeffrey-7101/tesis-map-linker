from rest_framework import serializers
from .models import Conexion

class ConexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conexion
        fields = ['id', 'id_nodo_origen', 'id_nodo_destino', 'distancia']

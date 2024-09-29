# serializers.py
from rest_framework import serializers
from .models import Nodo

class NodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = ['id_nodo', 'codigo', 'latitud_qr1', 'longitud_qr1', 'latitud_qr2', 'longitud_qr2', 'altitud','decripcion']

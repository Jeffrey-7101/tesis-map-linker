from django.contrib import admin
from .models import Conexion
# Register your models here.
@admin.register(Conexion)
class ConexionAdmin(admin.ModelAdmin):
    list_display=('id_nodo_origen','id_nodo_destino','distancia')
    search_fields=('id_nodo_origen','id_nodo_destino')

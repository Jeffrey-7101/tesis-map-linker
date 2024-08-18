# nodos/urls.py
from django.urls import path
from .views import NodoListCreate, NodoUpdateDelete, ListarNodosJson

urlpatterns = [
    path('nodos/', NodoListCreate.as_view(), name='nodo_list_create'),
    path('nodos/<int:id>/', NodoUpdateDelete.as_view(), name='nodo_update_delete'),
    path('listar_nodos_json/', ListarNodosJson.as_view(), name='listar_nodos_json'),
]

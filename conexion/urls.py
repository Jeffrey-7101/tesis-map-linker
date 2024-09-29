from django.urls import path
from . import views

urlpatterns = [
    # Ruta para obtener la lista de conexiones y crear una nueva conexión
    path('conexion/', views.ConexionListCreateAPIView.as_view(), name='conexion-list-create'),

    # Ruta para obtener, actualizar o eliminar una conexión específica por ID
    path('conexion/<int:pk>/', views.ConexionRetrieveUpdateDestroyAPIView.as_view(), name='conexion-retrieve-update-destroy'),
]
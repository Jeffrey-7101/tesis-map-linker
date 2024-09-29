# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Nodo
from .serializers import NodoSerializer

class NodoListCreate(APIView):
    def get(self, request):
        # Listar todos los nodos
        nodos = Nodo.objects.all()
        serializer = NodoSerializer(nodos, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Crear un nuevo nodo
        serializer = NodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail':'Nodo Creado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NodoUpdateDelete(APIView):
    def get(self, request, id):
        # Obtener detalles de un nodo específico
        try:
            nodo = Nodo.objects.get(id_nodo=id)
        except Nodo.DoesNotExist:
            return Response({'detail':'Node not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = NodoSerializer(nodo)
        return Response(serializer.data)

    def put(self, request, id):
        # Actualizar un nodo específico
        try:
            nodo = Nodo.objects.get(id_nodo=id)
        except Nodo.DoesNotExist:
            return Response({'detail':'Node not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = NodoSerializer(nodo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        # Eliminar un nodo específico
        try:
            nodo = Nodo.objects.get(id=id)
        except Nodo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        nodo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ListarNodosJson(APIView):
    def get(self, request):
        nodos = Nodo.objects.all().values('id', 'codigo', 'latitud_qr1', 'longitud_qr1', 'latitud_qr2', 'longitud_qr2', 'altitud')
        return Response({'nodos': list(nodos)})

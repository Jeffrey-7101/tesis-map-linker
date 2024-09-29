from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conexion, Nodo
from .serializers import ConexionSerializer

class ConexionListCreateAPIView(APIView):
    def get(self, request):
        conexiones = Conexion.objects.all()
        serializer = ConexionSerializer(conexiones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ConexionSerializer(data=request.data)
        if serializer.is_valid():
            nodo_origen = serializer.validated_data['id_nodo_origen']
            nodo_destino = serializer.validated_data['id_nodo_destino']
            distancia = serializer.validated_data['distancia']

            # Crear la conexión de A a B
            conexion_a_b = Conexion.objects.create(
                id_nodo_origen=nodo_origen,
                id_nodo_destino=nodo_destino,
                distancia=distancia
            )

            # Crear la conexión de B a A
            conexion_b_a = Conexion.objects.create(
                id_nodo_origen=nodo_destino,
                id_nodo_destino=nodo_origen,
                distancia=distancia
            )

            return Response({'detail': 'Conexión creada con éxito'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConexionRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        try:
            conexion = Conexion.objects.get(pk=pk)
        except Conexion.DoesNotExist:
            return Response({'detail': 'Conexión no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConexionSerializer(conexion)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            conexion = Conexion.objects.get(pk=pk)
        except Conexion.DoesNotExist:
            return Response({'detail': 'Conexión no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConexionSerializer(conexion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            conexion = Conexion.objects.get(pk=pk)
        except Conexion.DoesNotExist:
            return Response({'detail': 'Conexión no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        conexion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

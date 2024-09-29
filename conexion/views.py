from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conexion, Nodo
from .serializers import ConexionSerializer
from collections import defaultdict
import heapq

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

class CalcularCaminoAPIView(APIView):
    def get(self, request):
        id_nodo_origen = request.query_params.get('id_nodo_origen')
        id_nodo_destino = request.query_params.get('id_nodo_destino')

        # Crear un grafo a partir de las conexiones relevantes
        grafo = self.crear_grafo()
        camino, distancia_total = self.dijkstra(grafo, id_nodo_origen, id_nodo_destino)

        if camino is None:
            return Response({'detail': 'No se pudo encontrar un camino entre los nodos proporcionados.'}, 
                            status=status.HTTP_404_NOT_FOUND)

        # Generar la lista de conexiones entre los nodos en el camino
        distancias_camino = []
        for i in range(len(camino) - 1):
            nodo_actual = camino[i]
            siguiente_nodo = camino[i + 1]
            # Buscar la distancia de la conexión
            try:
                conexion = Conexion.objects.get(id_nodo_origen=nodo_actual, id_nodo_destino=siguiente_nodo)
            except Conexion.DoesNotExist:
                # Manejar el caso en que la conexión no existe
                return Response({'detail': f'No existe conexión entre {nodo_actual} y {siguiente_nodo}.'}, 
                                status=status.HTTP_404_NOT_FOUND)
            
            distancias_camino.append({
                'nodo_origen': nodo_actual,
                'nodo_destino': siguiente_nodo,
                'distancia': conexion.distancia
            })

        return Response({
            'camino': distancias_camino,
            'distancia_total': distancia_total
        }, status=status.HTTP_200_OK)

    def crear_grafo(self):
        # Crea un grafo a partir de las conexiones en la base de datos
        grafo = defaultdict(list)
        conexiones = Conexion.objects.all()

        for conexion in conexiones:
            grafo[conexion.id_nodo_origen_id].append((conexion.id_nodo_destino_id, conexion.distancia))
            grafo[conexion.id_nodo_destino_id].append((conexion.id_nodo_origen_id, conexion.distancia))

        print("Grafo construido:", dict(grafo))  # Depuración: imprime el grafo
        return grafo

    def dijkstra(self, grafo, inicio, fin):
        # Verifica si los nodos de inicio y fin están en el grafo
        if inicio not in grafo or fin not in grafo:
            return None, None  # O puedes lanzar un error más descriptivo

        # Implementación del algoritmo de Dijkstra
        distancias = {nodo: float('infinity') for nodo in grafo}
        distancias[inicio] = 0
        prioridad = [(0, inicio)]
        caminos = {nodo: [] for nodo in grafo}
        caminos[inicio] = [inicio]

        while prioridad:
            distancia_actual, nodo_actual = heapq.heappop(prioridad)

            if distancia_actual > distancias[nodo_actual]:
                continue

            for vecino, peso in grafo[nodo_actual]:
                distancia = distancia_actual + peso

                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    caminos[vecino] = caminos[nodo_actual] + [vecino]
                    heapq.heappush(prioridad, (distancia, vecino))

        if fin not in distancias or distancias[fin] == float('infinity'):
            return None, None

        return caminos[fin], distancias[fin]
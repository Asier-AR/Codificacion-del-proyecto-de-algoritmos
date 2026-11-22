from Clases import Inventario

class Sede:
    def __init__(self, nombre, inventario=None):

        self._Nombre=nombre
        self._Inventario=inventario if inventario is not None else Inventario()


class SistemaSede:
    def __init__(self, sedes=None, conexiones=None):
        self._sedes = sedes if sedes is not None else {}
        self._vecinos = conexiones if conexiones is not None else {}     # nombre -> {nombreVecino: distancia} guarda las distancias existentes entre sedes

    def agregarSede(self, sede):
        self._sedes.append(sede)

    def añadirConexion(self, sede1, sede2, distancia):
        if sede1 not in self._vecinos:
            self._vecinos[sede1] = {}
        if sede2 not in self._vecinos:
            self._vecinos[sede2] = {}
        self._vecinos[sede1][sede2] = distancia
        self._vecinos[sede2][sede1] = distancia  # Conexión bidireccional

    def obtenerDistancia(self, sede1, sede2, visitados=None):
        if visitados is None:
            visitados = []
        if sede1 == sede2:
            return 0
        visitados.append(sede1)
        mejor = -1
        for vecino, peso in self._vecinos[sede1].items():
            if vecino in visitados:
                continue
            resto = self.obtenerDistancia(vecino, sede2, visitados) #recursividad para buscar la distancia entre sedes
            if resto != -1 and (mejor == -1 or peso + resto < mejor): 
                mejor = peso + resto
        visitados.remove(sede1)      # backtracking: se libera para otras rutas
        return mejor

    def sedesMasCarcanasConRecurso(self, sedeOrigen, nombreRecurso):
        """
        Busca en todas las sedes (excepto sedeOrigen) si tienen el recurso
        disponible (en inventarioDisponible, no en Nodisponible).
        Devuelve una lista de tuplas (nombreSede, distancia) ordenada por
        distancia (Dijkstra simplificado / BFS con pesos usando cola de
        prioridad manual). Devuelve lista vacía si no hay ninguna.
        """
        # --- Dijkstra ---
        INF = float("inf")
        dist = {s: INF for s in self._sedes}
        dist[sedeOrigen] = 0
        pendientes = [sedeOrigen]           # cola simplificada (nodos por procesar)

        # Un Dijkstra sin heapq pero correcto para grafos pequeños (<20 nodos):
        # repite hasta que todos los nodos estén procesados.
        procesados = set()
        while pendientes:
            # elegir el nodo con menor dist que no esté procesado
            actual = min(pendientes, key=lambda s: dist[s])
            pendientes.remove(actual)
            if actual in procesados:
                continue
            procesados.add(actual)
            for vecino, peso in self._vecinos.get(actual, {}).items():
                nueva = dist[actual] + peso
                if nueva < dist[vecino]:
                    dist[vecino] = nueva
                    if vecino not in pendientes:
                        pendientes.append(vecino)

        # --- filtrar sedes que tienen el recurso disponible ---
        resultado = []
        for nombreSede, sede in self._sedes.items():
            if nombreSede == sedeOrigen:
                continue
            inv = sede._Inventario
            if nombreRecurso in inv._inventarioDisponible:
                resultado.append((nombreSede, dist[nombreSede]))

        resultado.sort(key=lambda t: t[1])   # ordenar por distancia
        return resultado

    def buscarEnOtrasSedes(self, sedeOrigen, nombreRecurso):
        """
        HU008 – interfaz de alto nivel para el menú.
        Imprime el resultado y devuelve la lista de (sede, distancia).
        """
        encontradas = self.sedesMasCarcanasConRecurso(sedeOrigen, nombreRecurso)
        if not encontradas:
            # verificar si existe el recurso aunque sea en Nodisponible
            existeEn = []
            for nombreSede, sede in self._sedes.items():
                if nombreSede == sedeOrigen:
                    continue
                inv = sede._Inventario
                if nombreRecurso in inv._inventarioDisponible or nombreRecurso in inv._Nodisponible:
                    existeEn.append(nombreSede)
            if existeEn:
                print(f"El recurso '{nombreRecurso}' existe en {existeEn} pero está agotado en todas.")
            else:
                print(f"El recurso '{nombreRecurso}' no existe en ninguna sede.")
            return []
        print(f"\nSedes con '{nombreRecurso}' disponible (ordenadas por cercanía a '{sedeOrigen}'):")
        for sede, dist in encontradas:
            print(f"  → {sede}  (distancia: {dist} km)")
        print(f"Recomendación: ir a '{encontradas[0][0]}' (más cercana, {encontradas[0][1]} km).")
        return encontradas

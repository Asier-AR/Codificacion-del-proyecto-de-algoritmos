from Clases import Inventario

class Sede:
    def __init__(self, nombre, inventario=None):

        self._Nombre=nombre
        self._Inventario=inventario if inventario is not None else Inventario()


class SistemaSede:
    def __init__(self, sedes=None, conexiones=None):
        self._sedes = sedes if sedes is not None else []
        self._vecinos = conexiones if conexiones is not None else []     # nombre -> {nombreVecino: distancia} guarda las distancias existentes entre sedes

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


        
        


        

        
    


    

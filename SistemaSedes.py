from Clases import Inventario

class Sede:
    def __init__(self, nombre, inventario=None):

        self._Nombre=nombre
        self._Inventario=inventario if inventario is not None else Inventario()


class SistemaSede:
    def __init__(self):
        self._sedes = {}       # nombre -> Sede diccionario que guarda el nombre de las sedes
        self._vecinos = {}     # nombre -> {nombreVecino: distancia} guarda las distancias existentes entre sedes

    def añadirSede(self, sede):
        if sede._Nombre in self._sedes:
            print("Esa sede ya existe.")
            return False
        self._sedes[sede._Nombre] = sede
        self._vecinos[sede._Nombre] = {}
        return True

    def conectar(self, a, b, distancia): #funcion que conecta las sedes generando una distancia
        if a not in self._sedes or b not in self._sedes or a == b: # si alguna de las 2 sedes no existe no se hace nada
            return False
        if distancia <= 0: #si la distancia ingresada es menor a 0 o -1 entonces no se hace nada
            return False
        self._vecinos[a][b] = distancia
        self._vecinos[b][a] = distancia   # no dirigido
        return True

        
    


    

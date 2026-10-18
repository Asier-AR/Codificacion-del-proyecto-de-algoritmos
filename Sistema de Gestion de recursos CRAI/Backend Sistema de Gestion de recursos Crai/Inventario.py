class Inventario: #clase inventario que va a contener un diccionario de objetos de clase recurso o hijos de esta clase
    def __init__(self, inventario):
        self._inventarioDisponible = inventario or {} #guarda todos los objetos que se le ingresen en la seccion disponible y si no se le ingresa ninguno crea un diccionario vacio
        self._Nodisponible = {} #Crea un diccionario vacio donde se van a guardar los recursos cuando su cantidad llegue a 0

    def añadirRecurso(self, nuevo): #metodo que se encarga de añadir un recurso nuevo o si este recurso ya existe entonces añadira mas elementos a su cantidad
        nombre = nuevo._nombre 
        if nombre in self._inventarioDisponible: #añade mas cantidad de objetos al recurso si este existe
            print(f"El recurso {nombre} ya existe añadiendo cantidad ingresada al recurso ")
            self._inventarioDisponible[nombre]._cantidad += nuevo._cantidad
        elif nombre in self._Nodisponible: #verifica que el recurso no este en la lista de nodisponibles y si esta le añade la cantidad y luego lo mueve a disponibles
            self._Nodisponible[nombre]._cantidad += nuevo._cantidad
            self._inventarioDisponible[nombre] = self._Nodisponible.pop(nombre)
        else: #crea un recurso nuevo si este no se encuentra repetido 
            self._inventarioDisponible[nombre] = nuevo
        return True

    def darDeBajaRecurso(self, nombre): #sirve para eliminar un recurso del inventario 
        if nombre in self._inventarioDisponible:
            recurso = self._inventarioDisponible[nombre]  #si el objeto esta en inventario disponible crea una variable recurso que guardara el objeto atado a la clave nombre
            diccionario = self._inventarioDisponible #crea una variable diccionario que realmente es el inventario disponible
        elif nombre in self._Nodisponible: #repite los mismos pasos si el recurso esta en inventario no disponible
            recurso = self._Nodisponible[nombre] 
            diccionario = self._Nodisponible
        else: #si no existe en ninguno de los dos el recurso no existe 
            print("El recurso que deseas dar de baja no existe o se introdujo mal su nombre.")
            return False

        if recurso._listaEspera: #si hay usuarios en la lista de espera del recurso este no se puede dar de baja
            print("No se puede dar de baja: hay usuarios en la lista de espera.")
            return False

        del diccionario[nombre] #elimina el recurso
        print(f"Recurso '{nombre}' dado de baja.")
        return True    
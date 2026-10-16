class Pila:
    # Pila: el ultimo en entrar es el primero en salir (LIFO)
    def __init__(self):
        self._elementos = []
 
    def apilar(self, elemento):          # meter al tope
        self._elementos.append(elemento)
 
    def desapilar(self):                 # sacar el tope (None si esta vacia)
        if self.estaVacia():
            return None
        return self._elementos.pop()
 
    def cima(self):                      # mirar el tope sin sacarlo
        if self.estaVacia():
            return None
        return self._elementos[len(self._elementos) - 1]
 
    def estaVacia(self):
        return len(self._elementos) == 0
    
# OPERACIONES (clase padre y clases hijas)

class Operacion:
    def __init__(self, descripcion):
        self._descripcion = descripcion
 
    def deshacer(self):                  # cada hija lo escribe a su manera
        raise NotImplementedError("Cada operación debe definir cómo se deshace")
 
    def __str__(self):
        return self._descripcion
 
 
class OpRegistro(Operacion):
    # Se registro un usuario u operador en un diccionario. Deshacer = quitarlo.
    def __init__(self, tipoPersona, diccionario, clave, persona):
        super().__init__(f"Registro de {tipoPersona}: {persona._nombre} {persona._apellido} (C.C. {persona._cedula})")
        self._diccionario = diccionario
        self._clave = clave
 
    def deshacer(self):
        del self._diccionario[self._clave]
 
 
class OpEliminarPersona(Operacion):
    # Se elimino un usuario u operador. Deshacer = volver a ponerlo (con todos sus datos).
    def __init__(self, tipoPersona, diccionario, clave, persona):
        super().__init__(f"Eliminación de {tipoPersona}: {persona._nombre} {persona._apellido} (C.C. {persona._cedula})")
        self._diccionario = diccionario
        self._clave = clave
        self._persona = persona
 
    def deshacer(self):
        self._diccionario[self._clave] = self._persona
 
class HistorialOperaciones:
    def __init__(self):
        self._pila = Pila()
 
    def registrar(self, operacion):
        self._pila.apilar(operacion)
 
    def verUltima(self):                 # None si no hay nada para deshacer
        return self._pila.cima()
 
    def deshacerUltima(self):
        operacion = self._pila.desapilar()
        if operacion is None:
            print("No hay operaciones para deshacer.")
            return False
        operacion.deshacer()
        print("Se deshizo:", operacion)
        return True
 
    def confirmarYDeshacer(self):
        # esta es la que se llama desde el menu del operador
        ultima = self.verUltima()
        if ultima is None:
            print("No hay operaciones para deshacer.")
            return
        print("Última operación registrada:")
        print(" ", ultima)
        eleccion = input("Digite 1 para deshacerla, 2 para cancelar: ")
        if eleccion == "1":
            self.deshacerUltima()
        else:
            print("Acción cancelada.")
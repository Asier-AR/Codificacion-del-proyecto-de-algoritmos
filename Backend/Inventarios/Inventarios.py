class Inventario:
    def __init__(self, inventario=None):
        self._inventarioDisponible = inventario if inventario is not None else {}
        self._Nodisponible = {}
        self._libro = {}      # categoría -> [nombres]
        self._Equipo = {}     # categoría -> [nombres]
        self._Otros = []
        for objeto in self._inventarioDisponible.values():
            self._clasificar(objeto)

    def _clasificar(self, objeto):
        if isinstance(objeto, libro):
            self._libro.setdefault(objeto._categoria, []).append(objeto._nombre)
        elif isinstance(objeto, equipoComputacion):
            self._Equipo.setdefault(objeto._categoria, []).append(objeto._nombre)
        else:
            self._Otros.append(objeto._nombre)

    def _desclasificar(self, objeto):
        if isinstance(objeto, libro):
            arbol = self._libro
        elif isinstance(objeto, equipoComputacion):
            arbol = self._Equipo
        else:
            self._Otros.remove(objeto._nombre)
            return
        arbol[objeto._categoria].remove(objeto._nombre)
        if not arbol[objeto._categoria]:      # si la categoría quedó vacía, se borra
            del arbol[objeto._categoria]        
        

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
            self._clasificar(nuevo)
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
        self._desclasificar(recurso)
        del diccionario[nombre] #elimina el recurso
        print(f"Recurso '{nombre}' dado de baja.")

        return True    


import random
from datetime import date, timedelta

class recurso:
    def __init__(self, nombre="", cantidad=0, fechaIngreso=None):
        self._nombre = nombre
        self._cantidad = cantidad
        self._listaEspera = []
        self._fechaIngreso = fechaIngreso or self.generarFecha()

    def generarFecha(self):
        inicio = date(2024, 1, 1)
        fin = date(2026, 11, 22)
        dias = (fin - inicio).days
        return (inicio + timedelta(days=random.randrange(dias + 1))).strftime("%Y-%m-%d")


class libro(recurso):
    def __init__(self, nombre="", cantidad=0, autor="", fechaPublicacion="", categoria="general"):
        super().__init__(nombre, cantidad)
        self._autor = autor
        self._fechaPublicacion = fechaPublicacion
        self._categoria = categoria.strip().lower() or "general"


class equipoComputacion(recurso):
    def __init__(self, nombre="", cantidad=0, modelo="", categoria="general"):
        super().__init__(nombre, cantidad)
        self._modelo = modelo
        self._categoria = categoria.strip().lower() or "general"
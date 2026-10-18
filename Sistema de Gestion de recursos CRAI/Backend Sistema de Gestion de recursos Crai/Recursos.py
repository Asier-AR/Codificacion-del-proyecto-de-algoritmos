class recurso: #clase recurso que servira como base para las clases hijas libro y equipoComputacion
    def __init__(self, nombre="", cantidad=0):
        self._nombre=nombre
        self._cantidad=cantidad
        self._listaEspera=[]

class libro(recurso):
    def __init__(self, nombre="", cantidad=0, autor="", fechaPublicacion=""):
        super().__init__(nombre, cantidad)
        self._autor=autor
        self._fechaPublicacion=fechaPublicacion


class equipoComputacion(recurso):
     def __init__(self, nombre="", cantidad=0, modelo=""):
            super().__init__(nombre, cantidad)
            self._modelo=modelo
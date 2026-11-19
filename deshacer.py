class Pila: #Pila: el ultimo en entrar es el primero en salir (LIFO), se usa para guardar las operaciones en orden
    def __init__(self):
        self._elementos = [] #lista de Python donde el final de la lista es el tope de la pila

    def apilar(self, elemento): #mete un elemento al tope de la pila
        self._elementos.append(elemento) #append agrega al final, que es el tope

    def desapilar(self): #saca y devuelve el tope
        if self.estaVacia():
            return None #si no hay nada devuelve None en vez de dar error
        return self._elementos.pop() #pop quita y devuelve el ultimo elemento

    def cima(self): #mira el tope SIN sacarlo
        if self.estaVacia():
            return None
        return self._elementos[len(self._elementos) - 1] #el ultimo elemento de la lista

    def estaVacia(self): #True si no hay ningun elemento
        return len(self._elementos) == 0


# Cada operacion guarda lo necesario para revertirse (los objetos afectados y, si hace falta, el estado anterior).
# deshacer() devuelve True si pudo revertir y False si no (imprimiendo el motivo).

class Operacion: #clase padre de todas las operaciones
    def __init__(self, descripcion):
        self._descripcion = descripcion #texto que se le muestra a la persona al pedir confirmacion

    def deshacer(self): #cada clase hija lo escribe a su manera (polimorfismo)
        raise NotImplementedError("Cada operación debe definir cómo se deshace") #si una hija no lo define, avisa del error

    def __str__(self): #permite hacer print(operacion) y usarla dentro de un f-string
        return self._descripcion


class OpRegistro(Operacion):
    # Se registro un usuario u operador. Deshacer = quitarlo.
    def __init__(self, tipoPersona, diccionario, clave, persona): #tipoPersona: "usuario" u "operador", diccionario: donde se guardo, clave: la cedula
        super().__init__(f"Registro de {tipoPersona}: {persona._nombre} {persona._apellido} (C.C. {persona._cedula})")
        self._diccionario = diccionario #usuarios u operadores
        self._clave = clave #cedula con la que se guardo
        self._persona = persona #se guarda para comprobar que sigue siendo la misma persona

    def deshacer(self):
        if self._diccionario.get(self._clave) is not self._persona: #"is not" compara que sea el MISMO objeto, no solo que sea igual
            print("No se puede deshacer: esa persona ya no está registrada.") #ya la eliminaron o esa cedula es de otra persona
            return False
        if getattr(self._persona, "_objetosReservados", None): #getattr con None por defecto porque los operadores no tienen este atributo
            print("No se puede deshacer: la persona ya tiene préstamos activos.") #borrarla dejaria prestamos huerfanos
            return False
        del self._diccionario[self._clave] #quita a la persona del diccionario
        return True


class OpEliminarPersona(Operacion):
    # Se elimino un usuario u operador. Deshacer = volver a ponerlo con todos sus datos.
    def __init__(self, tipoPersona, diccionario, clave, persona):
        super().__init__(f"Eliminación de {tipoPersona}: {persona._nombre} {persona._apellido} (C.C. {persona._cedula})")
        self._diccionario = diccionario
        self._clave = clave
        self._persona = persona #se guarda el objeto completo para conservar sancion, objetos reservados, contraseña, etc.

    def deshacer(self):
        if self._clave in self._diccionario: #otra persona se registro con esa cedula mientras tanto
            print("No se puede deshacer: ya hay otra persona registrada con esa cédula.") #restaurar pisaria sus datos
            return False
        self._diccionario[self._clave] = self._persona #vuelve a ponerla con la misma cedula
        return True


class OpSancion(Operacion):
    # Se sanciono o se quito la sancion. Guarda el estado anterior y lo restaura.
    def __init__(self, usuario, sancionAnterior): #sancionAnterior: True si ya tenia sancion antes (la accion fue quitarla), False si no (la accion fue sancionar)
        accion = "Retiro de sanción a" if sancionAnterior else "Sanción a" #elige el texto segun la accion que se hizo
        super().__init__(f"{accion} {usuario._nombre} {usuario._apellido}")
        self._usuario = usuario
        self._sancionAnterior = sancionAnterior #una sola clase sirve para las dos acciones porque solo se restaura el estado previo

    def deshacer(self):
        self._usuario._sancion = self._sancionAnterior #siempre se puede restaurar, no necesita validaciones
        return True


class OpAnadirRecurso(Operacion):
    # Se anadieron unidades a un recurso (nuevo o existente). Deshacer = restar esas unidades.
    def __init__(self, inventario, nombre, cantidad, eraNuevo): #eraNuevo: True si el recurso no existia antes de añadirlo
        super().__init__(f"Añadir {cantidad} unidad(es) del recurso '{nombre}'")
        self._inventario = inventario #objeto Inventario, se necesitan sus dos diccionarios
        self._nombre = nombre
        self._cantidad = cantidad #cuantas unidades se añadieron
        self._eraNuevo = eraNuevo

    def deshacer(self):
        disp = self._inventario._inventarioDisponible #recursos con unidades
        nodisp = self._inventario._Nodisponible #recursos agotados
        if self._nombre in disp: #1. se busca el recurso en cualquiera de los dos inventarios
            r = disp[self._nombre]
        elif self._nombre in nodisp:
            r = nodisp[self._nombre]
        else:
            print("No se puede deshacer: el recurso ya no existe en el inventario.") #lo dieron de baja
            return False

        nueva = r._cantidad - self._cantidad #cantidad que quedaria despues de restar lo añadido
        if nueva < 0: #2. si quedaria negativa, alguien ya presto parte de esas unidades
            print("No se puede deshacer: parte de esas unidades ya fue prestada.")
            return False

        r._cantidad = nueva #3. se restan las unidades
        if nueva == 0: #si no queda nada hay que acomodar el recurso
            if self._eraNuevo and not r._listaEspera:
                disp.pop(self._nombre, None) #el recurso no existia antes: se borra (None evita error si no esta en ese dict)
                nodisp.pop(self._nombre, None)
            elif self._nombre in disp:
                nodisp[self._nombre] = disp.pop(self._nombre) #ya existia: vuelve a quedar agotado
        return True


class OpBajaRecurso(Operacion):
    # Se dio de baja un recurso. Deshacer = devolverlo al inventario donde estaba.
    def __init__(self, inventario, recurso, estabaDisponible): #estabaDisponible: True si estaba en inventarioDisponible, False si en Nodisponible
        super().__init__(f"Baja del recurso '{recurso._nombre}'")
        self._inventario = inventario
        self._recurso = recurso #objeto completo, con su cantidad y lista de espera
        self._estabaDisponible = estabaDisponible

    def deshacer(self):
        nombre = self._recurso._nombre
        if nombre in self._inventario._inventarioDisponible or nombre in self._inventario._Nodisponible: #alguien creo otro recurso con el mismo nombre
            print("No se puede deshacer: ya existe otro recurso con ese nombre.") #restaurar lo pisaria
            return False
        if self._estabaDisponible: #se devuelve al mismo diccionario del que salio
            self._inventario._inventarioDisponible[nombre] = self._recurso
        else:
            self._inventario._Nodisponible[nombre] = self._recurso
        return True


class OpPrestamo(Operacion):
    # Se hizo un prestamo. Deshacer = anularlo como si nunca hubiera pasado.
    def __init__(self, sistema, prestamo):
        super().__init__(f"Préstamo #{prestamo._numero} de '{prestamo._recurso._nombre}' a {prestamo._usuario._nombre} {prestamo._usuario._apellido}")
        self._sistema = sistema #objeto SistemaPrestamos
        self._prestamo = prestamo #el prestamo que se hizo

    def deshacer(self):
        return self._sistema.anularPrestamo(self._prestamo) #la logica esta en Prestamos.py porque ahi viven los historiales y el contador


class OpDevolucion(Operacion):
    # Se devolvio un recurso. Deshacer = volver a dejar el prestamo activo.
    def __init__(self, sistema, prestamo):
        super().__init__(f"Devolución del préstamo #{prestamo._numero} ('{prestamo._recurso._nombre}')")
        self._sistema = sistema
        self._prestamo = prestamo

    def deshacer(self):
        return self._sistema.reabrirPrestamo(self._prestamo) #la logica esta en Prestamos.py


class OpListaEspera(Operacion):
    # Un usuario se unio a la lista de espera de un recurso agotado. Deshacer = sacarlo de la lista.
    def __init__(self, recurso, usuario):
        super().__init__(f"Unirse a la lista de espera de '{recurso._nombre}'")
        self._recurso = recurso
        self._usuario = usuario

    def deshacer(self):
        if self._usuario not in self._recurso._listaEspera: #si ya no esta, le llego el turno y se le presto el recurso
            print("No se puede deshacer: ya saliste de la lista de espera (te atendieron).") #ese caso se deshace deshaciendo el prestamo
            return False
        self._recurso._listaEspera.remove(self._usuario) #lo saca de la lista
        return True

class HistorialOperaciones: #envuelve una Pila de operaciones, menu.py crea uno por persona
    def __init__(self):
        self._pila = Pila()

    def registrar(self, operacion): #se llama justo despues de hacer una accion reversible
        self._pila.apilar(operacion)

    def verUltima(self): #mira la ultima operacion sin sacarla, None si no hay nada para deshacer
        return self._pila.cima()

    def deshacerUltima(self):
        operacion = self._pila.desapilar() #saca la ultima operacion de la pila
        if operacion is None:
            print("No hay operaciones para deshacer.")
            return False
        if operacion.deshacer(): #cada operacion sabe como revertirse
            print("Se deshizo:", operacion)
            return True
        print("No se pudo deshacer:", operacion) #la operacion se descarta: el estado cambio y ya no es reversible, asi no bloquea las anteriores
        return False

    def confirmarYDeshacer(self): #es la que se llama desde el menu del operador y del usuario
        ultima = self.verUltima() #se mira sin sacar, por si la persona cancela
        if ultima is None:
            print("No hay operaciones para deshacer.")
            return
        print("Última operación registrada:")
        print(" ", ultima)
        eleccion = input("Digite 1 para deshacerla, 2 para cancelar: ")
        if eleccion == "1":
            self.deshacerUltima()
        else:
            print("Acción cancelada.") #cualquier otra cosa cancela, la operacion sigue en la pila
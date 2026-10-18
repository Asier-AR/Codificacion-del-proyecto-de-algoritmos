class Pila:
    # Pila: el ultimo en entrar es el primero en salir (LIFO)
    def __init__(self):
        self._elementos = []

    def apilar(self, elemento):
        self._elementos.append(elemento)

    def desapilar(self):
        if self.estaVacia():
            return None
        return self._elementos.pop()

    def cima(self):
        if self.estaVacia():
            return None
        return self._elementos[len(self._elementos) - 1]

    def estaVacia(self):
        return len(self._elementos) == 0

# Cada operacion guarda lo necesario para revertirse.
# deshacer() devuelve True si pudo revertir y False si no (imprimiendo el motivo).

class Operacion:
    def __init__(self, descripcion):
        self._descripcion = descripcion

    def deshacer(self):
        raise NotImplementedError("Cada operación debe definir cómo se deshace")

    def __str__(self):
        return self._descripcion


class OpRegistro(Operacion):
    # Se registro un usuario u operador. Deshacer = quitarlo.
    def __init__(self, tipoPersona, diccionario, clave, persona):
        super().__init__(f"Registro de {tipoPersona}: {persona._nombre} {persona._apellido} (C.C. {persona._cedula})")
        self._diccionario = diccionario
        self._clave = clave
        self._persona = persona

    def deshacer(self):
        if self._diccionario.get(self._clave) is not self._persona:
            print("No se puede deshacer: esa persona ya no está registrada.")
            return False
        if getattr(self._persona, "_objetosReservados", None):
            print("No se puede deshacer: la persona ya tiene préstamos activos.")
            return False
        del self._diccionario[self._clave]
        return True


class OpEliminarPersona(Operacion):
    # Se elimino un usuario u operador. Deshacer = volver a ponerlo con todos sus datos.
    def __init__(self, tipoPersona, diccionario, clave, persona):
        super().__init__(f"Eliminación de {tipoPersona}: {persona._nombre} {persona._apellido} (C.C. {persona._cedula})")
        self._diccionario = diccionario
        self._clave = clave
        self._persona = persona

    def deshacer(self):
        if self._clave in self._diccionario:
            print("No se puede deshacer: ya hay otra persona registrada con esa cédula.")
            return False
        self._diccionario[self._clave] = self._persona
        return True


class OpSancion(Operacion):
    # Se sanciono o se quito la sancion. Guarda el estado anterior y lo restaura.
    def __init__(self, usuario, sancionAnterior):
        accion = "Retiro de sanción a" if sancionAnterior else "Sanción a"
        super().__init__(f"{accion} {usuario._nombre} {usuario._apellido}")
        self._usuario = usuario
        self._sancionAnterior = sancionAnterior

    def deshacer(self):
        self._usuario._sancion = self._sancionAnterior
        return True


class OpAnadirRecurso(Operacion):
    # Se anadieron unidades a un recurso (nuevo o existente). Deshacer = restar esas unidades.
    def __init__(self, inventario, nombre, cantidad, eraNuevo):
        super().__init__(f"Añadir {cantidad} unidad(es) del recurso '{nombre}'")
        self._inventario = inventario
        self._nombre = nombre
        self._cantidad = cantidad
        self._eraNuevo = eraNuevo

    def deshacer(self):
        disp = self._inventario._inventarioDisponible
        nodisp = self._inventario._Nodisponible
        if self._nombre in disp:
            r = disp[self._nombre]
        elif self._nombre in nodisp:
            r = nodisp[self._nombre]
        else:
            print("No se puede deshacer: el recurso ya no existe en el inventario.")
            return False

        nueva = r._cantidad - self._cantidad
        if nueva < 0:
            print("No se puede deshacer: parte de esas unidades ya fue prestada.")
            return False

        r._cantidad = nueva
        if nueva == 0:
            if self._eraNuevo and not r._listaEspera:
                disp.pop(self._nombre, None)       # el recurso no existia antes: se borra
                nodisp.pop(self._nombre, None)
            elif self._nombre in disp:
                nodisp[self._nombre] = disp.pop(self._nombre)   # vuelve a quedar agotado
        return True


class OpBajaRecurso(Operacion):
    # Se dio de baja un recurso. Deshacer = devolverlo al inventario donde estaba.
    def __init__(self, inventario, recurso, estabaDisponible):
        super().__init__(f"Baja del recurso '{recurso._nombre}'")
        self._inventario = inventario
        self._recurso = recurso
        self._estabaDisponible = estabaDisponible

    def deshacer(self):
        nombre = self._recurso._nombre
        if nombre in self._inventario._inventarioDisponible or nombre in self._inventario._Nodisponible:
            print("No se puede deshacer: ya existe otro recurso con ese nombre.")
            return False
        if self._estabaDisponible:
            self._inventario._inventarioDisponible[nombre] = self._recurso
        else:
            self._inventario._Nodisponible[nombre] = self._recurso
        return True


class OpPrestamo(Operacion):
    # Se hizo un prestamo. Deshacer = anularlo como si nunca hubiera pasado.
    def __init__(self, sistema, prestamo):
        super().__init__(f"Préstamo #{prestamo._numero} de '{prestamo._recurso._nombre}' a {prestamo._usuario._nombre} {prestamo._usuario._apellido}")
        self._sistema = sistema
        self._prestamo = prestamo

    def deshacer(self):
        return self._sistema.anularPrestamo(self._prestamo)


class OpDevolucion(Operacion):
    # Se devolvio un recurso. Deshacer = volver a dejar el prestamo activo.
    def __init__(self, sistema, prestamo):
        super().__init__(f"Devolución del préstamo #{prestamo._numero} ('{prestamo._recurso._nombre}')")
        self._sistema = sistema
        self._prestamo = prestamo

    def deshacer(self):
        return self._sistema.reabrirPrestamo(self._prestamo)


class OpListaEspera(Operacion):
    # Un usuario se unio a la lista de espera. Deshacer = sacarlo de la lista.
    def __init__(self, recurso, usuario):
        super().__init__(f"Unirse a la lista de espera de '{recurso._nombre}'")
        self._recurso = recurso
        self._usuario = usuario

    def deshacer(self):
        if self._usuario not in self._recurso._listaEspera:
            print("No se puede deshacer: ya saliste de la lista de espera (te atendieron).")
            return False
        self._recurso._listaEspera.remove(self._usuario)
        return True


# ---------------- HISTORIAL ----------------

class HistorialOperaciones:
    def __init__(self):
        self._pila = Pila()

    def registrar(self, operacion):
        self._pila.apilar(operacion)

    def verUltima(self):
        return self._pila.cima()

    def deshacerUltima(self):
        operacion = self._pila.desapilar()
        if operacion is None:
            print("No hay operaciones para deshacer.")
            return False
        if operacion.deshacer():
            print("Se deshizo:", operacion)
            return True
        print("No se pudo deshacer:", operacion)   # la operacion se descarta, ya no es reversible
        return False

    def confirmarYDeshacer(self):
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
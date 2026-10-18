from datetime import datetime
from deshacer import OpPrestamo, OpDevolucion, OpListaEspera

class Prestamo:
    def __init__(self, numero, usuario, recurso):
        self._numero = numero
        self._usuario = usuario              # objeto usuario
        self._recurso = recurso              # objeto recurso
        self._fechaPrestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._fechaDevolucion = ""           # vacio = todavia no lo devuelve
        self._estado = "Activo"              # Activo o Devuelto

    def registrarDevolucion(self):
        self._estado = "Devuelto"
        self._fechaDevolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        texto = f"#{self._numero} | {self._usuario._nombre} {self._usuario._apellido} | {self._recurso._nombre} | Prestado: {self._fechaPrestamo} | {self._estado}"
        if self._estado == "Devuelto":
            texto += f" el {self._fechaDevolucion}"
        return texto


class SistemaPrestamos:
    def __init__(self, inventario):
        self._inventarioDisponible = inventario._inventarioDisponible   # dict de recursos
        self._inventarioNoDisponible = inventario._Nodisponible         # dict de recursos no disponibles
        self._historialUsuarios = {}         # cedula -> lista de prestamos
        self._historialRecursos = {}         # nombre del recurso -> lista de prestamos
        self._contador = 0                   # numero consecutivo de prestamo

    def prestar(self, usuario, nombreRecurso, historial=None):
        # --- validaciones ---
        if usuario._sancion:
            print("No puedes realizar préstamos porque tienes una sanción activa.")
            return False
        if nombreRecurso not in self._inventarioDisponible and nombreRecurso not in self._inventarioNoDisponible:
            print("El recurso no existe en el inventario.")
            return False
        if nombreRecurso in self._inventarioNoDisponible:
            print("No hay unidades disponibles de este recurso.")
            eleccion = str(input("Le gustaria unirse a la lista de espera (escribe 1 para confirmar, 2 para negarse): "))
            if eleccion == "1":
                agotado = self._inventarioNoDisponible[nombreRecurso]
                lista = agotado._listaEspera
                if usuario in lista:
                    print("Usted ya se encuentra en la lista de espera de este recurso")
                    return False
                lista.append(usuario)
                if historial is not None:
                    historial.registrar(OpListaEspera(agotado, usuario))
                print("Ya quedaste en la lista de espera")
                return True
            elif eleccion == "2":
                print("Saliendo del proceso")
                return False
            else:
                print("Opcion invalida saliendo del proceso")
                return False

        recurso = self._inventarioDisponible[nombreRecurso]
        # --- se hace el prestamo ---
        self._contador += 1
        nuevo = Prestamo(self._contador, usuario, recurso)
        recurso._cantidad -= 1
        if recurso._cantidad == 0:
            self._inventarioNoDisponible[nombreRecurso] = self._inventarioDisponible.pop(nombreRecurso)
        usuario._objetosReservados.append(nombreRecurso)

        # --- se guarda en los dos historiales ---
        if usuario._cedula not in self._historialUsuarios:
            self._historialUsuarios[usuario._cedula] = []
        self._historialUsuarios[usuario._cedula].append(nuevo)

        if nombreRecurso not in self._historialRecursos:
            self._historialRecursos[nombreRecurso] = []
        self._historialRecursos[nombreRecurso].append(nuevo)

        if historial is not None:
            historial.registrar(OpPrestamo(self, nuevo))

        print("Préstamo registrado:", nuevo)
        return True

    def prestamosActivos(self, usuario):
        activos = []
        if usuario._cedula in self._historialUsuarios:
            for p in self._historialUsuarios[usuario._cedula]:
                if p._estado == "Activo":
                    activos.append(p)
        return activos

    def devolver(self, usuario, numeroPrestamo, registrados, historial=None):
        for p in self.prestamosActivos(usuario):
            if p._numero == numeroPrestamo:
                p.registrarDevolucion()
                p._recurso._cantidad += 1
                nombre = p._recurso._nombre
                if nombre in usuario._objetosReservados:
                    usuario._objetosReservados.remove(nombre)
                print("Devolución registrada:", p)
                if historial is not None:
                    historial.registrar(OpDevolucion(self, p))   # antes de atender la espera
                if nombre in self._inventarioNoDisponible:
                    self._inventarioDisponible[nombre] = self._inventarioNoDisponible.pop(nombre)
                    self.atenderEspera(nombre, registrados, historial)
                return True
        print("No tienes un préstamo activo con ese número.")
        return False

    # ---------- para deshacer ----------
    def anularPrestamo(self, p):
        # deshace un prestamo: lo borra de los historiales y devuelve la unidad
        if p._estado != "Activo":
            print("No se puede deshacer: ese préstamo ya fue devuelto.")
            return False
        nombre = p._recurso._nombre
        if nombre not in self._inventarioDisponible and nombre not in self._inventarioNoDisponible:
            print("No se puede deshacer: el recurso ya no está en el inventario.")
            return False

        p._recurso._cantidad += 1
        if nombre in self._inventarioNoDisponible:
            self._inventarioDisponible[nombre] = self._inventarioNoDisponible.pop(nombre)
        if nombre in p._usuario._objetosReservados:
            p._usuario._objetosReservados.remove(nombre)
        if p in self._historialUsuarios.get(p._usuario._cedula, []):
            self._historialUsuarios[p._usuario._cedula].remove(p)
        if p in self._historialRecursos.get(nombre, []):
            self._historialRecursos[nombre].remove(p)
        if p._numero == self._contador:
            self._contador -= 1
        return True

    def reabrirPrestamo(self, p):
        # deshace una devolucion: el prestamo vuelve a estar activo
        if p._estado != "Devuelto":
            print("No se puede deshacer: ese préstamo ya está activo.")
            return False
        nombre = p._recurso._nombre
        if nombre not in self._inventarioDisponible:
            print("No se puede deshacer: otra persona ya tomó la unidad devuelta.")
            return False

        p._recurso._cantidad -= 1
        if p._recurso._cantidad == 0:
            self._inventarioNoDisponible[nombre] = self._inventarioDisponible.pop(nombre)
        p._estado = "Activo"
        p._fechaDevolucion = ""
        p._usuario._objetosReservados.append(nombre)
        return True

    def verHistorialUsuario(self, usuario, recientePrimero=True):
        print(f"\nHistorial de {usuario._nombre} {usuario._apellido}:")
        if usuario._cedula not in self._historialUsuarios or not self._historialUsuarios[usuario._cedula]:
            print(" - Sin préstamos.")
            return
        lista = self._historialUsuarios[usuario._cedula]
        if recientePrimero:
            lista = lista[::-1]
        for p in lista:
            print(" -", p)

    def verHistorialRecurso(self, nombreRecurso, recientePrimero=True):
        if nombreRecurso not in self._inventarioDisponible and nombreRecurso not in self._inventarioNoDisponible:
            print("El recurso no existe en el inventario.")
            return
        print(f"\nHistorial de {nombreRecurso}:")
        if nombreRecurso not in self._historialRecursos or not self._historialRecursos[nombreRecurso]:
            print(" - Sin préstamos.")
            return
        lista = self._historialRecursos[nombreRecurso]
        if recientePrimero:
            lista = lista[::-1]
        for p in lista:
            print(" -", p)

    def atenderEspera(self, nombre, registrados, historial=None):
        while nombre in self._inventarioDisponible:
            recurso = self._inventarioDisponible[nombre]
            if not recurso._listaEspera:
                break
            Us = recurso._listaEspera.pop(0)
            if Us._sancion or Us._cedula not in registrados:
                continue
            self.prestar(Us, nombre, historial)

    def tienePrestamosActivos(self, nombre):
        if nombre not in self._historialRecursos:
            return False
        for p in self._historialRecursos[nombre]:
            if p._estado == "Activo":
                return True
        return False
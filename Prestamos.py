from datetime import datetime

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
        self._inventario = inventario        # dict de recursos
        self._historialUsuarios = {}         # cedula -> lista de prestamos
        self._historialRecursos = {}         # nombre del recurso -> lista de prestamos
        self._contador = 0                   # numero consecutivo de prestamo

    def prestar(self, usuario, nombreRecurso):
        # --- validaciones ---
        if usuario._sancion:
            print("No puedes realizar préstamos porque tienes una sanción activa.")
            return False
        if nombreRecurso not in self._inventario:
            print("El recurso no existe en el inventario.")
            return False
        recurso = self._inventario[nombreRecurso]
        if recurso._cantidad <= 0:
            print("No hay unidades disponibles de este recurso.")
            return False

        # --- se hace el prestamo ---
        self._contador += 1
        nuevo = Prestamo(self._contador, usuario, recurso)
        recurso._cantidad -= 1
        usuario._objetosReservados.append(nombreRecurso)   # asi el operador lo ve al buscar al usuario

        # --- se guarda en los dos historiales ---
        if usuario._cedula not in self._historialUsuarios:
            self._historialUsuarios[usuario._cedula] = []
        self._historialUsuarios[usuario._cedula].append(nuevo)

        if nombreRecurso not in self._historialRecursos:
            self._historialRecursos[nombreRecurso] = []
        self._historialRecursos[nombreRecurso].append(nuevo)

        print("Préstamo registrado:", nuevo)
        return True

    def prestamosActivos(self, usuario):
        # recorre el historial del usuario y se queda solo con los que siguen activos
        activos = []
        if usuario._cedula in self._historialUsuarios:
            for p in self._historialUsuarios[usuario._cedula]:
                if p._estado == "Activo":
                    activos.append(p)
        return activos

    def devolver(self, usuario, numeroPrestamo):
        for p in self.prestamosActivos(usuario):
            if p._numero == numeroPrestamo:
                p.registrarDevolucion()
                p._recurso._cantidad += 1
                if p._recurso._nombre in usuario._objetosReservados:
                    usuario._objetosReservados.remove(p._recurso._nombre)
                print("Devolución registrada:", p)
                return True
        print("No tienes un préstamo activo con ese número.")
        return False

    def verHistorialUsuario(self, usuario, recientePrimero=True):
        print(f"\nHistorial de {usuario._nombre} {usuario._apellido}:")
        if usuario._cedula not in self._historialUsuarios:
            print(" - Sin préstamos.")
            return
        lista = self._historialUsuarios[usuario._cedula]
        if recientePrimero:
            lista = lista[::-1]              # lista al reves
        for p in lista:
            print(" -", p)

    def verHistorialRecurso(self, nombreRecurso, recientePrimero=True):
        if nombreRecurso not in self._inventario:
            print("El recurso no existe en el inventario.")
            return
        print(f"\nHistorial de {nombreRecurso}:")
        if nombreRecurso not in self._historialRecursos:
            print(" - Sin préstamos.")
            return
        lista = self._historialRecursos[nombreRecurso]
        if recientePrimero:
            lista = lista[::-1]
        for p in lista:
            print(" -", p)
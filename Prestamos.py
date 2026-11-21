from datetime import datetime
from deshacer import OpPrestamo, OpDevolucion, OpListaEspera


class Prestamo:
    def __init__(self, numero, usuario, recurso, sede):
        self._numero = numero
        self._usuario = usuario              # objeto usuario
        self._recurso = recurso              # objeto recurso
        self._sede = sede                    # nombre de la sede donde se hizo el prestamo
        self._fechaPrestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._fechaDevolucion = ""           # vacio = todavia no lo devuelve
        self._estado = "Activo"              # Activo o Devuelto

    def registrarDevolucion(self):
        self._estado = "Devuelto"
        self._fechaDevolucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        texto = (f"#{self._numero} | {self._usuario._nombre} {self._usuario._apellido} | "
                 f"{self._recurso._nombre} | Sede: {self._sede} | "
                 f"Prestado: {self._fechaPrestamo} | {self._estado}")
        if self._estado == "Devuelto":
            texto += f" el {self._fechaDevolucion}"
        return texto


class SistemaPrestamos:
    def __init__(self, sistemaSede):
        self._sistemaSede = sistemaSede      # grafo de sedes; cada sede tiene su Inventario
        self._historialUsuarios = {}         # cedula -> lista de prestamos
        self._historialRecursos = {}         # (sede, nombre) -> lista de prestamos
        self._contador = 0                   # numero consecutivo de prestamo
        self._obtenerHistorial = None        # funcion que entrega la pila de deshacer de una persona (la asigna menu.py)
        self._usuarios = None                # diccionario de usuarios (lo asigna menu.py), lo usa anularPrestamo

    def _inv(self, sede): #devuelve el inventario de una sede
        return self._sistemaSede._sedes[sede]._Inventario

    def prestar(self, usuario, sede, nombreRecurso, historial=None, silencioso=False):
        inv = self._inv(sede)
        disp = inv._inventarioDisponible
        nodisp = inv._Nodisponible
        # --- validaciones ---
        if usuario._sancion:
            print("No puedes realizar préstamos porque tienes una sanción activa.")
            return False
        if nombreRecurso not in disp and nombreRecurso not in nodisp:
            print("El recurso no existe en esta sede.")
            return False
        if nombreRecurso in nodisp:
            print("No hay unidades disponibles de este recurso en esta sede.")
            eleccion = str(input("Le gustaria unirse a la lista de espera (escribe 1 para confirmar, 2 para negarse): "))
            if eleccion == "1":
                agotado = nodisp[nombreRecurso]
                if usuario in agotado._listaEspera:
                    print("Usted ya se encuentra en la lista de espera de este recurso")
                    return False
                agotado._listaEspera.append(usuario)
                if historial is not None:
                    historial.registrar(OpListaEspera(agotado, usuario)) #unirse a la espera tambien se puede deshacer
                print("Ya quedaste en la lista de espera")
                return True
            elif eleccion == "2":
                print("Saliendo del proceso")
                return False
            else:
                print("Opcion invalida saliendo del proceso")
                return False

        recurso = disp[nombreRecurso]
        # --- se hace el prestamo ---
        self._contador += 1
        nuevo = Prestamo(self._contador, usuario, recurso, sede)
        recurso._cantidad -= 1
        if recurso._cantidad == 0:
            nodisp[nombreRecurso] = disp.pop(nombreRecurso) #pasa a no disponibles
        usuario._objetosReservados.append(nombreRecurso)

        # --- se guarda en los dos historiales ---
        if usuario._cedula not in self._historialUsuarios:
            self._historialUsuarios[usuario._cedula] = []
        self._historialUsuarios[usuario._cedula].append(nuevo)

        clave = (sede, nombreRecurso)
        if clave not in self._historialRecursos:
            self._historialRecursos[clave] = []
        self._historialRecursos[clave].append(nuevo)

        if historial is not None:
            historial.registrar(OpPrestamo(self, nuevo)) #se apila para poder deshacer el prestamo

        if not silencioso:
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
                inv = self._inv(p._sede) #la devolucion va a la sede donde se presto
                p.registrarDevolucion()
                p._recurso._cantidad += 1
                nombre = p._recurso._nombre
                if nombre in usuario._objetosReservados:
                    usuario._objetosReservados.remove(nombre)
                print("Devolución registrada:", p)
                if historial is not None:
                    historial.registrar(OpDevolucion(self, p)) #se apila antes de atender la espera
                if nombre in inv._Nodisponible:
                    inv._inventarioDisponible[nombre] = inv._Nodisponible.pop(nombre)
                    self.atenderEspera(p._sede, nombre, registrados, historial)
                return True
        print("No tienes un préstamo activo con ese número.")
        return False

    # ---------- metodos que usa deshacer.py ----------
    def anularPrestamo(self, p): #deshace un prestamo: lo borra de los historiales y devuelve la unidad al inventario
        if p._estado != "Activo":
            print("No se puede deshacer: ese préstamo ya fue devuelto.")
            return False
        inv = self._inv(p._sede)
        nombre = p._recurso._nombre
        if nombre not in inv._inventarioDisponible and nombre not in inv._Nodisponible:
            print("No se puede deshacer: el recurso ya no está en el inventario.")
            return False

        p._recurso._cantidad += 1
        if nombre in inv._Nodisponible:
            inv._inventarioDisponible[nombre] = inv._Nodisponible.pop(nombre)
        if nombre in p._usuario._objetosReservados:
            p._usuario._objetosReservados.remove(nombre)
        lista = self._historialUsuarios.get(p._usuario._cedula, [])
        if p in lista:
            lista.remove(p)
        lista = self._historialRecursos.get((p._sede, nombre), [])
        if p in lista:
            lista.remove(p)
        if p._numero == self._contador: #si era el ultimo, se libera su numero
            self._contador -= 1
        if self._usuarios is not None: #la unidad quedo libre: se atiende a quien esperaba
            self.atenderEspera(p._sede, nombre, self._usuarios)
        return True

    def reabrirPrestamo(self, p): #deshace una devolucion: el prestamo vuelve a estar activo
        if p._estado != "Devuelto":
            print("No se puede deshacer: ese préstamo ya está activo.")
            return False
        if p._usuario._sancion:
            print("No se puede deshacer: el usuario tiene una sanción activa.")
            return False
        inv = self._inv(p._sede)
        nombre = p._recurso._nombre
        if nombre not in inv._inventarioDisponible:
            print("No se puede deshacer: otra persona ya tomó la unidad devuelta.")
            return False

        p._recurso._cantidad -= 1
        if p._recurso._cantidad == 0:
            inv._Nodisponible[nombre] = inv._inventarioDisponible.pop(nombre)
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

    def verHistorialRecurso(self, sede, nombreRecurso, recientePrimero=True):
        inv = self._inv(sede)
        if nombreRecurso not in inv._inventarioDisponible and nombreRecurso not in inv._Nodisponible:
            print("El recurso no existe en esta sede.")
            return
        print(f"\nHistorial de {nombreRecurso} en {sede}:")
        clave = (sede, nombreRecurso)
        if clave not in self._historialRecursos or not self._historialRecursos[clave]:
            print(" - Sin préstamos.")
            return
        lista = self._historialRecursos[clave]
        if recientePrimero:
            lista = lista[::-1]
        for p in lista:
            print(" -", p)

    def atenderEspera(self, sede, nombre, registrados, historial=None):
        disp = self._inv(sede)._inventarioDisponible
        while nombre in disp:
            recurso = disp[nombre]
            if not recurso._listaEspera:
                break
            Us = recurso._listaEspera.pop(0)
            if Us._cedula not in registrados: #el usuario ya no existe
                continue
            if Us._sancion: #se le saca de la fila y se le avisa por que
                Us._buzon.append(f"Se te retiró de la lista de espera de '{nombre}' (sede {sede}) porque tienes una sanción activa.")
                continue
            pila = self._obtenerHistorial("us", Us._cedula) if self._obtenerHistorial else historial #el prestamo queda en la pila de quien lo recibe
            if self.prestar(Us, sede, nombre, pila, True):
                Us._buzon.append(f"El recurso {nombre} (sede {sede}) que tenias en la lista de espera ya te fue prestado y ya puedes ir a reclamarlo")

    def tienePrestamosActivos(self, sede, nombre):
        clave = (sede, nombre)
        if clave not in self._historialRecursos:
            return False
        for p in self._historialRecursos[clave]:
            if p._estado == "Activo":
                return True
        return False
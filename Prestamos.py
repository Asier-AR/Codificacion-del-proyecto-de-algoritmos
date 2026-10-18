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
        self._inventarioDisponible = inventario._inventarioDisponible# dict de recursos
        self._inventarioNoDisponible=inventario._Nodisponible #dict de recursos no disponibles    
        self._historialUsuarios = {}         # cedula -> lista de prestamos
        self._historialRecursos = {}         # nombre del recurso -> lista de prestamos
        self._contador = 0                   # numero consecutivo de prestamo

    def prestar(self, usuario, nombreRecurso, silencioso=False):
        # --- validaciones ---
        if usuario._sancion:
            print("No puedes realizar préstamos porque tienes una sanción activa.")
            return False
        if nombreRecurso not in self._inventarioDisponible and nombreRecurso not in self._inventarioNoDisponible: 
            print("El recurso no existe en el inventario.")
            return False
        if nombreRecurso in self._inventarioNoDisponible:
            print("No hay unidades disponibles de este recurso.")
            eleccion=str(input("Le gustaria unirse a la lista de espera (escribe 1 para confirmar, 2 para negarse): "))
            if eleccion=="1":
                lista=self._inventarioNoDisponible[nombreRecurso]._listaEspera
                if usuario in lista:
                    print("Usted ya se encuentra en la lista de espera de este recurso")
                    return False
                lista.append(usuario)
                print("Ya quedaste en la lista de espera")
                return True
            elif eleccion =="2":
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
        if recurso._cantidad== 0:
            self._inventarioNoDisponible[nombreRecurso]=self._inventarioDisponible.pop(nombreRecurso) #movemos el recurso de los inventarios disponibles a los no disponibles
        usuario._objetosReservados.append(nombreRecurso)   # asi el operador lo ve al buscar al usuario

        # --- se guarda en los dos historiales ---
        if usuario._cedula not in self._historialUsuarios:
            self._historialUsuarios[usuario._cedula] = []
        self._historialUsuarios[usuario._cedula].append(nuevo)

        if nombreRecurso not in self._historialRecursos:
            self._historialRecursos[nombreRecurso] = []
        self._historialRecursos[nombreRecurso].append(nuevo)

        if not silencioso:
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

    def devolver(self, usuario, numeroPrestamo, registrados): #metodo que permite devolver un recurso
        for p in self.prestamosActivos(usuario):
            if p._numero == numeroPrestamo:
                p.registrarDevolucion()
                p._recurso._cantidad += 1
                nombre = p._recurso._nombre
                if nombre in usuario._objetosReservados:
                    usuario._objetosReservados.remove(nombre)
                print("Devolución registrada:", p)
                if nombre in self._inventarioNoDisponible:
                    self._inventarioDisponible[nombre] = self._inventarioNoDisponible.pop(nombre)
                    self.atenderEspera(nombre, registrados)
                return True
        print("No tienes un préstamo activo con ese número.")
        return False
    
    def verHistorialUsuario(self, usuario, recientePrimero=True): #metodo que permite ver el historial de acciones realizadas por un usuario
        print(f"\nHistorial de {usuario._nombre} {usuario._apellido}:")
        if usuario._cedula not in self._historialUsuarios:
            print(" - Sin préstamos.")
            return
        lista = self._historialUsuarios[usuario._cedula]
        if recientePrimero:
            lista = lista[::-1]              # lista al reves
        for p in lista:
            print(" -", p)

    def verHistorialRecurso(self, nombreRecurso, recientePrimero=True): #metodo que permite ver las personas que han pedido prestadas un recurso junto con sus fechas
        if nombreRecurso not in self._inventarioDisponible and nombreRecurso not in self._inventarioNoDisponible:
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
            
    def atenderEspera(self, nombre, registrados): #metodo que se encarga de realizar los prestamos de manera automatica para las personas que esten en una lista de espera
        while nombre in self._inventarioDisponible:
            recurso = self._inventarioDisponible[nombre]
            if not recurso._listaEspera:
                break
            Us = recurso._listaEspera.pop(0)
            if Us._sancion or Us._cedula not in registrados: #si el usuario esta sancionado o ya no existe en el registro continua al siguiente
                continue
            if self.prestar(Us, nombre, True): #realiza el prestamo de manera automatica
                Us._buzon.append(f"El recurso {nombre} que tenias en la lista de espera ya te fue prestado y ya puedes ir a reclamarlo")


    def tienePrestamosActivos(self, nombre): #se encarga de verificar que un usuario tenga o no tenga prestamos activos
        if nombre not in self._historialRecursos:
            return False
        for p in self._historialRecursos[nombre]:
            if p._estado == "Activo":
                return True
        return False
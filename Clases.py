class persona:
    def __init__(self, nombre="", apellido="", cedula=0, nombreUsuario="", contraseña=""):
        self._nombre = nombre
        self._apellido = apellido
        self._cedula = cedula
        self._nombreUsuario = nombreUsuario
        self._contraseña = contraseña

    def iniciarSesion(self): #permite iniciar Sesion usando el nombre de usuario y la contraseña dandole 4 intentos a la persona
        for j in range(4):
            nombreUsuario = input("Ingrese su nombre de usuario: ")
            contraseña = input("Ingrese su contraseña: ")
            if nombreUsuario == self._nombreUsuario and contraseña == self._contraseña:
                print(f"Inicio de sesión exitoso, bienvenido {self._nombre} {self._apellido}")
                return True
            print(f"Usuario o contraseña no válidos. Intentos restantes: {3 - j}")
        print("Número de intentos agotados, volviendo al menú")
        return False
            


class usuario(persona): 
    def __init__(self, nombre="", apellido="", cedula=0, nombreUsuario="", contraseña="",
                 sanciones=False, objetosReservados=None):
        super().__init__(nombre, apellido, cedula, nombreUsuario, contraseña)
        self._sancion = sanciones
        self._objetosReservados = objetosReservados or []


class Operador(persona):
    def __init__(self, nombre="", apellido="", cedula=0, nombreUsuario="", contraseña=""):
        super().__init__(nombre, apellido, cedula, nombreUsuario, contraseña)
    # sin iniciarSesion: la hereda de persona

    def buscador(self, registrados): #permite buscar un usuari
        try:
            cedulaBuscar = int(input("Ingrese la cédula que desea buscar: "))
        except ValueError:
            print("Ingrese solo números.")
            return -1
        u = registrados.get(cedulaBuscar)
        if u is None:
            print("Usuario no encontrado.")
            return -1
        print("Usuario encontrado:")
        print(f"Nombre: {u._nombre}")
        print(f"Apellido: {u._apellido}")
        print(f"Cédula: {u._cedula}")
        print(f"Sanción: {u._sancion}")
        print("Objetos reservados:")
        for obj in u._objetosReservados:
            print(f" - {obj}")

    def mostrarUsuarios(self, registrados):
        if not registrados:
            print("No hay usuarios registrados.")
            return
        for u in registrados.values():
            print(f"Nombre: {u._nombre}")
            print(f"Apellido: {u._apellido}")
            print(f"Cédula: {u._cedula}")
            print(f"Sanción: {u._sancion}")
            if u._objetosReservados:
                print("Objetos reservados:")
                for obj in u._objetosReservados:
                    print(f" - {obj}")
            else:
                print("Objetos reservados: Ninguno")
            print("-" * 30)
    def eliminarUsuario(self, registrados):
        try:
            cedulaBuscar = int(input("Ingrese la cédula del usuario que desea eliminar: "))
        except ValueError:
            print("Ingrese solo números.")
            return
        u = registrados.get(cedulaBuscar)
        if u is None:
            print("No se encontró ningún usuario con esa cédula.")
            return
        print(f"¿Desea eliminar a {u._nombre} {u._apellido} (C.C. {u._cedula})?")
        eleccion = input("Digite 1 para confirmar, 2 para cancelar: ")
        if eleccion == "1":
            del registrados[cedulaBuscar]
            print("Usuario eliminado correctamente.")
        else:
            print("Acción cancelada.")
    def sancionarUsuario(self, Us):
        if Us._sancion:
            print("El usuario ya tiene una sanción activa.")
            return False
        Us._sancion = True
        print(f"Usuario {Us._nombre} {Us._apellido} sancionado.")
        return True
    def quitarSancion(self, Us):
        if Us._sancion:
            print(f"Revocando sancion a {Us._nombre} {Us._apellido}")
            Us._sancion= False
        else: 
            print(f"El usuario {Us._nombre} {Us._apellido} no posee ninguna sancion activa")

class Inventario:
    def __init__(self, inventario):
        self._inventarioDisponible = inventario or {}
        self._Nodisponible = {}

    def añadirRecurso(self, nuevo):
        nombre = nuevo._nombre
        if nombre in self._inventarioDisponible:
            self._inventarioDisponible[nombre]._cantidad += nuevo._cantidad
        elif nombre in self._Nodisponible:
            self._Nodisponible[nombre]._cantidad += nuevo._cantidad
            self._inventarioDisponible[nombre] = self._Nodisponible.pop(nombre)
        else:
            self._inventarioDisponible[nombre] = nuevo
        return True

    def darDeBajaRecurso(self, nombre):
        if nombre in self._inventarioDisponible:
            recurso = self._inventarioDisponible[nombre]
            diccionario = self._inventarioDisponible
        elif nombre in self._Nodisponible:
            recurso = self._Nodisponible[nombre]
            diccionario = self._Nodisponible
        else:
            print("El recurso que deseas dar de baja no existe.")
            return False

        if recurso._listaEspera:
            print("No se puede dar de baja: hay usuarios en la lista de espera.")
            return False

        del diccionario[nombre]
        print(f"Recurso '{nombre}' dado de baja.")
        return True    


class recurso:
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


      
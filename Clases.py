class persona:
    def __init__(self, nombre="", apellido="", cedula=0, nombreUsuario="", contraseña=""): #constructor de la clase persona
        self._nombre = nombre
        self._apellido = apellido
        self._cedula = cedula
        self._nombreUsuario = nombreUsuario
        self._contraseña = contraseña

    def iniciarSesion(self): #creacion del metodo iniciar sesion
        for j in range(4):
            nombreUsuario = input("Ingrese su nombre de usuario: ")
            contraseña = input("Ingrese su contraseña: ")
            if nombreUsuario == self._nombreUsuario and contraseña == self._contraseña:
                print(f"Inicio de sesión exitoso, bienvenido {self._nombre} {self._apellido}")
                return True
            print(f"Usuario o contraseña no válidos. Intentos restantes: {3 - j}")
        print("Número de intentos agotados, volviendo al menú")
        return False
            


class usuario(persona): #clase usuario hija de la clase persona
    def __init__(self, nombre="", apellido="", cedula=0, nombreUsuario="", contraseña="", sanciones=False, objetosReservados=None): #constructor de la clase usuario
        super().__init__(nombre, apellido, cedula, nombreUsuario, contraseña)
        self._sancion = sanciones
        self._objetosReservados = objetosReservados or [] #se se crea una lista de objetos reservados si se incluye una en el constructor o si no la crea vacia


class Operador(persona): #clae operador hija de la clase persona
    def __init__(self, nombre="", apellido="", cedula=0, nombreUsuario="", contraseña=""):
        super().__init__(nombre, apellido, cedula, nombreUsuario, contraseña)
    # sin iniciarSesion: la hereda de persona

    def buscador(self, registrados): #metodo para buscar usuarios en la base de datos
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

    def mostrarUsuarios(self, registrados): #metodo que printea a todos los usuarios
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
    def eliminarUsuario(self, registrados): #Metodo que elimina usuarios de la base de datos
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

class Inventario: 
    def __init__(self, inventario):
        self._inventarioDisponible=inventario or {}
        self._Nodisponible={}
    def añadirRecurso(self, recurso):
        if recurso._nombre in self._inventarioDisponible:
            self._inventarioDisponible[recurso._nombre]._cantidad+=recurso.cantidad
        else:
            self._inventarioDisponible[recurso._nombre]=recurso



class recurso:
    def __init__(self, nombre="", cantidad=0):
        self._nombre=nombre
        self._cantidad=cantidad

    def añadir(self):
        intentos=0
        cantidad= int (input("Ingrese la cantidad de elementos que desea añadir: "))
        
        while cantidad<0:
            print("No puedes sumar una cantidad negativa ingrese una cantidad valida : ")
            cantidad=int(input())
            if intentos==4:
                print("Se acabaron los intentos para escribir una cantidad valida cancelando proceso: ")
                return 
            intentos+=1
        self._cantidad+=cantidad

    def darBaja(self):
        intentos=0
        cantidad= int (input("Ingrese la cantidad de elementos que desea dar de baja: "))
        while cantidad:
            print("No existen tantos elementos de ese recurso ingrese otra cantidad: ")
            cantidad=int(input())
            if intentos==4:
                print("Se acabaron los intentos para escribir una cantidad valida cancelando proceso: ")
                return 
            intentos+=1
        self._cantidad-=cantidad


class libro(recurso):
    def __init__(self, nombre="", cantidad=0, autor="", fechaPublicacion=""):
        super().__init__(nombre, cantidad)
        self._autor=autor
        self._fechaPublicacion=fechaPublicacion


class equipoComputacion(recurso):
     def __init__(self, nombre="", cantidad=0, modelo=""):
            super().__init__(nombre, cantidad)
            self._modelo=modelo


      
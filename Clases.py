class persona: #clase padre que servira como base para todas las demas clases
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
            


class usuario(persona):  #clase usuario hija de persona que tendra los atributos extras sancion y objetos reservados
    def __init__(self, nombre="", apellido="", cedula=0, nombreUsuario="", contraseña="",
                 sanciones=False, objetosReservados=None):
        super().__init__(nombre, apellido, cedula, nombreUsuario, contraseña)
        self._sancion = sanciones # sirve para verificar si el usuario posee o no una sancion
        self._objetosReservados = objetosReservados or [] #lista que guarda todos los objetos Reservados que posea el usuario 
        self._buzon=[] #es un buzon de notificaciones


class Operador(persona): #clase operador hija de persona
    def __init__(self, nombre="", apellido="", cedula=0, nombreUsuario="", contraseña=""):
        super().__init__(nombre, apellido, cedula, nombreUsuario, contraseña)
    # sin iniciarSesion: la hereda de persona

    def buscador(self, registrados): #permite buscar un usuario 
        try: #se encarga de que el usuario solo pueda digitar numeros y no letras
            cedulaBuscar = int(input("Ingrese la cédula que desea buscar: ")) 
        except ValueError: #manda error si el usuario digita letras y cancela el proceso
            print("Ingrese solo números.") 
            return -1
        u = registrados.get(cedulaBuscar) #el .get(cedulabuscar) permite que el diccionario devuelva None en ves de key error si la cedula no existe
        if u is None: #determina que el usuario no existe o no esta registrado
            print("Usuario no encontrado.")
            return -1
        #segmento que escribe todos los datos del usuario
        print("Usuario encontrado:") 
        print(f"Nombre: {u._nombre}")
        print(f"Apellido: {u._apellido}")
        print(f"Cédula: {u._cedula}")
        print(f"Sanción: {u._sancion}")
        print("Objetos reservados:")
        for obj in u._objetosReservados:
            print(f" - {obj}")

    def mostrarUsuarios(self, registrados): #metodo que printea todos los usuarios registrados junto a sus datos
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
    def eliminarUsuario(self, registrados): #metodo que elimina a un usuario 
        try:
            cedulaBuscar = int(input("Ingrese la cédula del usuario que desea eliminar: "))
        except ValueError:
            print("Ingrese solo números.")
            return
        u = registrados.get(cedulaBuscar)
        if u is None:
            print("No se encontró ningún usuario con esa cédula.")
            return
        print(f"¿Desea eliminar a {u._nombre} {u._apellido} (C.C. {u._cedula})?") #se asegura de que el operador halla escrito al usuario correcto y no otro por accidente
        eleccion = input("Digite 1 para confirmar, 2 para cancelar: ")
        if eleccion == "1":
            del registrados[cedulaBuscar] #elimina al usuario 
            print("Usuario eliminado correctamente.")
            return u
        else: #cancela la accion si el usuario escribe 2 o cualquier otra cosa
            print("Acción cancelada.")
            return
    def sancionarUsuario(self, Us): #metodo que se encarga de sancionar un usuario
        if Us._sancion: #si el usuario ya esta sancionado le avisa al operador y no hace mas
            print("El usuario ya tiene una sanción activa.")
            return False
        Us._sancion = True #sanciona al usuario finalmente
        print(f"Usuario {Us._nombre} {Us._apellido} sancionado.")
        return True
    def quitarSancion(self, Us): #metodo que quita la sancion de un usuario
        if Us._sancion: #si el usuario esta sancionado le quita la sancion
            print(f"Revocando sancion a {Us._nombre} {Us._apellido}")
            Us._sancion= False
            return True
        else: #si el usuario no esta sancionado le avisa al operador y no hace nada
            print(f"El usuario {Us._nombre} {Us._apellido} no posee ninguna sancion activa")
            return False

class Inventario: #clase inventario que va a contener un diccionario de objetos de clase recurso o hijos de esta clase
    def __init__(self, inventario):
        self._inventarioDisponible = inventario or {} #guarda todos los objetos que se le ingresen en la seccion disponible y si no se le ingresa ninguno crea un diccionario vacio
        self._Nodisponible = {} #Crea un diccionario vacio donde se van a guardar los recursos cuando su cantidad llegue a 0

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

        del diccionario[nombre] #elimina el recurso
        print(f"Recurso '{nombre}' dado de baja.")
        return True    


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


      
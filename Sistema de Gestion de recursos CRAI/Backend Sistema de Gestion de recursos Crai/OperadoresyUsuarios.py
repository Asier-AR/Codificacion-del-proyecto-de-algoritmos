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
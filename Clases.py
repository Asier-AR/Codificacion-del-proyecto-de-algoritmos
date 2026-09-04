class persona:
    def __init__(self, nombre="", apellido="", cedula=0):
        self._nombre=nombre
        self._apellido=apellido
        self._cedula=cedula
    def registro(self):
        
        self._nombre=str(input("Ingrese su nombre: "))
        self._apellido=str(input("Ingrese su apellido: "))
        self._cedula=int(input("Digite su cedula: "))
        return {self._cedula:{"Nombre":self._nombre, "Apellido":self._apellido, "Cedula": self._cedula}} #devuelve un diccionario cuyo valor central es la cedula

        

class usuario(persona):
    def __init__(self, nombre="", apellido="", cedula=0, sanciones=False, objetosReservados=None): #constructor
        super().__init__(nombre, apellido, cedula)
        if objetosReservados==None:
            objetosReservados=[] #para evitar comportamientos inesperados por la mutabilidad de las listas
        self._Sancion=sanciones
        self._ObjetosReservados=objetosReservados

    def registro(self, registrados): #registra un usuario nuevo
        datos=super().registro()
        self._Sancion=False
        self._ObjetosReservados=[]
        for usuario in registrados:
            if self._cedula in usuario:
                print("Cedula ya registrada cancelando proceso")
                return None 
        return{self._cedula:{"Nombre":self._nombre, "Apellido":self._apellido, "Cedula": self._cedula,"Sancion":self._Sancion, "Objetos reservados": self._ObjetosReservados}} #devuelve un diccionario cuyo valor central es la cedula

    
class Operador(persona): #clase que hereda los metodos de la clase persona
    def __init__(self, nombre="", apellido="", cedula=0, contraseñaCuenta="", nombreUsuario=""): #constructor
        super().__init__(nombre, apellido, cedula) #hereda los atributos nombre, apellido, cedula de la clase persona
        self.nombreUsuario=nombreUsuario
        self.contraseñaCuenta=contraseñaCuenta

    def iniciarSesion(self, operadores):
        nombreUsuario = str (input("Ingrese su nombre de usuario: ")) #pide el nombre de usuario
        contraseñaCuenta =str(input("Ingrese su contraseña: ")) #pide la contraseña
        for operador in operadores:  # recorre la lista de operadores
            for cedula, datos in operador.items():  # analiza cada diccionario
                if datos["Nombre de Usuario"] == nombreUsuario and datos["Contraseña"] == contraseñaCuenta: #analiza la contraseña y los usuarios
                    print(f"Inicio de sesión exitoso. Bienvenido {datos['Nombre']} {datos['Apellido']}.")
                    return True #devuelve true si el usuario y la contraseña son correctos
        print("Usuario o contraseña incorrectos.") #si son incorrectos devuelve false
        return False


    def registro(self, operadores):
        # Llamamos al registro de la clase padre
        datos = super().registro()
        # Pedimos los atributos propios del operador
        nombreUsuario = str(input("Ingrese el nombre de usuario del operador: "))
        contraseñaCuenta = str(input("Ingrese la contraseña del operador: "))

        # Verificar duplicados
        for operador in operadores:
            # Cada "operador" es un diccionario con la forma {cedula: datos}
            for cedula, info in operador.items(): #recorre las libreria totamndo el indice y sus datos
                if self._cedula == cedula:
                    print("Cédula ya registrada, cancelando proceso")
                    return None
                while info["Nombre de Usuario"] == nombreUsuario:
                    print("Usuario ya existente, prueba con otro nombre o escribe 0 si decide salir del proceso")
                    nombreUsuario = str(input("Ingrese un nombre de usuario diferente: "))
                    if nombreUsuario=="0":
                        print("volviendo al menu de operador")
                        return
                


        datos[self._cedula]["Nombre de Usuario"] = nombreUsuario
        datos[self._cedula]["Contraseña"] = contraseñaCuenta
        return datos  # Devuelve un diccionario con los datos del operador
        

    def buscador(self, registrados):
        cedulaBuscar = int(input("Ingrese la cédula que desea buscar: "))
        for usuario in registrados:
            if cedulaBuscar in usuario:  # la cédula es la clave
                print(f"Usuario encontrado: {usuario[cedulaBuscar]}")
                return usuario[cedulaBuscar]
        print("Usuario no encontrado.")
        return None

    def mostrarUsuarios(self, registrados):
        if not registrados:
            print("No hay usuarios registrados.")

        for usuario in registrados: #recorre todas las bibliotecas guardadas en la lista usuarios
            for cedula, datos in usuario.items(): #toma el indice principal y los subindices de este indice
                print(f"Nombre: {datos['Nombre']}") #imprime los datos que guarda el diccionario en "Nombre"
                print(f"Apellido: {datos['Apellido']}") 
                print(f"Cédula: {cedula}")  
                print(f"Sanción: {datos['Sancion']}")
                print(f"Objetos reservados: {', '.join(datos['Objetos reservados'])}")
                print("-" * 30)

    def eliminarUsuario(self, registrados): 
        cedulaBuscar = int(input("Ingrese la cédula del usuario que desea eliminar: "))
        for usuario in registrados:  # usuario es un diccionario dentro de la lista
            if cedulaBuscar in usuario:  # verificamos si la cédula está en ese diccionario
                print(f"¿Este es el usuario que desea eliminar?: {usuario[cedulaBuscar]}") #printea el usuario para que no se cometan errores
                eleccion = int(input("Digite 1 si desea confirmar la acción, 2 si desea cancelar: "))
                if eleccion == 1:
                    registrados.remove(usuario)  # aquí eliminamos el diccionario de la lista
                    print("Usuario eliminado correctamente.")
                    return  #marca el fin del metodo y no se hace return de registrados porque la funcion  .remove modifica la lista registrados en memoria
                elif eleccion==2:
                    print("Acción cancelada.")
                    return #marca el fin del metodo
                else:
                    print("opcion invalida cancelando proceso")
                    return 
        print("No se encontró ningún usuario con esa cédula.")
        return #marca el fuin del metodo 
    



            
        




        




                

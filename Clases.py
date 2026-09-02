class usuario:
    def __init__(self, nombre="", apellido="", cedula=0, sanciones=False, objetosReservados=None): #constructor
        if objetosReservados==None:
            objetosReservados=[] #para evitar comportamientos inesperados por la mutabilidad de las listas
        self._Nombre=nombre
        self._Apellido=apellido
        self._Cedula=cedula
        self._Sancion=sanciones
        self._ObjetosReservados=objetosReservados

    def registro(self, nombre, apellido, cedula, sanciones=False, objetosReservados=None): #registra un usuario nuevo
        if objetosReservados==None:
            objetosReservados=[]
        self._Nombre=str(nombre)
        self._Apellido=str(apellido)
        self._Cedula=int(cedula)
        self._Sancion=sanciones
        self._ObjetosReservados=objetosReservados
        return{self._Cedula:{"Nombre":self._Nombre, "Apellido":self._Apellido, "Cedula": self._Cedula, "Objetos reservados": self._ObjetosReservados}} #devuelve un diccionario cuyo valor central es la cedula

    
class Operador(usuario): #clase que hereda los metodos de la clase usuario
    def __init__(self, nombre="", apellido="", cedula=0, contraseñaCuenta="", nombreUsuario=""): #constructor
        super().__init__(nombre, apellido, cedula) #hereda los atributos nombre, apellido, cedula de la clase usuario
        self.nombreUsuario=nombreUsuario
        self.contraseñaCuenta=contraseñaCuenta

    def iniciarSesion(self, nombreUsuario, contraseñaCuenta, operadores):
        for operador in operadores:  # recorre la lista de operadores
            for cedula, datos in operador.items():  # analiza cada diccionario
                if datos["Nombre de Usuario"] == nombreUsuario and datos["Contraseña"] == contraseñaCuenta: #analiza la contraseña y los usuarios
                    print(f"Inicio de sesión exitoso. Bienvenido {datos['Nombre']} {datos['Apellido']}.")
                    return True #devuelve ture si el usuario y la contraseña son correctos
        print("Usuario o contraseña incorrectos.") #si son incorrectos devuelve false
        return False


    def registro(self, nombre, apellido, cedula, contraseñaCuenta, nombreUsuario):
        # Llamamos al registro de la clase padre
        datos = super().registro(nombre, apellido, cedula)
        #elimina el objeto reservados de la clase usuario ya que el operador no lo usa
        datos[cedula].pop("Objetos reservados", None)
        # Añadimos los atributos propios del operador 
        datos[cedula]["Nombre de Usuario"] = nombreUsuario
        datos[cedula]["Contraseña"] = contraseñaCuenta
        return datos

    def buscador(self, registrados):
        cedulaBuscar = int(input("Ingrese la cédula que desea buscar: "))
        for usuario in registrados:
            if cedulaBuscar in usuario:  # la cédula es la clave
                print(f"Usuario encontrado: {usuario[cedulaBuscar]}")
                return usuario[cedulaBuscar]
        print("Usuario no encontrado.")
        return None
    



            
        




        



registrados=[
    {
        111111: {
            "Nombre": "Asier",
            "Apellido": "Arguinzones",
            "Cedula": 111111,
            "Sancion": False,
            "Objetos reservados": ["Libro: Cien años de soledad", "Computador portátil"]
        }}] #lista donde se guardara los usuarios registrados


operadores = [ 
    {
        333333: {
            "Nombre": "Carlos",
            "Apellido": "Pérez",
            "Cedula": 333333,
            "Sancion": False,
            "Objetos reservados": [],
            "Nombre de Usuario": "cperez",
            "Contraseña": "clave123"
        }
    }]  #Lista donde se guardaran los operadores registrados 

print("Escribe 0 si quieres cerrar el menu, 1 si quieres crear usuarios, Escribe 2 si quieres registrar operadores, 3 si quieres iniciar sesion como un operador, 4 si quieres cerrar el programa ")
y=1 #para el bucle while que permite que el menu no se cierre
z=1 #para el bucle while que permite que el menu del operador no se cierre
while (y==1):
    x=int(input())
    if x==0:
        print(f"Saliendo del menu")
        y=0

    if x==1:
        cantidadRegistro=int(input("Ingrese la cantidad de usuarios que desea registrar "))

        for k in range(cantidadRegistro):
            #recopilacion des los datos para crear un nuevo usuuario
            nombre=str(input (f"Ingrese el nombre del {k+1} usuario "))
            apellido=str(input(f"Ingrese el apellido del {k+1} usuario "))
            cedula=int(input(f"ingrese la cedula del {k+1} usuario "))
            nuevoUsuario= usuario() #crea un objeto usuario para emplear sus metodos
            datos=nuevoUsuario.registro(nombre, apellido, cedula) #crea un nuevo usuario devolviendolo en forma de diccionario
            registrados.append(datos) #añade los nuevos usuarios registrados a la lista de registro

        print("\n usuarios registrados :") #escribe la lista usuario (es solo para verificar que funciona)
        for usua in registrados: #recorre la lista de diccionarios printeandola
                print(usua) 

    elif x==2:
        cantidadRegistro=int(input("Ingresa la cantidad de operadores que desea añadir: "))
        #recopilacion de los datos necesarios para crear un  operador
        for i in range(cantidadRegistro):
            nombre = str(input(f"Ingrese el nombre del operador {i+1}: "))                     
            apellido = str(input(f"Ingrese el apellido del operador {i+1}: "))
            cedula = int(input(f"Ingrese la cédula del operador {i+1}: "))
            nombreUsuario = str(input(f"Ingrese el nombre de usuario del operador {i+1}: "))
            contraseña = str(input(f"Ingrese la contraseña del operador {i+1}: "))

            nuevoOperador = Operador() #objeto operador vacio para emplear los metodos de operador
            datos = nuevoOperador.registro(nombre, apellido, cedula, contraseña, nombreUsuario) #creacion de un nuevo operador
            operadores.append(datos) #añade los nuevos operadores en la lista de operadores

        print("\nOperadores registrados:") #escribe la lista operador (es solo para verificar que funciona)
        for op in operadores:
            print(op)

    elif x==3:
        z=1  
        op=Operador() #se crea un objeto vacio para emplear los metodos
        nombreUsuario=str(input("Ingrese su nombre de usuario ")) #pide el nombre de usuario
        contraseña=str(input("Ingrese su contraseña ")) #pide la contraseña
        if (op.iniciarSesion(nombreUsuario, contraseña, operadores)==True): #se usa lo que devuelve el metodo iniciar sesion del operador para permitir el acceso en el menu del operador
            print ("Escribe 0 si quieres salir del menu del operador, 1 si quieres buscar un usuario especifico")  
            while z!=0:
                h=int(input())
                if h==0:
                    print(f"Saliendo del menu")
                    z=0
                elif h==1:
                    op.buscador(registrados)
                

#Aun falta la implementacion de una verificacion para evitar usuarios de operadores repetidos y cedulas repetidas en los registros.
# ademas de la implementacion de la clase objetos que es la que va a permitir hacer las reservas 
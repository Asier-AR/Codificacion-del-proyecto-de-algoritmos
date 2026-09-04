from Clases import persona, usuario, Operador

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
            "Nombre de Usuario": "cperez",
            "Contraseña": "clave123"
        }
    }]  #Lista donde se guardaran los operadores registrados 

print("Escribe: ")
print("0 si quieres cerrar el menu")
print("1 si quieres crear usuarios")  
print("2 si quieres iniciar sesion como un operador")
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
            nuevoUsuario= usuario() #crea un objeto usuario para emplear sus metodos
            datos=nuevoUsuario.registro(registrados) #crea un nuevo usuario devolviendolo en forma de diccionario
            registrados.append(datos) #añade los nuevos usuarios registrados a la lista de registro

    elif x==2:
        z=1  
        op=Operador() #se crea un objeto vacio para emplear los metodos
        if (op.iniciarSesion(operadores)==True): #se usa lo que devuelve el metodo iniciar sesion del operador para permitir el acceso en el menu del operador
            print ("Escribe") 
            print("0 si quieres salir del menu del operador") 
            print ("1 si quieres buscar un usuario especifico") 
            print("2 si quieres registrar un nuevo operador")
            print("3 si quiere mostrar a todos los usuarios")
            print("4 si quiere eliminar un usuario")
            while z!=0 and z!=-1:
                h=int(input())
                if h==0:
                    print(f"Saliendo del menu")
                    z=0
                elif h==1:
                    op.buscador(registrados)
                elif h==2:

                    cantidadRegistro=int(input("Ingresa la cantidad de operadores que desea añadir: "))
                    for i in range(cantidadRegistro):
                        datos=op.registro(operadores)
                        operadores.append(datos) #añade los nuevos operadores en la lista de operadores
                elif h==3:
                    op.mostrarUsuarios(registrados)
                elif h==4:
                    op.eliminarUsuario(registrados)
                else:
                    print("Opcion no valida saliendo del menu")
                    z=-1
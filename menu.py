from Clases import *


def pedirNumero(mensaje): #se asegura que no hayan entradas raras como letras al momento de elegir las opciones
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingrese solo números.")


def registro(): #permite crear una lista con los datos primarios para crear un objeto ya sea de tipo operador o de tipo usuario
    nombre = input("Ingrese su nombre (mínimo 3 letras, sin números, espacios ni símbolos): ")
    while len(nombre) < 3 or not nombre.isalpha(): #el metodo isalpha lo que hace es devolver true si el metodo solo posee letras sin ningun caracter especial como $ o !
        nombre = input("Nombre no válido, ingréselo de nuevo: ")

    apellido = input("Ingrese su primer apellido (mínimo 3 letras, sin números, espacios ni símbolos): ")
    while len(apellido) < 3 or not apellido.isalpha():
        apellido = input("Apellido no válido, ingréselo de nuevo: ")

    cedula = pedirNumero("Digite su cédula (debe contener minimo 6 digitos y maximo 10 digitos): ")
    while len(str(cedula))<6 or len(str(cedula))>10 or "-" in str(cedula):
        cedula = pedirNumero("Cédula no válida (mínimo 6 dígitos y maximo 10), ingrésela de nuevo: ")

    nombreUsuario = input("Ingrese su nombre de usuario (mínimo 3 caracteres, sin espacios): ")
    while len(nombreUsuario) < 3 or " " in nombreUsuario:
        nombreUsuario = input("Nombre de usuario muy corto o con espacios, ingrese otro: ")

    contraseña = input("Ingrese su contraseña (mínimo 5 caracteres, sin espacios): ")
    while len(contraseña) < 5 or " " in contraseña:
        contraseña = input("Contraseña muy corta o con espacios, ingrese otra: ")

    return nombre, apellido, cedula, nombreUsuario, contraseña


def menuOperador(Op, usuarios, operadores): #printea las opciones y ejecuta el menu del operador
    while True:
        print("\n--- MENÚ OPERADOR ---")
        print("0. Salir del menú del operador")
        print("1. Buscar un usuario")
        print("2. Registrar un nuevo operador")
        print("3. Mostrar todos los usuarios")
        print("4. Eliminar un usuario")
        h = pedirNumero("Opción: ")

        if h == 0:
            print("Saliendo del menú del operador")
            break
        elif h == 1:
            Op.buscador(usuarios)
        elif h == 2:
            nombre, apellido, cedula, nombreUsuario, contraseña = registro()
            if cedula in operadores:
                print("Cédula ya registrada, cancelando proceso.")
            else:
                operadores[cedula] = Operador(nombre, apellido, cedula, nombreUsuario, contraseña)
                print("Operador registrado correctamente.")
        elif h == 3:
            Op.mostrarUsuarios(usuarios)
        elif h == 4:
            Op.eliminarUsuario(usuarios)
        else:
            print("Opción no válida.")

def menuUsuario(Us): #es el menu de los usuarios a dia de hoy esta en proceso
    while True:
        print("\n--- MENÚ Usuario ---")
        print("0. Salir del menú del Usuario")
        print("1. Realizar un prestamo")
        print("2. Revisar datos propios")
        print("3. Devolver un objeto")
        h = pedirNumero("Opción: ")

        if h==0:
            print("Volviendo al menu principal")
            break

usuarios = { #diccionario de objetos de clase usuario
    1398765820: usuario("Ana", "Pérez", 1001, "ana", "ana123"),
    1002256804: usuario("Luis", "Gómez", 1002, "luis", "luis123", sanciones=True, objetosReservados=["Balón", "Raqueta"]),
    1003456789: usuario("Marta", "Rojas", 1003, "marta", "marta123", objetosReservados=["Ajedrez"]),
}

operadores = { #diccionario de objetos de clase operador
    1098736417: Operador("Admin", "Sistema", 1, "admin", "1234"),
    2239467890: Operador("Carlos", "Díaz", 2, "carlos", "op2024"),
}

while True: #menu principal
    print("\n--- MENÚ PRINCIPAL ---")
    print("0. Cerrar el menú")
    print("1. Registrar un usuario")
    print ("2. Iniciar sesión como usuario")
    print("3. Iniciar sesión como operador")
    x = pedirNumero("Opción: ")

    if x == 0:
        print("Saliendo del menú")
        break
    elif x == 1:
        nombre, apellido, cedula, nombreUsuario, contraseña = registro()
        if cedula in usuarios:
            print("Cédula ya registrada, cancelando proceso.")
        else:
            usuarios[cedula] = usuario(nombre, apellido, cedula, nombreUsuario, contraseña)
            print("Usuario registrado correctamente.")

    elif x==2:
        Us=None
        for k in range (4):
            cedula= pedirNumero("Ingrese su numero de cedula: ")
            if cedula in usuarios:
                Us= usuarios[cedula]
                break
            print(f"Cédula no encontrada. Intentos restantes: {3 - k}")
        else:
            print("Intentos agotados para ingresar una cédula válida, volviendo al menú.")

        if Us is not None and Us.iniciarSesion():
            menuUsuario(Us)

    elif x == 3:
        Op = None
        for k in range(4):
            cedula = pedirNumero("Ingrese su número de cedula: ")
            if cedula in operadores: #chequea que la cedula que se realize exista y este registrada
                Op = operadores[cedula] #designa el objeto operador con todos los datos internos
                break
            print(f"Cédula no encontrada. Intentos restantes: {3 - k}") #determina el numero de intentos para ingresar la cedula
        else:
            print("Intentos agotados para ingresar una cédula válida, volviendo al menú.")

        if Op is not None and Op.iniciarSesion(): #revisa que se haya iniciado sesion y que el paso de la cedula se haya realizado
            menuOperador(Op, usuarios, operadores)
    else:
        print("="*50 )
        print("Opción no válida.") #evita que se escriban cosas como 5 que no tengan opcion
        print ("="*50)
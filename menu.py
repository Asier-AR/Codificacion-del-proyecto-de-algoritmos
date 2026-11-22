from FuncionesMenu import *

while True: #menu principal
    print("\n--- MENÚ PRINCIPAL ---")
    print("0. Cerrar el menú")
    print("1. Registrarse como usuario")
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
        elif cedula in usuariosBaja:
            print("Esta cedula ya existe pero la cuenta esta desactivada, contacte un operador para mas informacion")
        else:
            nuevoUs = usuario(nombre, apellido, cedula, nombreUsuario, contraseña)
            usuarios[cedula] = nuevoUs
            confirmarRegistro("usuario", usuarios, cedula, nuevoUs) #aqui aun no hay sesion iniciada, asi que se confirma o se deshace al instante

    elif x==2:
        Us=None
        while True:
            cedula= pedirNumero("Ingrese su numero de cedula o ingrese 0 si desea cancelar el proceso: ")
            if cedula in usuarios:
                Us= usuarios[cedula]
                break
            elif cedula in usuariosBaja:
                print("Cuenta desactivada, contacte con un operador para mas informacion.")
                break

            elif cedula==0:
                print("Cancelando el proceso volviendo al menu")
                break

            print(f"Cédula no encontrada")


        if Us is not None and Us.iniciarSesion():
            menuUsuario(Us, sistema, usuarios)

    elif x == 3:
        Op = None
        while True:
            cedula = pedirNumero("Ingrese su número de cedula o escriba 0 si desea cancelar el proceso: ")
            if cedula in operadores: #chequea que la cedula que se realize exista y este registrada
                Op = operadores[cedula] #designa el objeto operador con todos los datos internos
                break
            elif cedula==0:
                print("Cancelando el proceso volviendo al menu")
                break

        if Op is not None and Op.iniciarSesion(): #revisa que se haya iniciado sesion y que el paso de la cedula se haya realizado
            menuOperador(Op, usuarios, operadores, sistema, usuariosBaja)
    else:
        print("="*50 )
        print("Opción no válida.") #evita que se escriban cosas como 5 que no tengan opcion
        print ("="*50)
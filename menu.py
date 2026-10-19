from Clases import *
from Prestamos import *
from Registros import *
from deshacer import *

inventario = Inventario(sistemaInventario_dict)   # envuelve el diccionario de Registros.py en un objeto Inventario
sistema = SistemaPrestamos(inventario) #crea un objeto de la clase sistema de prestamos

historiales = {}   # una pila de deshacer por persona: ("us", cedula) o ("op", cedula)

def historialDe(tipo, cedula): #devuelve la pila de deshacer de una persona, y la crea si es la primera vez
    clave = (tipo, cedula)
    if clave not in historiales:
        historiales[clave] = HistorialOperaciones()
    return historiales[clave]

sistema._obtenerHistorial = historialDe #NUEVO: asi el sistema sabe en que pila apilar los prestamos que salen de la lista de espera
sistema._usuarios = usuarios #NUEVO: asi el sistema puede atender la lista de espera cuando se anula un prestamo

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

def confirmarRegistro(tipo, diccionario, cedula, persona): #muestra los datos y deja deshacer el registro si hubo un error (por ejemplo en la cédula)
    print("\nDatos registrados:")
    print(f"  Nombre: {persona._nombre} {persona._apellido}")
    print(f"  Cédula: {persona._cedula}")
    print(f"  Usuario: {persona._nombreUsuario}")
    eleccion = input("¿Son correctos? Digite 1 para confirmar, 2 para deshacer el registro: ")
    while eleccion not in ("1", "2"): #NUEVO: antes cualquier tecla distinta de 2 confirmaba el registro, ahora se repite la pregunta hasta que escriba 1 o 2
        eleccion = input("Opción inválida, digite 1 para confirmar o 2 para deshacer el registro: ")
    if eleccion == "2":
        if OpRegistro(tipo, diccionario, cedula, persona).deshacer(): #reutiliza la operacion de deshacer registro
            print("Registro deshecho. Puede registrarse de nuevo con los datos correctos.")
        return False
    print("Registro confirmado.")
    return True

def registrarRecurso(): #permite registrar un recurso
    print("¿Qué tipo de recurso desea añadir?")
    print("1. Equipo de computación")
    print("2. Libro")
    print("3. Recurso varios")
    h = pedirNumero("Opción: ")
    while h not in (1, 2, 3):
        h = pedirNumero("Opción inválida, escriba 1, 2 o 3: ")

    nombre = input("Ingrese el nombre del recurso: ").strip().lower()
    while nombre == "":
        nombre = input("El nombre no puede estar vacío, ingréselo de nuevo: ").strip().lower() #el metodo strip elimina todos los espacios y tabulaciones en los nombres tanto como en la izquierda como por la derecha

    cantidad = pedirNumero("Ingrese la cantidad que desea añadir: ")
    while cantidad <= 0:
        cantidad = pedirNumero("La cantidad debe ser mayor que cero, intente de nuevo: ")

    if h == 1:
        modelo = input("Ingrese el modelo del equipo: ")
        return equipoComputacion(nombre, cantidad, modelo)
    elif h == 2:
        autor = input("Ingrese el autor del libro: ")
        fecha = input("Ingrese el año de publicación (por ejemplo 1918): ")
        return libro(nombre, cantidad, autor, fecha)
    else:
        return recurso(nombre, cantidad)

def menuOperador(Op, usuarios, operadores, sistema, inventario): #printea las opciones y ejecuta el menu del operador
    historial = historialDe("op", Op._cedula) #pila de deshacer propia de este operador
    while True:
        print("\n--- MENÚ OPERADOR ---")
        print("0. Salir del menú del operador")
        print("1. Buscar un usuario")
        print("2. Registrar un nuevo operador")
        print("3. Mostrar todos los usuarios")
        print("4. Sancionar a un usuario")
        print("5. Quitar sancion a un usuario")
        print("6. Añadir un nuevo recurso")
        print("7. Eliminar un usuario")
        print("8. Mostar historial de los recursos")
        print("9. Dar de baja un recurso ")
        print("10. Deshacer la última operación")
        h = pedirNumero("Opción: ")

        if h == 0:
            print("Saliendo del menú del operador")
            break
        elif h == 1:
            Op.buscador(usuarios) #permite buscar un usuario
        elif h == 2:
            nombre, apellido, cedula, nombreUsuario, contraseña = registro() #permite registrar un operador
            if cedula in operadores:
                print("Cédula ya registrada, cancelando proceso.")
            else:
                nuevoOp = Operador(nombre, apellido, cedula, nombreUsuario, contraseña)
                operadores[cedula] = nuevoOp
                if confirmarRegistro("operador", operadores, cedula, nuevoOp): #si lo confirma, queda en la pila para poder deshacerlo despues
                    historial.registrar(OpRegistro("operador", operadores, cedula, nuevoOp))
        elif h == 3: #permite printear todos los usuarios
            Op.mostrarUsuarios(usuarios)
        elif h==4: #permite sancionar un usuario usando su numero de cedula
            cedula= pedirNumero("Ingrese la cedula del usuario: ")
            if cedula in usuarios:
                Us=usuarios[cedula]
                print(f"Esta seguro que quiere sancionar al usuario {Us._nombre} {Us._apellido}")
                eleccion=str (input("Escribe 1 para aceptar, 2 para cancelar: "))
                if eleccion=="1":
                    if Op.sancionarUsuario(Us): #solo se apila si de verdad se sanciono
                        historial.registrar(OpSancion(Us, False))
                elif eleccion=="2":
                    print("cancelando proceso ")
                else:
                    print("Opcion invalida cancelando proceso")
            else:
                print("La cedula que se introdujo no esta registrada")
        elif h==5:
            cedula=pedirNumero("Ingrese la cedula del usuario: ")
            if cedula in usuarios: #revisa que la cedula existe
                Us=usuarios[cedula]
                print(f"Esta seguro que quiere revocar la sancion del usuario {Us._nombre} {Us._apellido}")
                eleccion=str (input("Escribe 1 para aceptar, 2 para cancelar: "))
                if eleccion=="1":
                    if Op.quitarSancion(Us): #quita la sancion y, si hubo cambio, se apila para poder deshacerlo
                        historial.registrar(OpSancion(Us, True))
                elif eleccion=="2":
                    print("cancelando proceso ")
                else:
                    print("Opcion invalida cancelando proceso")
            else:
                print("La cedula que se introdujo no esta registrada")
        elif h==6:
            nuevo=registrarRecurso()
            eraNuevo = nuevo._nombre not in inventario._inventarioDisponible and nuevo._nombre not in inventario._Nodisponible #se revisa antes de añadir, para saber si el recurso ya existia
            inventario.añadirRecurso(nuevo)
            historial.registrar(OpAnadirRecurso(inventario, nuevo._nombre, nuevo._cantidad, eraNuevo))
            sistema.atenderEspera(nuevo._nombre, usuarios, historial) #los prestamos de la espera quedan en la pila de deshacer de cada usuario que los recibe, no en la del operador
        elif h == 7:
            eliminado = Op.eliminarUsuario(usuarios) #devuelve el usuario eliminado o None si no se elimino nada
            if eliminado is not None:
                historial.registrar(OpEliminarPersona("usuario", usuarios, eliminado._cedula, eliminado))

        elif h==8:
            nombre= input("Ingrese el nombre del recurso: ").strip().lower()
            sistema.verHistorialRecurso(nombre)

        elif h==9:
            nombre= input("Ingrese el nombre del recurso al que desea dar de baja : ").strip().lower()
            if sistema.tienePrestamosActivos(nombre):
                print("No se puede dar de baja el recurso porque aun hay prestamos activos ")
            else:
                estabaDisponible = nombre in inventario._inventarioDisponible #se guarda donde estaba para devolverlo ahi si se deshace
                rec = inventario._inventarioDisponible.get(nombre) if estabaDisponible else inventario._Nodisponible.get(nombre)
                if inventario.darDeBajaRecurso(nombre): #solo se apila si de verdad se dio de baja
                    historial.registrar(OpBajaRecurso(inventario, rec, estabaDisponible))

        elif h == 10:
            historial.confirmarYDeshacer() #muestra la ultima operacion y pide confirmacion

        else:
            print("="*50 )
            print("Opción no válida.") #evita que se escriban cosas como 5 que no tengan opcion
            print ("="*50)

def menuUsuario(Us, sistema, inventario, usuarios): #es el menu de los usuarios a dia de hoy esta en proceso
    historial = historialDe("us", Us._cedula) #pila de deshacer propia de este usuario
    if Us._buzon: #NUEVO: al entrar avisa si hay notificaciones sin leer
        print(f"\nTienes {len(Us._buzon)} notificación(es) nueva(s). Revísalas en la opción 7.")
    while True:
        print(f"\n--- MENÚ Usuario de: {Us._nombre} ---")
        print("0. Salir del menú del Usuario")
        print("1. Ver recursos disponibles ")
        print("2. Realizar un prestamo")
        print("3. Revisar datos propios")
        print("4. Devolver un objeto")
        print("5. Ver historial de usuario")
        print("6. Deshacer mi última acción")
        print("7. Ver notificaciones") #NUEVO
        h = pedirNumero("Opción: ")

        if h==0:
            print("Volviendo al menu principal")
            return

        elif h==1:
            for nombre, objeto in inventario._inventarioDisponible.items():
                print(f"Nombre: {nombre}")
                print(f"  Cantidad: {objeto._cantidad}")
            for nombre in inventario._Nodisponible:
                print(f"Nombre: {nombre}")
                print("  Agotado (puede unirse a la lista de espera)")
        elif h==2:
            Recurso=input("Ingrese el recurso que desea reservar ").strip().lower() #NUEVO: strip quita espacios sobrantes para que no falle por un espacio al final

            sistema.prestar(Us, Recurso, historial) #se le pasa la pila para que el prestamo (o la espera) se pueda deshacer
        elif h==3:
            print(f"Nombre: {Us._nombre} \n Apellido: {Us._apellido} \n Nombre de usuario: {Us._nombreUsuario} \n Recursos Reservados: {Us._objetosReservados} \n Sancion: {Us._sancion}")
        elif h == 4:
            activos = sistema.prestamosActivos(Us)
            if not activos:
                print("No tienes préstamos activos.")

            else:
                for p in activos:
                    print(" -", p)
                numero = pedirNumero("Número del préstamo a devolver: ")
                sistema.devolver(Us, numero, usuarios, historial) #la devolucion tambien queda en la pila
        elif h==5:
            sistema.verHistorialUsuario(Us)
        elif h==6:
            historial.confirmarYDeshacer() #muestra la ultima accion del usuario y pide confirmacion
        elif h==7: #NUEVO: muestra las notificaciones del buzon (por ejemplo, que lo sacaron de una lista de espera por una sancion)
            if not Us._buzon:
                print("No tienes notificaciones.")
            else:
                for aviso in Us._buzon:
                    print(" -", aviso)
                Us._buzon.clear() #una vez leidas se vacia el buzon
        else:
            print("="*50 )
            print("Opción no válida.") #evita que se escriban cosas como 5 que no tengan opcion
            print ("="*50)
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
        else:
            nuevoUs = usuario(nombre, apellido, cedula, nombreUsuario, contraseña)
            usuarios[cedula] = nuevoUs
            confirmarRegistro("usuario", usuarios, cedula, nuevoUs) #aqui aun no hay sesion iniciada, asi que se confirma o se deshace al instante

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
            menuUsuario(Us, sistema, inventario, usuarios)

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
            menuOperador(Op, usuarios, operadores, sistema, inventario)
    else:
        print("="*50 )
        print("Opción no válida.") #evita que se escriban cosas como 5 que no tengan opcion
        print ("="*50)
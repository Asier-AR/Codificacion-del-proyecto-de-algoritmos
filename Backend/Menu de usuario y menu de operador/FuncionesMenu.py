from UsuariosOperadores import Operador, usuario
from Inventarios import Inventario, libro, equipoComputacion, recurso
from SistemaSedes import Sede, SistemaSede
from deshacer import (
    Pila,
    Operacion,
    OpRegistro,
    OpEliminarPersona,
    OpSancion,
    OpAnadirRecurso,
    OpBajaRecurso,
    OpPrestamo,
    OpDevolucion,
    OpListaEspera,
    HistorialOperaciones,
)
from Prestamos import Prestamo, SistemaPrestamos
from Registros import (
    usuarios,
    usuariosBaja,
    sistemaInventario_dict1,
    sistemaInventario_dict2,
    sistemaInventario_dict3,
    sistemaInventario_dict4,
    historialPrestamos,
    operadores,
    inventario1,
    inventario2,
    inventario3,
    inventario4,
    sedeCentro,
    sedeNorte,
    sedeSur,
    sedeEmprendimiento,
    sedes,
    conexiones,
    SistemaSedes,
)
from ordenamientos import (
    sinTildes,
    categoriaDe,
    FilaRecurso,
    burbuja,
    insercion,
    mergeSort,
    quickSort,
    crearFilas,
    ordenarRecursos,
    mostrarRecursos,
    FilaConteo,
    informePrestamos,
)

sistema = SistemaPrestamos(SistemaSedes) #crea un objeto de la clase sistema de prestamos

def elegirCategoria(sistema, sedes, atributo):
    categorias = []
    for nombreSede in sedes:
        for c in getattr(sistema._inv(nombreSede), atributo):
            if c not in categorias:
                categorias.append(c)
    if not categorias:
        print("No hay categorías en esa selección.")
        return None
    for i, c in enumerate(categorias, 1):
        print(f"{i}. {c}")
    num = pedirNumero("Ingrese el numero de la categoria: ")
    while num < 1 or num > len(categorias):
        num = pedirNumero("Numero no valido, intente de nuevo: ")
    return categorias[num - 1]


def imprimirRecurso(inv, x):          # evita repetir el bloque de impresión
    if x in inv._inventarioDisponible:
        obj = inv._inventarioDisponible[x]
        cantidad = obj._cantidad
    else:
        obj = inv._Nodisponible[x]
        cantidad = "Agotado (puede unirse a la lista de espera)"
    print(f"Nombre: {x}")
    if isinstance(obj, libro):
        print(f"Autor: {obj._autor}")
        print(f"Fecha de publicacion: {obj._fechaPublicacion}")
    elif isinstance(obj, equipoComputacion):
        print(f"Modelo: {obj._modelo}")
    print(f"Cantidad: {cantidad}\n")


def mostrarInventario(sistema):
    sedes = list(sistema._sistemaSede._sedes)
    eleccion = input("¿Desea buscar en alguna sede en especifico? (S/N) ").lower().strip()
    if eleccion in ("s", "si"):
        sedes = [elegirSede(sistema)]
    else:
        print("Se mostrara el inventario de todas las sedes.")

    print("Que tipo de articulo desea ver.")
    print("1. Libros\n2. Equipo de computacion\n3. Otros")
    filtro = pedirNumero("Cualquier otro numero muestra todo: ")
    atributos = {1: "_libro", 2: "_Equipo"}

    categoria = None
    if filtro in atributos:
        if input("¿Desea filtrar por una categoria? (S/N) ").lower().strip() in ("s", "si"):
            categoria = elegirCategoria(sistema, sedes, atributos[filtro])
            if categoria is None:
                return

    for nombreSede in sedes:
        inv = sistema._inv(nombreSede)
        print("\n" + "=" * 20, nombreSede, "=" * 20)
        if filtro in atributos:
            arbol = getattr(inv, atributos[filtro])
            for cat, nombres in arbol.items():
                if categoria is not None and cat != categoria:
                    continue
                print(f"--- {cat} ---")
                for x in nombres:
                    imprimirRecurso(inv, x)
        elif filtro == 3:
            for x in inv._Otros:
                imprimirRecurso(inv, x)
        else:
            for x in list(inv._inventarioDisponible) + list(inv._Nodisponible):
                imprimirRecurso(inv, x)
        


            



def elegirSede(sistema):
    nombres = list(sistema._sistemaSede._sedes)
    for i, n in enumerate(nombres, 1):
        print(f"{i}. {n}")
    num = pedirNumero("Numero de la sede: ")
    while num < 1 or num > len(nombres):
        num = pedirNumero("Numero no valido, intente de nuevo: ")
    return nombres[num - 1]





def cargarHistorial(sistema):
    for numero, cedula, nombreRecurso, fechaPrestamo, fechaDevolucion in historialPrestamos:
        Us = usuarios[cedula]
        sede = next(s for s in sistema._sistemaSede._sedes
                    if nombreRecurso in sistema._inv(s)._inventarioDisponible
                    or nombreRecurso in sistema._inv(s)._Nodisponible)
        inv = sistema._inv(sede)
        rec = inv._inventarioDisponible.get(nombreRecurso) or inv._Nodisponible[nombreRecurso]

        p = Prestamo(numero, Us, rec, sede)
        p._fechaPrestamo = fechaPrestamo
        if fechaDevolucion != "":
            p._estado = "Devuelto"
            p._fechaDevolucion = fechaDevolucion
        else:
            rec._cantidad -= 1
            Us._objetosReservados.append(nombreRecurso)

        sistema._historialUsuarios.setdefault(cedula, []).append(p)
        sistema._historialRecursos.setdefault((sede, nombreRecurso), []).append(p)

    sistema._contador = len(historialPrestamos)

    for sede in sistema._sistemaSede._sedes:      # lo que quedó en 0 pasa a agotados
        inv = sistema._inv(sede)
        for n in list(inv._inventarioDisponible):
            if inv._inventarioDisponible[n]._cantidad == 0:
                inv._Nodisponible[n] = inv._inventarioDisponible.pop(n)

cargarHistorial(sistema) #carga los 200 prestamos de Registros.py

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
        categoria = input("Ingrese la categoría del equipo: ")
        return equipoComputacion(nombre, cantidad, modelo, categoria)
    elif h == 2:
        autor = input("Ingrese el autor del libro: ")
        fecha = input("Ingrese el año de publicación (por ejemplo 1918): ")
        categoria = input("Ingrese la categoría del libro: ")
        return libro(nombre, cantidad, autor, fecha, categoria)
    else:
        return recurso(nombre, cantidad)

def verDisponibilidad(sistema):
    nombreSede=elegirSede(sistema)
    Nombre=input("Ingrese el nombre del recurso: ").strip().lower()
    inventario=sistema._inv(nombreSede)
    if Nombre in inventario._inventarioDisponible:
        print(f"El recurso {Nombre} se encuentra disponible y se tiene un stock de: {inventario._inventarioDisponible[Nombre]._cantidad}")
    elif Nombre in inventario._Nodisponible:
        print(f"El recurso si existe en la {nombreSede} pero no se encuentra disponible en este momento")
        sistema._sistemaSede.buscarEnOtrasSedes(nombreSede, Nombre)
    else:
        sistema._sistemaSede.buscarEnOtrasSedes(nombreSede, Nombre)

def menuOperador(Op, usuarios, operadores, sistema, usuariosBaja): #printea las opciones y ejecuta el menu del operador
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
        print("9. Dar de baja un recurso.")
        print("10. Deshacer la última operación.")
        print("11. Listar recursos ordenados.")
        print("12. Mostrar listado de prestamos")
        print("13. Ver disponibilidad de un recurso")
        print("14. Registrar devolucion.")
        h = pedirNumero("Opción: ")

        if h == 0:
            print("Saliendo del menú del operador")
            break
        elif h == 1:
            Op.buscador(usuarios, usuariosBaja) #permite buscar un usuario
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
            Op.mostrarUsuarios(usuarios, usuariosBaja)
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
                print("La cedula que se introdujo no esta registrada, o la cuenta del usuario esta desactivada")
        elif h==6:
            sede=elegirSede(sistema)
            inventario=sistema._inv(sede)
            nuevo=registrarRecurso()
            eraNuevo = nuevo._nombre not in inventario._inventarioDisponible and nuevo._nombre not in inventario._Nodisponible #se revisa antes de añadir, para saber si el recurso ya existia
            inventario.añadirRecurso(nuevo)
            historial.registrar(OpAnadirRecurso(inventario, nuevo._nombre, nuevo._cantidad, eraNuevo))
            sistema.atenderEspera(sede, nuevo._nombre, usuarios, historial) #los prestamos de la espera quedan en la pila de deshacer de cada usuario que los recibe, no en la del operador
        elif h == 7:
            eliminado = Op.eliminarUsuario(usuarios) #devuelve el usuario eliminado o None si no se elimino nada
            if eliminado is not None:
                usuariosBaja[eliminado._cedula]=eliminado
                historial.registrar(OpEliminarPersona("usuario", usuarios, eliminado._cedula, eliminado, usuariosBaja))

        elif h==8:
            sede=elegirSede(sistema)
            nombre= input("Ingrese el nombre del recurso: ").strip().lower()
            sistema.verHistorialRecurso(sede, nombre)

        elif h==9:
            sede=elegirSede(sistema)
            inventario=sistema._inv(sede)
            nombre= input("Ingrese el nombre del recurso al que desea dar de baja : ").strip().lower()
            if sistema.tienePrestamosActivos(sede, nombre):
                print("No se puede dar de baja el recurso porque aun hay prestamos activos ")
            else:
                estabaDisponible = nombre in inventario._inventarioDisponible #se guarda donde estaba para devolverlo ahi si se deshace
                rec = inventario._inventarioDisponible.get(nombre) if estabaDisponible else inventario._Nodisponible.get(nombre)
                if inventario.darDeBajaRecurso(nombre): #solo se apila si de verdad se dio de baja
                    historial.registrar(OpBajaRecurso(inventario, rec, estabaDisponible))

        elif h == 10:
            historial.confirmarYDeshacer() #muestra la ultima operacion y pide confirmacion
        
        elif h==11:
            
            print("Desea ver los recurso de \n 1. Todas las sedes \n 2. Una sede")
            eleccion=pedirNumero("Escriba el numero que aparece alfrente de la opcion: ")
            if eleccion==2:
                sede=[elegirSede(sistema)]
            else:
                sede=list(sistema._sistemaSede._sedes)

            print("Ordenar por: \n 1. Mas prestados \n 2. antiguedad \n 3. categoria\n 4. estado ")
            criterio=pedirNumero("Opcion: ")
            criterios = {1: "prestamos", 2: "antiguedad", 3: "categoria", 4: "estado"}
            while criterio not in criterios:
                criterio=pedirNumero("Opcion no valida intentelo de nuevo: ")
            invertir = input("¿Invertir el orden? (S/N): ").strip().lower() in ("s", "si") # el in ocaciona devuelve verdadero si el usuario escribe s o si, 
            # pero si escribe cualquier otra cosa devuelve falso
            limite = pedirNumero("Cuántas filas mostrar (0 = todas): ")
            filas, algoritmo, segundos = ordenarRecursos(sistema, sede, criterios[criterio], invertir)
            mostrarRecursos(filas, limite)
            print(f"Ordenado con {algoritmo} en {segundos:.6f} s")
            
        elif h == 12:
            limite = pedirNumero("Cuántos objetos mostrar (0 = todos): ")
            informePrestamos(sistema, limite)         

        elif h==13:
            verDisponibilidad(sistema)
        elif h==14:
            cedulaBuscar=pedirNumero("Porfavor ingrese la cedula del usuario que va a registrar su devolucion ")
            if cedulaBuscar in usuarios:
                Us=usuarios[cedulaBuscar]
                historialUs = historialDe("us", Us._cedula)
                activos = sistema.prestamosActivos(Us)
                if not activos:
                    print("El usuario no tiene préstamos activos.")

                else:
                    for p in activos:
                        print(" -", p)
                    numero = pedirNumero("Número del préstamo a devolver: ")
                    sistema.devolver(Us, numero, usuarios, historialUs) #la devolucion tambien queda en la pila

            else:
                print("Cedula no existente o dada de baja: ")

        else:
            print("="*50 )
            print("Opción no válida.") #evita que se escriban cosas que no tengan opcion
            print ("="*50)




def menuUsuario(Us, sistema, usuarios): #es el menu de los usuarios a dia de hoy esta en proceso
    historial = historialDe("us", Us._cedula) #pila de deshacer propia de este usuario
    if Us._buzon: #NUEVO: al entrar avisa si hay notificaciones sin leer
        print(f"\nTienes {len(Us._buzon)} notificación(es) nueva(s). Revísalas en la opción 7.")
    while True:
        print(f"\n--- MENÚ Usuario de: {Us._nombre} ---")
        print("0. Salir del menú del Usuario")
        print("1. Ver inventarios ")
        print("2. Ver disponibilidad de un recurso")
        print("3. Realizar un prestamo")
        print("4. Revisar datos propios")
        print("5. Ver historial de usuario")
        print("6. Deshacer mi última acción")
        print("7. Ver notificaciones") #NUEVO
        h = pedirNumero("Opción: ")

        if h==0:
            print("Volviendo al menu principal")
            return

        elif h==1:
           mostrarInventario(sistema)
        elif h==2:
            verDisponibilidad(sistema)
                


        elif h==3:
            sede=elegirSede(sistema)

            Recurso=input("Ingrese el recurso que desea reservar ").strip().lower() #NUEVO: strip quita espacios sobrantes para que no falle por un espacio al final

            sistema.prestar(Us, sede, Recurso, historial) #se le pasa la pila para que el prestamo (o la espera) se pueda deshacer
        elif h==4:
            print(f"Nombre: {Us._nombre} \n Apellido: {Us._apellido} \n Nombre de usuario: {Us._nombreUsuario} \n Recursos Reservados: {Us._objetosReservados} \n Sancion: {Us._sancion}")

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
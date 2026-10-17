from Clases import *
from Prestamos import *

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

def registrarRecurso():
    print("¿Qué tipo de recurso desea añadir?")
    print("1. Equipo de computación")
    print("2. Libro")
    print("3. Recurso varios")
    h = pedirNumero("Opción: ")
    while h not in (1, 2, 3):
        h = pedirNumero("Opción inválida, escriba 1, 2 o 3: ")

    nombre = input("Ingrese el nombre del recurso: ").strip()
    while nombre == "":
        nombre = input("El nombre no puede estar vacío, ingréselo de nuevo: ").strip() #el metodo strip elimina todos los espacios y tabulaciones en los nombres tanto como en la izquierda como por la derecha

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
        

        




def menuOperador(Op, usuarios, operadores, sistema): #printea las opciones y ejecuta el menu del operador
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
        elif h==4:
            cedula= pedirNumero("Ingrese la cedula del usuario: ")
            if cedula in usuarios:
                Us=usuarios[cedula]
                print(f"Esta seguro que quiere sancionar al usuario {Us._nombre} {Us._apellido}")
                eleccion=str (input("Escribe 1 para aceptar, 2 para cancelar: "))
                if eleccion=="1":
                    Op.sancionarUsuario(Us)
                elif eleccion=="2":
                    print("cancelando proceso ")
                else:
                    print("Opcion invalida cancelando proceso")
            else: 
                print("La cedula que se introdujo no esta registrada")
        elif h==5:
            cedula=pedirNumero("Ingrese la cedula del usuario: ")
            if cedula in usuarios:
             Us=usuarios[cedula]
             print(f"Esta seguro que quiere revocar la sancion del usuario {Us._nombre} {Us._apellido}")
             eleccion=str (input("Escribe 1 para aceptar, 2 para cancelar: "))
             if eleccion=="1":
                Op.quitarSancion(Us)
             elif eleccion=="2":
                print("cancelando proceso ")
             else:
                print("Opcion invalida cancelando proceso")
            else: 
                print("La cedula que se introdujo no esta registrada")
        elif h==6:
            nuevo=registrarRecurso()
            sistemaInventario_dict.añadirRecurso(nuevo)
            sistema.atenderEspera(nuevo._nombre, usuarios)
        elif h == 7:
            Op.eliminarUsuario(usuarios)
        else:
            print("Opción no válida.")

def menuUsuario(Us, sistema, inventario, usuarios): #es el menu de los usuarios a dia de hoy esta en proceso
    while True:
        print(f"\n--- MENÚ Usuario de: {Us._nombre} ---")
        print("0. Salir del menú del Usuario")
        print("1. Ver recursos disponibles ")
        print("2. Realizar un prestamo")
        print("3. Revisar datos propios")
        print("4. Devolver un objeto")
        h = pedirNumero("Opción: ")

        if h==0:
            print("Volviendo al menu principal")
            return

        elif h==1:
            for nombre, objeto in inventario._inventarioDisponible.items():
                print(f"Nombre: {nombre}")
                print(f"  Cantidad: {objeto._cantidad}")
        
        elif h==2:
            Recurso=input("Ingrese el recurso que desea reservar ")

            sistema.prestar(Us, Recurso)
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
                sistema.devolver(Us, numero, usuarios)
            

            


usuarios = { #diccionario de objetos de clase usuario
    1398765820: usuario("Ana", "Pérez", 1001, "ana", "ana123"),
    1002256804: usuario("Luis", "Gómez", 1002, "luis", "luis123", sanciones=True, objetosReservados=["Balón", "Raqueta"]),
    1003456789: usuario("Marta", "Rojas", 1003, "marta", "marta123", objetosReservados=["Ajedrez"]),
}

operadores = { #diccionario de objetos de clase operador
<<<<<<< Updated upstream
    1098736417: Operador("Admin", "Sistema", 1, "admin", "1234"),
    2239467890: Operador("Carlos", "Díaz", 2, "carlos", "op2024"),
}
=======
1098736417: Operador("Admin", "Sistema", 1098736417, "admin", "1234"),
2239467890: Operador("Carlos", "Díaz", 2239467890, "carlos", "op2024"),
1023456789: Operador("Ana", "Gómez", 1023456789, "ana.gomez", "pass123"),
1034567890: Operador("Luis", "Rodríguez", 1034567890, "luis.rodriguez", "clave2025"),
1045678901: Operador("Sofía", "Martínez", 1045678901, "sofia.martinez", "abc987"),
1056789012: Operador("Mateo", "López", 1056789012, "mateo.lopez", "oplat24"),
1067890123: Operador("Valentina", "Pérez", 1067890123, "valen.perez", "segura1"),
1078901234: Operador("Alejandro", "García", 1078901234, "alejandro.g", "garcia20"),
1089012345: Operador("Lucía", "Fernández", 1089012345, "lucia.f", "lucia123"),
1090123456: Operador("David", "Torres", 1090123456, "david.torres", "torres99"),
1101234567: Operador("Camila", "Ramírez", 1101234567, "camila.r", "cami2026"),
1112345678: Operador("Andrés", "Castro", 1112345678, "andres.c", "castro01"),
1123456789: Operador("Mariana", "Morales", 1123456789, "mariana.m", "marii456"),
1134567890: Operador("Santiago", "Ortiz", 1134567890, "santiago.o", "santi88"),
1145678901: Operador("Valeria", "Gutiérrez", 1145678901, "valeria.g", "valguti"),
1156789012: Operador("Daniel", "Jiménez", 1156789012, "daniel.j", "dj2024"),
1167890123: Operador("Isabella", "Ruiz", 1167890123, "isabella.r", "ruiz123"),
1178901234: Operador("Sebastián", "Hernández", 1178901234, "sebastian.h", "sebxh"),
1189012345: Operador("Gabriela", "Jiménez", 1189012345, "gabriela.j", "gabi99"),
1190123456: Operador("Nicolás", "Álvarez", 1190123456, "nicolas.a", "nicoalvarez"),
1201234567: Operador("Sara", "Romero", 1201234567, "sara.romero", "sromero"),
1212345678: Operador("Lucas", "Moreno", 1212345678, "lucas.moreno", "lucasmo"),
1223456789: Operador("Martina", "Muñoz", 1223456789, "martina.m", "mmunoz"),
1234567890: Operador("Joaquín", "Rojas", 1234567890, "joaquin.r", "jrojas25"),
1245678901: Operador("Elena", "Acosta", 1245678901, "elena.acosta", "elena123"),
1256789012: Operador("Emiliano", "Medina", 1256789012, "emiliano.m", "emedina"),
1267890123: Operador("Renata", "Silva", 1267890123, "renata.silva", "rsilva"),
1278901234: Operador("Matías", "Iglesias", 1278901234, "matias.i", "miglesias"),
1289012345: Operador("Victoria", "Soto", 1289012345, "victoria.s", "vsoto"),
1290123456: Operador("Bruno", "Contreras", 1290123456, "bruno.c", "bcontreras"),
1301234567: Operador("Catalina", "Navarro", 1301234567, "catalina.n", "cnavarro"),
1312345678: Operador("Felipe", "Mendoza", 1312345678, "felipe.m", "fmendoza"),
1323456789: Operador("Antonia", "Ríos", 1323456789, "antonia.r", "arios"),
1334567890: Operador("Tomás", "Castillo", 1334567890, "tomas.c", "tcastillo"),
1345678901: Operador("Agustina", "Ponce", 1345678901, "agustina.p", "aponce"),
1356789012: Operador("Benjamín", "Vargas", 1356789012, "benjamin.v", "bvargas"),
1367890123: Operador("Florencia", "Blanco", 1367890123, "florencia.b", "fblanco"),
1378901234: Operador("Vicente", "Paz", 1378901234, "vicente.p", "vpaz"),
1389012345: Operador("Julieta", "Flores", 1389012345, "julieta.f", "jflores"),
1390123456: Operador("Maximiliano", "Guerrero", 1390123456, "maxi.g", "mguerrero"),
1401234567: Operador("Emilia", "Herrera", 1401234567, "emilia.h", "eherrera"),
1412345678: Operador("Dante", "Medina", 1412345678, "dante.m", "dmedina"),
1423456789: Operador("Regina", "Peña", 1423456789, "regina.p", "rpena"),
1434567890: Operador("Thiago", "Cabrera", 1434567890, "thiago.c", "tcabrera"),
1445678901: Operador("Bianca", "Campos", 1445678901, "bianca.c", "bcampos"),
1456789012: Operador("Gaspar", "Vega", 1456789012, "gaspar.v", "gvega"),
1467890123: Operador("Clara", "Fuentes", 1467890123, "clara.f", "cfuentes"),
1478901234: Operador("Alonso", "Cervantes", 1478901234, "alonso.c", "acervantes"),
1489012345: Operador("Amparo", "Peralta", 1489012345, "amparo.p", "aperalta"),
1490123456: Operador("Gonzalo", "Molina", 1490123456, "gonzalo.m", "gmolina"),
1093887119: Operador("Asier", "Arguinzones", 1093887119, "Grimm", "978asier")
}


sistemaInventario_dict = Inventario ({
# Libros (10)
"Matemáticas Discretas": libro("Matemáticas Discretas", 5, "Kenneth Rosen", "2019"),
"Cálculo Integral": libro("Cálculo Integral", 4, "James Stewart", "2020"),
"Estructuras de Datos": libro("Estructuras de Datos", 3, "Mark Allen Weiss", "2013"),
"Física Mecánica": libro("Física Mecánica", 6, "Serway Jewett", "2018"),
"Inteligencia Artificial": libro("Inteligencia Artificial", 2, "Stuart Russell", "2021"),
"Algoritmos en Python": libro("Algoritmos en Python", 5, "Luciano Ramalho", "2022"),
"Bases de Datos": libro("Bases de Datos", 4, "Abraham Silberschatz", "2019"),
"Redes de Computadoras": libro("Redes de Computadoras", 3, "Andrew Tanenbaum", "2021"),
"Álgebra Lineal": libro("Álgebra Lineal", 7, "Stanley Grossman", "2015"),
"Ingeniería de Software": libro("Ingeniería de Software", 3, "Ian Sommerville", "2015"),
# Equipos de Computación (8)
"Computador Portátil Dell": equipoComputacion("Computador Portátil Dell", 4, "Latitude 5420"),
"Computador Portátil HP": equipoComputacion("Computador Portátil HP", 3, "ProBook 450"),
"MacBook Pro": equipoComputacion("MacBook Pro", 2, "M2 Pro 2023"),
"Tablet Lenovo": equipoComputacion("Tablet Lenovo", 5, "Tab P11"),
"Monitor LG 27": equipoComputacion("Monitor LG 27", 4, "UltraGear 27GN850"),
"Video Beam Epson": equipoComputacion("Video Beam Epson", 2, "PowerLite X49"),
"Impresora Laser": equipoComputacion("Impresora Laser", 2, "Brother HL-L2350DW"),
"iPad Air": equipoComputacion("iPad Air", 1, "5ta Generación"),
# Otros recursos / Varios (7)
"Calculadora Científica": recurso("Calculadora Científica", 10),
"Multímetro Digital": recurso("Multímetro Digital", 6),
"Arduino Uno Kit": recurso("Arduino Uno Kit", 5),
"Raspberry Pi 4": recurso("Raspberry Pi 4", 4),
"Kit de Herramientas de Red": recurso("Kit de Herramientas de Red", 3),
"Protoboard y Cables": recurso("Protoboard y Cables", 15),
"Mouse": recurso("Mouse", 5)
})

sistema= SistemaPrestamos(sistemaInventario_dict)
>>>>>>> Stashed changes

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
            menuUsuario(Us, sistema, sistemaInventario_dict, usuarios)

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
            menuOperador(Op, usuarios, operadores, sistema)
    else:
        print("="*50 )
        print("Opción no válida.") #evita que se escriban cosas como 5 que no tengan opcion
        print ("="*50)
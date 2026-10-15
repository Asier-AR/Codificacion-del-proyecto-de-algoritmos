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

from Clases import usuario, libro, equipoComputacion, recurso

usuarios = {
1000001001: usuario("Ana", "Pérez", 1000001001, "ana_p", "ana123"),
1000001002: usuario("Luis", "Gómez", 1000001002, "luis_g", "luis123", sanciones=True, objetosReservados=["Mouse"]),
1000001003: usuario("Marta", "Rojas", 1000001003, "marta_r", "marta123"),
1000001004: usuario("Carlos", "Ruiz", 1000001004, "carlos_r", "carlos123"),
1000001005: usuario("Sofía", "Torres", 1000001005, "sofia_t", "sofia123"),
1000001006: usuario("David", "Morales", 1000001006, "david_m", "david123", sanciones=True),
1000001007: usuario("Lucía", "Jiménez", 1000001007, "lucia_j", "lucia123"),
1000001008: usuario("Mateo", "Ortiz", 1000001008, "mateo_o", "mateo123"),
1000001009: usuario("Valentina", "Castro", 1000001009, "valen_c", "valen123"),
1000001010: usuario("Alejandro", "Vargas", 1000001010, "alejo_v", "alejo123"),
1000001011: usuario("Camila", "Silva", 1000001011, "camila_s", "camila123"),
1000001012: usuario("Daniel", "Rojas", 1000001012, "daniel_r", "daniel123"),
1000001013: usuario("Valeria", "Mendoza", 1000001013, "valeria_m", "valeria123"),
1000001014: usuario("Andrés", "Parra", 1000001014, "andres_p", "andres123"),
1000001015: usuario("Mariana", "López", 1000001015, "mariana_l", "mariana123"),
1000001016: usuario("Felipe", "Ramírez", 1000001016, "felipe_r", "felipe123"),
1000001017: usuario("Gabriela", "Herrera", 1000001017, "gaby_h", "gaby123"),
1000001018: usuario("Juan", "González", 1000001018, "juan_g", "juan123"),
1000001019: usuario("Paula", "Martínez", 1000001019, "paula_m", "paula123"),
1000001020: usuario("Santiago", "Rodríguez", 1000001020, "santi_r", "santi123"),
1000001021: usuario("Isabella", "Fernández", 1000001021, "isa_f", "isa123"),
1000001022: usuario("Nicolás", "Gómez", 1000001022, "nico_g", "nico123"),
1000001023: usuario("Elena", "Blanco", 1000001023, "elena_b", "elena123"),
1000001024: usuario("Tomás", "Navarro", 1000001024, "tomas_n", "tomas123"),
1000001025: usuario("Sara", "Castillo", 1000001025, "sara_c", "sara123")
}

operadores = { #diccionario de objetos de clase operador
1098736417: Operador("Admin", "Sistema", 1098736417, "admin", "1234"),
2239467890: Operador("Carlos", "Díaz", 2239467890, "carlos", "op2024"),
1023456789: Operador("Ana", "Gómez", 2, "ana.gomez", "pass123"),
1034567890: Operador("Luis", "Rodríguez", 2, "luis.rodriguez", "clave2025"),
1045678901: Operador("Sofía", "Martínez", 3, "sofia.martinez", "abc987"),
1056789012: Operador("Mateo", "López", 2, "mateo.lopez", "oplat24"),
1067890123: Operador("Valentina", "Pérez", 3, "valen.perez", "segura1"),
1078901234: Operador("Alejandro", "García", 2, "alejandro.g", "garcia20"),
1089012345: Operador("Lucía", "Fernández", 3, "lucia.f", "lucia123"),
1090123456: Operador("David", "Torres", 2, "david.torres", "torres99"),
1101234567: Operador("Camila", "Ramírez", 3, "camila.r", "cami2026"),
1112345678: Operador("Andrés", "Castro", 2, "andres.c", "castro01"),
1123456789: Operador("Mariana", "Morales", 3, "mariana.m", "marii456"),
1134567890: Operador("Santiago", "Ortiz", 2, "santiago.o", "santi88"),
1145678901: Operador("Valeria", "Gutiérrez", 3, "valeria.g", "valguti"),
1156789012: Operador("Daniel", "Jiménez", 2, "daniel.j", "dj2024"),
1167890123: Operador("Isabella", "Ruiz", 3, "isabella.r", "ruiz123"),
1178901234: Operador("Sebastián", "Hernández", 2, "sebastian.h", "sebxh"),
1189012345: Operador("Gabriela", "Jiménez", 3, "gabriela.j", "gabi99"),
1190123456: Operador("Nicolás", "Álvarez", 2, "nicolas.a", "nicoalvarez"),
1201234567: Operador("Sara", "Romero", 3, "sara.romero", "sromero"),
1212345678: Operador("Lucas", "Moreno", 2, "lucas.moreno", "lucasmo"),
1223456789: Operador("Martina", "Muñoz", 3, "martina.m", "mmunoz"),
1234567890: Operador("Joaquín", "Rojas", 2, "joaquin.r", "jrojas25"),
1245678901: Operador("Elena", "Acosta", 3, "elena.acosta", "elena123"),
1256789012: Operador("Emiliano", "Medina", 2, "emiliano.m", "emedina"),
1267890123: Operador("Renata", "Silva", 3, "renata.silva", "rsilva"),
1278901234: Operador("Matías", "Iglesias", 2, "matias.i", "miglesias"),
1289012345: Operador("Victoria", "Soto", 3, "victoria.s", "vsoto"),
1290123456: Operador("Bruno", "Contreras", 2, "bruno.c", "bcontreras"),
1301234567: Operador("Catalina", "Navarro", 3, "catalina.n", "cnavarro"),
1312345678: Operador("Felipe", "Mendoza", 2, "felipe.m", "fmendoza"),
1323456789: Operador("Antonia", "Ríos", 3, "antonia.r", "arios"),
1334567890: Operador("Tomás", "Castillo", 2, "tomas.c", "tcastillo"),
1345678901: Operador("Agustina", "Ponce", 3, "agustina.p", "aponce"),
1356789012: Operador("Benjamín", "Vargas", 2, "benjamin.v", "bvargas"),
1367890123: Operador("Florencia", "Blanco", 3, "florencia.b", "fblanco"),
1378901234: Operador("Vicente", "Paz", 2, "vicente.p", "vpaz"),
1389012345: Operador("Julieta", "Flores", 3, "julieta.f", "jflores"),
1390123456: Operador("Maximiliano", "Guerrero", 2, "maxi.g", "mguerrero"),
1401234567: Operador("Emilia", "Herrera", 3, "emilia.h", "eherrera"),
1412345678: Operador("Dante", "Medina", 2, "dante.m", "dmedina"),
1423456789: Operador("Regina", "Peña", 3, "regina.p", "rpena"),
1434567890: Operador("Thiago", "Cabrera", 2, "thiago.c", "tcabrera"),
1445678901: Operador("Bianca", "Campos", 3, "bianca.c", "bcampos"),
1456789012: Operador("Gaspar", "Vega", 2, "gaspar.v", "gvega"),
1467890123: Operador("Clara", "Fuentes", 3, "clara.f", "cfuentes"),
1478901234: Operador("Alonso", "Cervantes", 2, "alonso.c", "acervantes"),
1489012345: Operador("Amparo", "Peralta", 3, "amparo.p", "aperalta"),
1490123456: Operador("Gonzalo", "Molina", 2, "gonzalo.m", "gmolina")
}


sistemaInventario_dict = {
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
"iPad Air": equipoComputacion("iPad Air", 3, "5ta Generación"),
# Otros recursos / Varios (7)
"Calculadora Científica": recurso("Calculadora Científica", 10),
"Multímetro Digital": recurso("Multímetro Digital", 6),
"Arduino Uno Kit": recurso("Arduino Uno Kit", 5),
"Raspberry Pi 4": recurso("Raspberry Pi 4", 4),
"Kit de Herramientas de Red": recurso("Kit de Herramientas de Red", 3),
"Protoboard y Cables": recurso("Protoboard y Cables", 15),
"Mouse": recurso("Mouse", 5)
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
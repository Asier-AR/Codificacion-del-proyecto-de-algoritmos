from Clases import usuario, libro, equipoComputacion, recurso

# 1. DICCIONARIO DE 25 USUARIOS (Cédulas de 10 dígitos)
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

# 2. DICCIONARIO DE 25 RECURSOS (INVENTARIO)
sistemaInventarioDict = {
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
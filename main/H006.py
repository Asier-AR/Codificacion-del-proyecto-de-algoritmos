# Pruebas de escenarios para la Historia de Usuario H006
# Listado de recursos ordenados por criterios y sedes

from io import StringIO
from unittest.mock import patch

from Clases import usuario, Operador, recurso, libro, equipoComputacion, Inventario
from SistemaSedes import Sede, SistemaSede
from Prestamos import SistemaPrestamos
from deshacer import HistorialOperaciones
from ordenamientos import ordenarRecursos, mostrarRecursos


def crearEntornoPrueba():
    """Construye un entorno aislado con sedes, inventarios, usuarios y sistema de prestamos."""
    invCentro = Inventario({
        "clean code": libro("clean code", 2, "Robert Martin", "2008"),
        "macbook pro": equipoComputacion("macbook pro", 1, "M2 Pro"),
        "mouse": recurso("mouse", 3)
    })
    invNorte = Inventario({
        "algebra lineal": libro("algebra lineal", 4, "Stanley Grossman", "2015"),
        "calculo integral": libro("calculo integral", 1, "James Stewart", "2020")
    })
    invVacia = Inventario({})

    invCentro._inventarioDisponible["clean code"]._fechaIngreso = "2026-01-10"
    invCentro._inventarioDisponible["macbook pro"]._fechaIngreso = "2026-03-15"
    invCentro._inventarioDisponible["mouse"]._fechaIngreso = "2026-01-10"
    invNorte._inventarioDisponible["algebra lineal"]._fechaIngreso = "2026-02-01"
    invNorte._inventarioDisponible["calculo integral"]._fechaIngreso = "2026-02-01"

    sedeCentro = Sede("Sede centro", invCentro)
    sedeNorte = Sede("Sede Norte", invNorte)
    sedeVacia = Sede("Sede Vacia", invVacia)

    sedes = {
        "Sede centro": sedeCentro,
        "Sede Norte": sedeNorte,
        "Sede Vacia": sedeVacia
    }
    conexiones = {
        "Sede centro": {"Sede Norte": 5, "Sede Vacia": 8},
        "Sede Norte": {"Sede centro": 5},
        "Sede Vacia": {"Sede centro": 8}
    }

    redSedes = SistemaSede(sedes, conexiones)
    sistema = SistemaPrestamos(redSedes)

    u1 = usuario("Ana", "Perez", 1000001001, "ana_p", "ana123")
    u2 = usuario("Luis", "Gomez", 1000001002, "luis_g", "luis123", sanciones=True)
    u3 = usuario("Marta", "Rojas", 1000001003, "marta_r", "marta123")
    u4 = usuario("Carlos", "Ruiz", 1000001004, "carlos_r", "carlos123")
    registrados = {
        u1._cedula: u1,
        u2._cedula: u2,
        u3._cedula: u3,
        u4._cedula: u4
    }
    sistema._usuarios = registrados
    return sistema, registrados, u1, u2, u3, u4


def ejecutarPruebas():
    resultados = []

    def chk(nombre, fn, esperado):
        try:
            obtenido = fn()
        except Exception as ex:
            print(f"  [FALLA] {nombre}: lanzo {type(ex).__name__} ({ex})")
            return False
        ok = obtenido == esperado
        print(f"  [{'OK ' if ok else 'FALLA'}] {nombre}: obtuvo {obtenido}")
        if not ok:
            print(f"          esperaba {esperado}")
        return ok

    print("H006 · Listado de recursos ordenados por criterios y sedes")
    print("----------------------------------------------------------")

    # Escenario 1: Ordenar por criterio valido en una sede especifica o en todas las sedes
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "mouse")
        sistema.prestar(u1, "Sede centro", "mouse")
        sistema.prestar(u1, "Sede centro", "clean code")

    filasPrestamos, algPrestamos, _ = ordenarRecursos(sistema, "prestamos", "Sede centro")
    resultados.append(chk(
        "H006-E1: ordena por mas prestados usando merge sort en Sede centro",
        lambda: (algPrestamos, [f._nombre for f in filasPrestamos]),
        ("merge sort", ["mouse", "clean code", "macbook pro"])
    ))

    filasTodas, algCategoria, _ = ordenarRecursos(sistema, "categoria", None)
    resultados.append(chk(
        "H006-E1: ordena todas las sedes por categoria usando insercion",
        lambda: (algCategoria, len(filasTodas), filasTodas[0]._categoria),
        ("inserción", 5, "Equipo de computación")
    ))

    # Escenario 2: Empates en fecha de ingreso, recursos sin prestamos y estado estimado
    filasAntiguedad, algAntiguedad, _ = ordenarRecursos(sistema, "antiguedad", "Sede centro")
    resultados.append(chk(
        "H006-E2: desempata fechas iguales por nombre usando quick sort",
        lambda: (algAntiguedad, [f._nombre for f in filasAntiguedad]),
        ("quick sort", ["clean code", "mouse", "macbook pro"])
    ))

    filasEstado, algEstado, _ = ordenarRecursos(sistema, "estado", "Sede Norte")
    resultados.append(chk(
        "H006-E2: recursos sin prestamos previos conservan 0 prestamos y 'En buen estado'",
        lambda: (
            algEstado,
            [(f._nombre, f._prestamos, f._estado) for f in filasEstado]
        ),
        ("burbuja", [("algebra lineal", 0, "En buen estado"), ("calculo integral", 0, "En buen estado")])
    ))

    # Escenario 3: Criterio invalido, sede vacia y atributo faltante en inventario
    filasInvalido, algInvalido, _ = ordenarRecursos(sistema, "criterio_inexistente", "Sede centro")
    resultados.append(chk(
        "H006-E3: criterio no reconocido devuelve lista vacia de forma controlada",
        lambda: (filasInvalido, algInvalido),
        ([], "ninguno")
    ))

    filasVacia, _, _ = ordenarRecursos(sistema, "prestamos", "Sede Vacia")
    salidaVacia = StringIO()
    with patch("sys.stdout", new=salidaVacia):
        mostrarRecursos(filasVacia, "prestamos")
    resultados.append(chk(
        "H006-E3: sede sin recursos informa que no hay recursos para mostrar",
        lambda: (len(filasVacia), "No hay recursos para mostrar." in salidaVacia.getvalue()),
        (0, True)
    ))

    class InventarioInvalido:
        pass

    sistema._sistemaSede._sedes["Sede Vacia"]._Inventario = InventarioInvalido()
    lanzoAttributeError = False
    try:
        ordenarRecursos(sistema, "prestamos", "Sede Vacia")
    except AttributeError:
        lanzoAttributeError = True

    resultados.append(chk(
        "H006-E3: detecta coleccion faltante en inventario lanzando AttributeError",
        lambda: lanzoAttributeError,
        True
    ))

    print("----------------------------------------------------------")
    aprobadas = sum(1 for ok in resultados if ok)
    total = len(resultados)
    if all(resultados):
        print(f"  H006 CERRADA — {aprobadas}/{total} pruebas pasaron.")
    else:
        print(f"  H006 CON FALLAS — {aprobadas}/{total} aprobadas.")


if __name__ == "__main__":
    ejecutarPruebas()

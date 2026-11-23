# Pruebas de escenarios para la Historia de Usuario H004
# Deshacer ultima operacion con confirmacion y pila LIFO

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

    print("H004 · Deshacer ultima operacion con confirmacion y LIFO")
    print("----------------------------------------------------------")

    # Escenario 1: Usuario realiza accion reversible, elige deshacer y confirma
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    histU1 = HistorialOperaciones()
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "mouse", histU1)

    with patch("builtins.input", return_value="1"), patch("sys.stdout", new=StringIO()):
        histU1.confirmarYDeshacer()

    resultados.append(chk(
        "H004-E1: confirmar deshacer revierte el ultimo prestamo y restaura stock",
        lambda: (
            sistema._inv("Sede centro")._inventarioDisponible["mouse"]._cantidad,
            len(u1._objetosReservados),
            len(sistema._historialUsuarios.get(u1._cedula, [])),
            histU1.verUltima() is None
        ),
        (3, 0, 0, True)
    ))

    # Escenario 2: Visualiza ultima accion registrada y decide cancelar (opcion 2)
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    histU1 = HistorialOperaciones()
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "mouse", histU1)

    with patch("builtins.input", return_value="2"), patch("sys.stdout", new=StringIO()):
        histU1.confirmarYDeshacer()

    resultados.append(chk(
        "H004-E2: cancelar mantiene intacto el prestamo y conserva la operacion en la pila",
        lambda: (
            sistema._inv("Sede centro")._inventarioDisponible["mouse"]._cantidad,
            "mouse" in u1._objetosReservados,
            histU1.verUltima() is not None
        ),
        (2, True, True)
    ))

    # Escenario 3: Orden LIFO con acciones posteriores y operacion no reversible en el tope
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    histU1 = HistorialOperaciones()
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "clean code", histU1)
        sistema.prestar(u1, "Sede centro", "mouse", histU1)

    with patch("builtins.input", return_value="1"), patch("sys.stdout", new=StringIO()):
        histU1.confirmarYDeshacer()

    resultados.append(chk(
        "H004-E3: LIFO deshace solo la ultima accion y mantiene la anterior",
        lambda: ("mouse" not in u1._objetosReservados, "clean code" in u1._objetosReservados),
        (True, True)
    ))

    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    histU1 = HistorialOperaciones()
    op = Operador("Admin", "Sistema", 1098736417, "admin", "1234")
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "mouse", histU1)
        numMouse = sistema._historialUsuarios[u1._cedula][0]._numero
        sistema.devolver(u1, numMouse, registrados, histU1)
        op.sancionarUsuario(u1)

    with patch("builtins.input", return_value="1"), patch("sys.stdout", new=StringIO()):
        histU1.confirmarYDeshacer()

    resultados.append(chk(
        "H004-E3: rechaza deshacer devolucion si el estado actual lo impide (usuario sancionado)",
        lambda: (
            sistema._historialUsuarios[u1._cedula][0]._estado,
            "mouse" not in u1._objetosReservados,
            histU1.verUltima()._descripcion.startswith("Préstamo")
        ),
        ("Devuelto", True, True)
    ))

    print("----------------------------------------------------------")
    aprobadas = sum(1 for ok in resultados if ok)
    total = len(resultados)
    if all(resultados):
        print(f"  H004 CERRADA — {aprobadas}/{total} pruebas pasaron.")
    else:
        print(f"  H004 CON FALLAS — {aprobadas}/{total} aprobadas.")


if __name__ == "__main__":
    ejecutarPruebas()

# Pruebas de escenarios para la Historia de Usuario H002
# Prestamos, devoluciones y trazabilidad en historiales

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

    print("H002 · Prestamos, devoluciones y trazabilidad en historiales")
    print("----------------------------------------------------------")

    # Escenario 1: Entrega inicial y devolucion sin inconvenientes
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    histU1 = HistorialOperaciones()

    with patch("sys.stdout", new=StringIO()):
        prestadoOk = sistema.prestar(u1, "Sede centro", "clean code", histU1)

    recClean = sistema._inv("Sede centro")._inventarioDisponible["clean code"]
    resultados.append(chk(
        "H002-E1: prestamo inicial exitoso y descuenta inventario",
        lambda: (prestadoOk, recClean._cantidad, "clean code" in u1._objetosReservados),
        (True, 1, True)
    ))

    numPrestamo = sistema._historialUsuarios[u1._cedula][0]._numero
    with patch("sys.stdout", new=StringIO()):
        devueltoOk = sistema.devolver(u1, numPrestamo, registrados, histU1)

    prestamoObj = sistema._historialUsuarios[u1._cedula][0]
    resultados.append(chk(
        "H002-E1: devolucion actualiza estado, fecha, inventario e historiales",
        lambda: (
            devueltoOk,
            prestamoObj._estado,
            prestamoObj._fechaDevolucion != "",
            recClean._cantidad,
            "clean code" not in u1._objetosReservados,
            len(sistema._historialRecursos[("Sede centro", "clean code")])
        ),
        (True, "Devuelto", True, 2, True, 1)
    ))

    # Escenario 2: Datos faltantes / entrada invalida en el proceso de entrega o devolucion
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    with patch("sys.stdout", new=StringIO()):
        prestamoSinNombre = sistema.prestar(u1, "Sede centro", "")
    resultados.append(chk(
        "H002-E2: rechaza entrega cuando falta el nombre del recurso",
        lambda: prestamoSinNombre,
        False
    ))

    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "macbook pro")
    with patch("builtins.input", return_value="9"), patch("sys.stdout", new=StringIO()):
        esperaInvalida = sistema.prestar(u3, "Sede centro", "macbook pro")
    resultados.append(chk(
        "H002-E2: cancela sin alterar estado si el dato de confirmacion es invalido",
        lambda: (esperaInvalida, len(sistema._inv("Sede centro")._Nodisponible["macbook pro"]._listaEspera)),
        (False, 0)
    ))

    # Escenario 3: Devolucion inexistente y lista de espera con usuario eliminado o sancionado
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    with patch("sys.stdout", new=StringIO()):
        devolucionInexistente = sistema.devolver(u1, 999, registrados)
    resultados.append(chk(
        "H002-E3: rechaza devolver prestamo inexistente sin alterar inventario",
        lambda: (devolucionInexistente, sistema._inv("Sede centro")._inventarioDisponible["macbook pro"]._cantidad),
        (False, 1)
    ))

    u2._sancion = False
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "macbook pro")
    with patch("builtins.input", side_effect=["1", "1", "1"]), patch("sys.stdout", new=StringIO()):
        sistema.prestar(u4, "Sede centro", "macbook pro")
        sistema.prestar(u2, "Sede centro", "macbook pro")
        sistema.prestar(u3, "Sede centro", "macbook pro")

    del registrados[u4._cedula]
    u2._sancion = True
    numMac = sistema._historialUsuarios[u1._cedula][0]._numero
    with patch("sys.stdout", new=StringIO()):
        sistema.devolver(u1, numMac, registrados)

    resultados.append(chk(
        "H002-E3: al devolver depura usuario eliminado/sancionado y asigna al siguiente valido",
        lambda: (
            len(u2._buzon) > 0,
            "macbook pro" in u3._objetosReservados,
            "macbook pro" in sistema._inv("Sede centro")._Nodisponible
        ),
        (True, True, True)
    ))

    print("----------------------------------------------------------")
    aprobadas = sum(1 for ok in resultados if ok)
    total = len(resultados)
    if all(resultados):
        print(f"  H002 CERRADA — {aprobadas}/{total} pruebas pasaron.")
    else:
        print(f"  H002 CON FALLAS — {aprobadas}/{total} aprobadas.")


if __name__ == "__main__":
    ejecutarPruebas()

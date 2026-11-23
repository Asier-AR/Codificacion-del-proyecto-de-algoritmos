# Pruebas de escenarios para la Historia de Usuario H003
# Administracion FIFO de lista de espera y asignacion automatica

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

    print("H003 · Administracion FIFO de lista de espera y asignacion automatica")
    print("----------------------------------------------------------------------")

    # Escenario 1: Se devuelve o anaden existencias a un recurso sin lista de espera
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "macbook pro")
        numPrestamo = sistema._historialUsuarios[u1._cedula][0]._numero
        sistema.devolver(u1, numPrestamo, registrados)

    resultados.append(chk(
        "H003-E1: al devolver recurso sin lista de espera queda disponible con stock restaurado",
        lambda: (
            "macbook pro" in sistema._inv("Sede centro")._inventarioDisponible,
            sistema._inv("Sede centro")._inventarioDisponible["macbook pro"]._cantidad,
            len(sistema._inv("Sede centro")._inventarioDisponible["macbook pro"]._listaEspera)
        ),
        (True, 1, 0)
    ))

    # Escenario 2: Se devuelve o anaden existencias a un recurso con lista de espera
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "macbook pro")
    with patch("builtins.input", side_effect=["1", "1"]), patch("sys.stdout", new=StringIO()):
        sistema.prestar(u3, "Sede centro", "macbook pro")
        sistema.prestar(u4, "Sede centro", "macbook pro")

    numMac = sistema._historialUsuarios[u1._cedula][0]._numero
    with patch("sys.stdout", new=StringIO()):
        sistema.devolver(u1, numMac, registrados)

    resultados.append(chk(
        "H003-E2: asigna automaticamente al primer usuario en espera (FIFO) y conserva al siguiente",
        lambda: (
            "macbook pro" in u3._objetosReservados,
            "macbook pro" not in u4._objetosReservados,
            [u._cedula for u in sistema._inv("Sede centro")._Nodisponible["macbook pro"]._listaEspera]
        ),
        (True, True, [u4._cedula])
    ))

    # Escenario 3: El primer usuario de la fila esta sancionado o no existe
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    uFantasma = usuario("Fantasma", "SinRegistro", 9999999999, "fantasma", "123")
    u2._sancion = False
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "macbook pro")
    with patch("builtins.input", side_effect=["1", "1", "1"]), patch("sys.stdout", new=StringIO()):
        sistema.prestar(uFantasma, "Sede centro", "macbook pro")
        sistema.prestar(u2, "Sede centro", "macbook pro")
        sistema.prestar(u3, "Sede centro", "macbook pro")

    u2._sancion = True
    numMac = sistema._historialUsuarios[u1._cedula][0]._numero
    with patch("sys.stdout", new=StringIO()):
        sistema.devolver(u1, numMac, registrados)

    resultados.append(chk(
        "H003-E3: omite primer usuario inexistente y sancionado, notifica y asigna al siguiente valido",
        lambda: (
            len(u2._buzon) > 0,
            "macbook pro" in u3._objetosReservados,
            "macbook pro" not in uFantasma._objetosReservados
        ),
        (True, True, True)
    ))

    # Escenario 4: Se devuelve un objeto con lista de espera pero todos no existen o estan sancionados
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    uFantasma = usuario("Fantasma", "SinRegistro", 9999999999, "fantasma", "123")
    u2._sancion = False
    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "macbook pro")
    with patch("builtins.input", side_effect=["1", "1"]), patch("sys.stdout", new=StringIO()):
        sistema.prestar(uFantasma, "Sede centro", "macbook pro")
        sistema.prestar(u2, "Sede centro", "macbook pro")

    u2._sancion = True
    numMac = sistema._historialUsuarios[u1._cedula][0]._numero
    with patch("sys.stdout", new=StringIO()):
        sistema.devolver(u1, numMac, registrados)

    resultados.append(chk(
        "H003-E4: si todos en espera no existen o estan sancionados, limpia fila y deja recurso disponible",
        lambda: (
            "macbook pro" in sistema._inv("Sede centro")._inventarioDisponible,
            sistema._inv("Sede centro")._inventarioDisponible["macbook pro"]._cantidad,
            len(sistema._inv("Sede centro")._inventarioDisponible["macbook pro"]._listaEspera),
            len(u2._buzon) > 0
        ),
        (True, 1, 0, True)
    ))

    print("----------------------------------------------------------------------")
    aprobadas = sum(1 for ok in resultados if ok)
    total = len(resultados)
    if all(resultados):
        print(f"  H003 CERRADA — {aprobadas}/{total} pruebas pasaron.")
    else:
        print(f"  H003 CON FALLAS — {aprobadas}/{total} aprobadas.")


if __name__ == "__main__":
    ejecutarPruebas()
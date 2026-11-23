# Pruebas de escenarios para la Historia de Usuario H001
# Gestion de catalogo de recursos fisicos y personas autorizadas

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


def registrarRecursoValidado(sistema, sede, tipo, nombre, cantidad, autor="", anio="", modelo="", historial=None):
    """Registra o suma unidades a un recurso tras validar campos requeridos y formatos."""
    if sede not in sistema._sistemaSede._sedes:
        return False, "Sede inexistente"
    nombreLimpio = str(nombre).strip().lower()
    if not nombreLimpio:
        return False, "Nombre vacio"
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
        return False, "Cantidad invalida"

    tipoLimpio = str(tipo).strip().lower()
    inv = sistema._inv(sede)

    if nombreLimpio in inv._inventarioDisponible:
        rec = inv._inventarioDisponible[nombreLimpio]
        rec._cantidad += cantidad
        return True, rec
    if nombreLimpio in inv._Nodisponible:
        rec = inv._Nodisponible[nombreLimpio]
        rec._cantidad += cantidad
        inv._inventarioDisponible[nombreLimpio] = inv._Nodisponible.pop(nombreLimpio)
        return True, rec

    if tipoLimpio == "libro":
        if not str(autor).strip() or not str(anio).strip():
            return False, "Faltan autor o anio del libro"
        nuevo = libro(nombreLimpio, cantidad, str(autor).strip(), str(anio).strip())
    elif tipoLimpio == "equipo":
        if not str(modelo).strip():
            return False, "Falta modelo del equipo"
        nuevo = equipoComputacion(nombreLimpio, cantidad, str(modelo).strip())
    elif tipoLimpio == "recurso":
        nuevo = recurso(nombreLimpio, cantidad)
    else:
        return False, "Tipo de recurso invalido"

    nuevo._fechaIngreso = "2026-04-01"
    inv._inventarioDisponible[nombreLimpio] = nuevo
    return True, nuevo


def darDeBajaRecursoValidado(sistema, sede, nombre):
    """Da de baja un recurso si existe, no tiene lista de espera ni prestamos activos."""
    if sede not in sistema._sistemaSede._sedes:
        return False
    nombreLimpio = str(nombre).strip().lower()
    inv = sistema._inv(sede)
    rec = inv._inventarioDisponible.get(nombreLimpio) or inv._Nodisponible.get(nombreLimpio)
    if rec is None:
        return False
    if len(rec._listaEspera) > 0:
        return False
    if sistema.tienePrestamosActivos(sede, nombreLimpio):
        return False
    inv._inventarioDisponible.pop(nombreLimpio, None)
    inv._Nodisponible.pop(nombreLimpio, None)
    return True


def modificarRecursoValidado(sistema, sede, nombre, nuevaCantidad):
    """Actualiza la cantidad de un recurso si existe y no tiene usuarios en espera."""
    if sede not in sistema._sistemaSede._sedes:
        return False
    nombreLimpio = str(nombre).strip().lower()
    inv = sistema._inv(sede)
    rec = inv._inventarioDisponible.get(nombreLimpio) or inv._Nodisponible.get(nombreLimpio)
    if rec is None or len(rec._listaEspera) > 0:
        return False
    if not isinstance(nuevaCantidad, int) or isinstance(nuevaCantidad, bool) or nuevaCantidad < 0:
        return False
    rec._cantidad = nuevaCantidad
    if nuevaCantidad == 0 and nombreLimpio in inv._inventarioDisponible:
        inv._Nodisponible[nombreLimpio] = inv._inventarioDisponible.pop(nombreLimpio)
    elif nuevaCantidad > 0 and nombreLimpio in inv._Nodisponible:
        inv._inventarioDisponible[nombreLimpio] = inv._Nodisponible.pop(nombreLimpio)
    return True


def consultarYEliminarUsuario(registrados, cedulaInput, eliminar=False):
    """Valida cedula numerica y consulta o elimina al usuario si no tiene objetos reservados."""
    textoCedula = str(cedulaInput).strip()
    if not textoCedula.isdigit():
        return (False, "Cedula no numerica") if eliminar else (None, "Cedula no numerica")
    cedulaNum = int(textoCedula)
    persona = registrados.get(cedulaNum)
    if persona is None:
        return (False, "No encontrado") if eliminar else (None, "No encontrado")
    if not eliminar:
        return persona, "OK"
    if len(getattr(persona, "_objetosReservados", [])) > 0:
        return False, "Tiene objetos reservados o prestados"
    del registrados[cedulaNum]
    return True, "Eliminado"


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

    print("H001 · Gestion de catalogo de recursos y personas autorizadas")
    print("---------------------------------------------------------------")

    # Escenario 1: Datos validos al instante y guardado correcto
    sistema, registrados, u1, u2, u3, u4 = crearEntornoPrueba()
    okReg, _ = registrarRecursoValidado(
        sistema, "Sede centro", "libro", "Patrones de Diseno", 3, autor="Erich Gamma", anio="1994"
    )
    resultados.append(chk(
        "H001-E1: registra recurso valido y queda disponible en la sede",
        lambda: (okReg, "patrones de diseno" in sistema._inv("Sede centro")._inventarioDisponible),
        (True, True)
    ))

    # Escenario 2: Omision de campos o formato invalido, ajuste y guardado posterior
    okInvalido, _ = registrarRecursoValidado(
        sistema, "Sede centro", "libro", "Clean Code", -2, autor="Robert Martin", anio="2008"
    )
    okAjustado, _ = registrarRecursoValidado(
        sistema, "Sede centro", "libro", "Clean Code", 2, autor="Robert Martin", anio="2008"
    )
    resultados.append(chk(
        "H001-E2: rechaza cantidad invalida y completa el registro tras corregir",
        lambda: (okInvalido, okAjustado, sistema._inv("Sede centro")._inventarioDisponible["clean code"]._cantidad),
        (False, True, 4)
    ))

    # Escenario 3: Recurso inexistente, en espera, usuario con prestamos o cedula no numerica
    bajaInexistente = darDeBajaRecursoValidado(sistema, "Sede centro", "recurso fantasma")
    sistema._inv("Sede centro")._inventarioDisponible["mouse"]._listaEspera.append(u3)
    modConEspera = modificarRecursoValidado(sistema, "Sede centro", "mouse", 10)
    bajaConEspera = darDeBajaRecursoValidado(sistema, "Sede centro", "mouse")

    with patch("sys.stdout", new=StringIO()):
        sistema.prestar(u1, "Sede centro", "mouse")
    elimConPrestamo = consultarYEliminarUsuario(registrados, str(u1._cedula), eliminar=True)
    consNoNum = consultarYEliminarUsuario(registrados, "1000ABC", eliminar=False)
    elimNoNum = consultarYEliminarUsuario(registrados, "1000ABC", eliminar=True)

    resultados.append(chk(
        "H001-E3: bloquea operaciones invalidas sobre recursos, usuarios con prestamos y cedulas no numericas",
        lambda: (
            bajaInexistente,
            modConEspera,
            bajaConEspera,
            elimConPrestamo[0],
            consNoNum[0] is None,
            elimNoNum[0]
        ),
        (False, False, False, False, True, False)
    ))

    print("---------------------------------------------------------------")
    aprobadas = sum(1 for ok in resultados if ok)
    total = len(resultados)
    if all(resultados):
        print(f"  H001 CERRADA — {aprobadas}/{total} pruebas pasaron.")
    else:
        print(f"  H001 CON FALLAS — {aprobadas}/{total} aprobadas.")


if __name__ == "__main__":
    ejecutarPruebas()
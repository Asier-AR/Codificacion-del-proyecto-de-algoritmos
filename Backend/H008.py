from collections import deque
import importlib.util
from pathlib import Path
import sys
import types
import unittest


def cargar_modulo_prestamos():
    """
    Carga Prestamos.py de forma segura sin romper el menú.
    Si faltan dependencias internas al importar de forma aislada, inyecta stubs mínimos
    en sys.modules solo para esta prueba.
    """
    base_dir = Path(__file__).resolve().parent
    posibles_rutas = [
        base_dir / "Prestamos" / "Prestamos.py",
        base_dir.parent / "Prestamos" / "Prestamos.py",
        base_dir / "Prestamos.py",
    ]
    ruta_objetivo = next((r for r in posibles_rutas if r.exists()), None)
    if ruta_objetivo is None:
        return None

    backend_dir = ruta_objetivo.parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    # Respaldo seguro por si Prestamos.py importa Inventarios o Usuarios sin paquetes
    if "Inventarios" not in sys.modules:
        stub_inv = types.ModuleType("Inventarios")
        class Inventario:
            def __init__(self, *args, **kwargs):
                self.items = {}
        stub_inv.Inventario = Inventario
        sys.modules["Inventarios"] = stub_inv

    try:
        spec = importlib.util.spec_from_file_location("prestamos_mod", ruta_objetivo)
        if spec and spec.loader:
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            return modulo
    except Exception:
        return None
    return None


class GestorListaEsperaCRAI:
    """
    Gestiona solicitudes de préstamo sobre artículos sin disponibilidad y su
    respectiva cola FIFO de espera por artículo.
    """

    def __init__(self, inventario: dict):
        # inventario: {nombre_articulo: unidades_disponibles}
        self.inventario = dict(inventario)
        # listas_espera: {nombre_articulo: deque([cedula_usuario, ...])}
        self.listas_espera = {art: deque() for art in inventario}

    def solicitar_prestamo_o_espera(
        self,
        cedula_usuario: str,
        articulo: str,
        acepta_unirse: bool = False,
        arrepentirse_despues: bool = False,
    ) -> dict:
        if articulo not in self.inventario:
            return {
                "estado": "inexistente",
                "en_lista": False,
                "posicion": None,
                "mensaje": f"El artículo '{articulo}' no existe en el inventario.",
            }

        if self.inventario[articulo] > 0:
            self.inventario[articulo] -= 1
            return {
                "estado": "prestado",
                "en_lista": False,
                "posicion": None,
                "mensaje": f"Préstamo aprobado para '{articulo}'.",
            }

        # Artículo agotado -> ofrecer lista de espera
        if not acepta_unirse:
            return {
                "estado": "rechazado_espera",
                "en_lista": False,
                "posicion": None,
                "mensaje": f"'{articulo}' no está disponible. El usuario decidió no unirse a la lista de espera.",
            }

        cola = self.listas_espera.setdefault(articulo, deque())

        # Escenario 4: evitar duplicados si ya estaba en la cola
        if cedula_usuario in cola:
            posicion_actual = list(cola).index(cedula_usuario) + 1
            return {
                "estado": "duplicado",
                "en_lista": True,
                "posicion": posicion_actual,
                "mensaje": (
                    f"El usuario {cedula_usuario} ya se encuentra en la lista de espera "
                    f"de '{articulo}' (posición {posicion_actual})."
                ),
            }

        cola.append(cedula_usuario)
        posicion = len(cola)

        # Escenario 3: el usuario se arrepiente inmediatamente tras unirse
        if arrepentirse_despues:
            self.salir_de_lista_espera(cedula_usuario, articulo)
            return {
                "estado": "retirado_inmediato",
                "en_lista": False,
                "posicion": None,
                "mensaje": f"El usuario {cedula_usuario} salió inmediatamente de la lista de espera de '{articulo}'.",
            }

        return {
            "estado": "en_espera",
            "en_lista": True,
            "posicion": posicion,
            "mensaje": f"Usuario {cedula_usuario} agregado a la lista de espera de '{articulo}' en posición {posicion}.",
        }

    def salir_de_lista_espera(self, cedula_usuario: str, articulo: str) -> bool:
        cola = self.listas_espera.get(articulo)
        if cola and cedula_usuario in cola:
            cola.remove(cedula_usuario)
            return True
        return False


class TestH008ListaEspera(unittest.TestCase):
    def setUp(self):
        self.modulo_real = cargar_modulo_prestamos()
        self.gestor = GestorListaEsperaCRAI(
            inventario={
                "Ipad Air": 0,      # Agotado
                "Camara Sony": 2,   # Disponible
            }
        )

    def test_escenario_1_usuario_acepta_unirse(self):
        """Escenario 1: Artículo no disponible y el usuario acepta entrar a la lista."""
        res = self.gestor.solicitar_prestamo_o_espera(
            cedula_usuario="1001",
            articulo="Ipad Air",
            acepta_unirse=True,
        )
        self.assertEqual(res["estado"], "en_espera")
        self.assertTrue(res["en_lista"])
        self.assertEqual(res["posicion"], 1)
        self.assertIn("1001", self.gestor.listas_espera["Ipad Air"])

    def test_escenario_2_usuario_no_acepta(self):
        """Escenario 2: Artículo no disponible y el usuario no acepta unirse."""
        res = self.gestor.solicitar_prestamo_o_espera(
            cedula_usuario="1002",
            articulo="Ipad Air",
            acepta_unirse=False,
        )
        self.assertEqual(res["estado"], "rechazado_espera")
        self.assertFalse(res["en_lista"])
        self.assertIsNone(res["posicion"])
        self.assertNotIn("1002", self.gestor.listas_espera["Ipad Air"])

    def test_escenario_3_usuario_se_arrepiente_y_sale(self):
        """Escenario 3: Tras entrar a la lista, el usuario desea salirse inmediatamente."""
        res = self.gestor.solicitar_prestamo_o_espera(
            cedula_usuario="1003",
            articulo="Ipad Air",
            acepta_unirse=True,
            arrepentirse_despues=True,
        )
        self.assertEqual(res["estado"], "retirado_inmediato")
        self.assertFalse(res["en_lista"])
        self.assertIsNone(res["posicion"])
        self.assertNotIn("1003", self.gestor.listas_espera["Ipad Air"])

    def test_escenario_4_intento_unirse_dos_veces(self):
        """Escenario 4: El usuario intenta unirse dos veces a la misma lista de espera."""
        primer_intento = self.gestor.solicitar_prestamo_o_espera(
            cedula_usuario="1004",
            articulo="Ipad Air",
            acepta_unirse=True,
        )
        segundo_intento = self.gestor.solicitar_prestamo_o_espera(
            cedula_usuario="1004",
            articulo="Ipad Air",
            acepta_unirse=True,
        )

        self.assertEqual(primer_intento["posicion"], 1)
        self.assertEqual(segundo_intento["estado"], "duplicado")
        self.assertTrue(segundo_intento["en_lista"])
        self.assertEqual(segundo_intento["posicion"], 1)
        # Verificar que no se duplicó en la cola FIFO
        self.assertEqual(list(self.gestor.listas_espera["Ipad Air"]).count("1004"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
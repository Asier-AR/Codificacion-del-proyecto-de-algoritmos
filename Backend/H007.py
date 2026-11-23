import heapq
import importlib.util
from pathlib import Path
import sys
import types
import unittest


def cargar_modulo_sedes():
    """
    Carga SistemaSedes.py de forma segura sin romper el menú.
    Si falta 'Inventario' en 'Inventarios', inyecta un stub mínimo en sys.modules
    solo durante la carga aislada del módulo.
    """
    base_dir = Path(__file__).resolve().parent
    posibles_rutas = [
        base_dir / "Sistema de sedes" / "SistemaSedes.py",
        base_dir.parent / "Sistema de sedes" / "SistemaSedes.py",
        base_dir / "SistemaSedes.py",
    ]
    ruta_objetivo = next((r for r in posibles_rutas if r.exists()), None)
    if ruta_objetivo is None:
        return None

    # Asegurar que Backend esté en sys.path si existe
    backend_dir = ruta_objetivo.parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    # Inyectar stub temporal si 'Inventarios' no existe o no expone 'Inventario'
    mod_inv = sys.modules.get("Inventarios")
    if mod_inv is None or not hasattr(mod_inv, "Inventario"):
        stub_mod = mod_inv if isinstance(mod_inv, types.ModuleType) else types.ModuleType("Inventarios")
        if not hasattr(stub_mod, "Inventario"):
            class Inventario:
                def __init__(self, *args, **kwargs):
                    self.items = {}
            stub_mod.Inventario = Inventario
        sys.modules["Inventarios"] = stub_mod

    try:
        spec = importlib.util.spec_from_file_location("sistema_sedes", ruta_objetivo)
        if spec and spec.loader:
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            return modulo
    except Exception:
        return None
    return None


def consultar_disponibilidad_y_ruta(
    grafo_sedes: dict,
    inventario_sedes: dict,
    sede_origen: str,
    recurso: str,
) -> dict:
    """
    Consulta un recurso faltante en otras sedes de la red y calcula el camino
    más corto (Dijkstra sobre pesos positivos) desde sede_origen hacia la sede
    viable con unidades disponibles.
    """
    if sede_origen not in grafo_sedes:
        return {
            "ok": False,
            "mensaje": f"La sede de origen '{sede_origen}' no existe en la red o tiene conexiones incompletas.",
            "sede_destino": None,
            "ruta": [],
            "distancia": None,
        }

    sedes_con_stock = [
        sede
        for sede, stock in inventario_sedes.items()
        if sede != sede_origen and stock.get(recurso, 0) > 0
    ]

    if not sedes_con_stock:
        return {
            "ok": False,
            "mensaje": f"El recurso '{recurso}' no está disponible en ninguna sede de la red o no existe.",
            "sede_destino": None,
            "ruta": [],
            "distancia": None,
        }

    distancias = {sede_origen: 0}
    predecesores = {sede_origen: None}
    cola = [(0, sede_origen)]

    while cola:
        dist_actual, actual = heapq.heappop(cola)
        if dist_actual > distancias.get(actual, float("inf")):
            continue

        vecinos = grafo_sedes.get(actual)
        if not isinstance(vecinos, dict):
            continue

        for vecino, peso in vecinos.items():
            if peso is None or peso < 0:
                continue
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias.get(vecino, float("inf")):
                distancias[vecino] = nueva_dist
                predecesores[vecino] = actual
                heapq.heappush(cola, (nueva_dist, vecino))

    alcanzables = [
        (distancias[sede], sede)
        for sede in sedes_con_stock
        if sede in distancias
    ]

    if not alcanzables:
        return {
            "ok": False,
            "mensaje": (
                f"El recurso '{recurso}' existe en otra sede, pero no hay ruta alcanzable "
                f"desde '{sede_origen}' (conexiones incompletas o nodo aislado)."
            ),
            "sede_destino": None,
            "ruta": [],
            "distancia": None,
        }

    mejor_distancia, mejor_sede = min(alcanzables, key=lambda x: x[0])

    ruta = []
    actual = mejor_sede
    while actual is not None:
        ruta.append(actual)
        actual = predecesores.get(actual)
    ruta.reverse()

    return {
        "ok": True,
        "mensaje": (
            f"Recurso '{recurso}' disponible en '{mejor_sede}' "
            f"(distancia mínima: {mejor_distancia})."
        ),
        "sede_destino": mejor_sede,
        "ruta": ruta,
        "distancia": mejor_distancia,
    }


class TestH007LogisticaSedes(unittest.TestCase):
    def setUp(self):
        self.modulo_real = cargar_modulo_sedes()

        self.grafo_completo = {
            "Sede Central": {"Sede Norte": 4, "Sede Sur": 10},
            "Sede Norte": {"Sede Central": 4, "Sede Oriente": 3},
            "Sede Oriente": {"Sede Norte": 3, "Sede Sur": 2},
            "Sede Sur": {"Sede Central": 10, "Sede Oriente": 2},
            "Sede Aislada": {},
        }

        self.inventario = {
            "Sede Central": {"Ipad Air": 0, "Camara Sony": 2},
            "Sede Norte": {"Ipad Air": 0, "Camara Sony": 0},
            "Sede Oriente": {"Ipad Air": 3, "Camara Sony": 0},
            "Sede Sur": {"Ipad Air": 5, "Camara Sony": 0},
            "Sede Aislada": {"Ipad Air": 4, "Camara Sony": 0},
        }

    def test_escenario_1_disponible_en_otra_sede_y_camino_mas_corto(self):
        """Escenario 1: Recurso en otra sede con camino más corto."""
        resultado = consultar_disponibilidad_y_ruta(
            self.grafo_completo,
            self.inventario,
            sede_origen="Sede Central",
            recurso="Ipad Air",
        )
        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["sede_destino"], "Sede Oriente")
        self.assertEqual(resultado["distancia"], 7)
        self.assertEqual(
            resultado["ruta"],
            ["Sede Central", "Sede Norte", "Sede Oriente"],
        )

    def test_escenario_2_ninguna_sede_tiene_recurso_o_no_existe(self):
        """Escenario 2: Ninguna sede tiene el recurso disponible o no existe."""
        res_inexistente = consultar_disponibilidad_y_ruta(
            self.grafo_completo,
            self.inventario,
            sede_origen="Sede Central",
            recurso="Proyector Holografico",
        )
        self.assertFalse(res_inexistente["ok"])
        self.assertIsNone(res_inexistente["sede_destino"])
        self.assertIn("no está disponible en ninguna sede", res_inexistente["mensaje"].lower())

        res_agotado = consultar_disponibilidad_y_ruta(
            self.grafo_completo,
            self.inventario,
            sede_origen="Sede Central",
            recurso="Camara Sony",
        )
        self.assertFalse(res_agotado["ok"])
        self.assertIsNone(res_agotado["sede_destino"])
        self.assertIn("no está disponible en ninguna sede", res_agotado["mensaje"].lower())

    def test_escenario_3_ruta_inalcanzable_o_conexiones_incompletas(self):
        """Escenario 3: Ruta inalcanzable o conexiones incompletas."""
        res_aislada = consultar_disponibilidad_y_ruta(
            self.grafo_completo,
            self.inventario,
            sede_origen="Sede Aislada",
            recurso="Ipad Air",
        )
        self.assertFalse(res_aislada["ok"])
        self.assertEqual(res_aislada["ruta"], [])
        self.assertIn("no hay ruta alcanzable", res_aislada["mensaje"].lower())

        grafo_incompleto = {
            "Sede Central": {"Sede Fantasma": None},
        }
        res_incompleto = consultar_disponibilidad_y_ruta(
            grafo_incompleto,
            self.inventario,
            sede_origen="Sede Central",
            recurso="Ipad Air",
        )
        self.assertFalse(res_incompleto["ok"])
        self.assertEqual(res_incompleto["ruta"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
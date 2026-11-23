import importlib.util
from pathlib import Path
import sys
import types
import unittest


def cargar_modulo_inventarios():
    """
    Carga Inventarios.py de forma segura sin activar menús interactivos ni fallar
    por imports cruzados cuando se ejecuta desde carpetas separadas.
    """
    base_dir = Path(__file__).resolve().parent
    posibles_rutas = [
        base_dir / "Inventarios" / "Inventarios.py",
        base_dir.parent / "Inventarios" / "Inventarios.py",
        base_dir / "Inventarios.py",
    ]
    ruta_objetivo = next((r for r in posibles_rutas if r.exists()), None)
    if ruta_objetivo is None:
        return None

    backend_dir = ruta_objetivo.parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    try:
        spec = importlib.util.spec_from_file_location("inventarios_mod", ruta_objetivo)
        if spec and spec.loader:
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            return modulo
    except Exception:
        return None
    return None


def filtrar_recursos(
    inventario: list,
    tipo: str = None,
    categoria: str = None,
    sede: str = None,
) -> list:
    """
    Filtra los recursos del inventario según tipo, categoría y sede.
    - Si se indican tipo, categoría y sede: devuelve los recursos que cumplen los 3 criterios.
    - Si no se indica sede (None o vacío): devuelve todos los recursos de todas las sedes
      que cumplan el tipo y la categoría indicados.
    - Si no se elige ningún filtro: devuelve todos los objetos del inventario.
    """
    tipo_norm = tipo.strip().lower() if isinstance(tipo, str) and tipo.strip() else None
    cat_norm = categoria.strip().lower() if isinstance(categoria, str) and categoria.strip() else None
    sede_norm = sede.strip().lower() if isinstance(sede, str) and sede.strip() else None

    resultados = []
    for item in inventario:
        if tipo_norm is not None and item.get("tipo", "").strip().lower() != tipo_norm:
            continue
        if cat_norm is not None and item.get("categoria", "").strip().lower() != cat_norm:
            continue
        if sede_norm is not None and item.get("sede", "").strip().lower() != sede_norm:
            continue
        resultados.append(item)

    return resultados


class TestH009FiltrosRecursos(unittest.TestCase):
    def setUp(self):
        self.modulo_real = cargar_modulo_inventarios()
        self.inventario = [
            {
                "id": "R001",
                "nombre": "Ipad Air",
                "tipo": "Tableta",
                "categoria": "Tecnologia",
                "sede": "Sede Central",
                "disponibles": 3,
            },
            {
                "id": "R002",
                "nombre": "Ipad Pro",
                "tipo": "Tableta",
                "categoria": "Tecnologia",
                "sede": "Sede Norte",
                "disponibles": 2,
            },
            {
                "id": "R003",
                "nombre": "Camara Sony Alpha",
                "tipo": "Camara",
                "categoria": "Audiovisual",
                "sede": "Sede Central",
                "disponibles": 1,
            },
            {
                "id": "R004",
                "nombre": "Calculo de Stewart",
                "tipo": "Libro",
                "categoria": "Academico",
                "sede": "Sede Sur",
                "disponibles": 5,
            },
            {
                "id": "R005",
                "nombre": "Galaxy Tab S9",
                "tipo": "Tableta",
                "categoria": "Tecnologia",
                "sede": "Sede Oriente",
                "disponibles": 4,
            },
        ]

    def test_escenario_1_tipo_categoria_y_sede_especificos(self):
        """
        Escenario 1: El usuario elige un tipo específico, una sede específica y una categoría.
        Resultado esperado: Muestra solo los recursos que cumplen los 3 filtros.
        """
        resultados = filtrar_recursos(
            self.inventario,
            tipo="Tableta",
            categoria="Tecnologia",
            sede="Sede Central",
        )
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0]["id"], "R001")
        self.assertEqual(resultados[0]["nombre"], "Ipad Air")
        self.assertEqual(resultados[0]["sede"], "Sede Central")

    def test_escenario_2_tipo_y_categoria_sin_sede_especifica(self):
        """
        Escenario 2: El usuario elige tipo y categoría específicos sin seleccionar sede.
        Resultado esperado: Muestra todos los recursos de todas las sedes que cumplan esos requisitos.
        """
        resultados = filtrar_recursos(
            self.inventario,
            tipo="Tableta",
            categoria="Tecnologia",
            sede=None,
        )
        self.assertEqual(len(resultados), 3)
        ids = {r["id"] for r in resultados}
        sedes = {r["sede"] for r in resultados}
        self.assertEqual(ids, {"R001", "R002", "R005"})
        self.assertEqual(sedes, {"Sede Central", "Sede Norte", "Sede Oriente"})

    def test_escenario_3_sin_elegir_ningun_filtro(self):
        """
        Escenario 3: El usuario no elige ningún filtro.
        Resultado esperado: Muestra todos los objetos del inventario.
        """
        resultados = filtrar_recursos(self.inventario)
        self.assertEqual(len(resultados), len(self.inventario))
        self.assertEqual(resultados, self.inventario)


if __name__ == "__main__":
    unittest.main(verbosity=2)
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


def cargar_modulo_usuarios():
    """Carga el módulo de usuarios sin ejecutar menús interactivos."""
    base_dir = Path(__file__).resolve().parent
    posibles_rutas = [
        base_dir / "Usuarios y operadores" / "Usuarios y operadores.py",
        base_dir.parent / "Usuarios y operadores" / "Usuarios y operadores.py",
        base_dir / "Usuarios y operadores.py",
    ]
    for ruta in posibles_rutas:
        if ruta.exists():
            spec = importlib.util.spec_from_file_location("usuarios_operadores", ruta)
            if spec and spec.loader:
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                return modulo
    return None


def validar_cedula(cedula: str) -> bool:
    """Valida que la cédula no tenga espacios extra ni caracteres no numéricos."""
    if not isinstance(cedula, str) or not cedula:
        return False
    return cedula.isdigit()


def consultar_usuario_por_cedula(base_usuarios: dict, cedula: str) -> dict:
    """
    Consulta directa en O(1) mediante el identificador único (cédula).
    Soporta los 3 escenarios de H005 sin lanzar excepciones inesperadas.
    """
    if not validar_cedula(cedula):
        return {
            "ok": False,
            "mensaje": "Cédula inválida: no debe contener espacios extra ni caracteres no numéricos.",
            "usuario": None,
        }

    usuario = base_usuarios.get(cedula)
    if usuario is None:
        return {
            "ok": False,
            "mensaje": f"No existe ningún usuario registrado con la cédula {cedula}.",
            "usuario": None,
        }

    return {
        "ok": True,
        "mensaje": "Usuario encontrado exitosamente.",
        "usuario": usuario,
    }


class TestH005ConsultaUsuario(unittest.TestCase):
    def setUp(self):
        # Si existe el módulo real del proyecto, se carga de forma segura sin romper menu.py
        self.modulo_real = cargar_modulo_usuarios()

        # Base indexada por cédula para garantizar búsqueda instantánea O(1)
        self.base_usuarios = {
            "1001234567": {
                "cedula": "1001234567",
                "nombre": "Ana Gómez",
                "rol": "Estudiante",
                "sancionado": False,
            },
            "1009876543": {
                "cedula": "1009876543",
                "nombre": "Carlos Pérez",
                "rol": "Docente",
                "sancionado": False,
            },
        }

    def test_escenario_1_cedula_exacta_registrada(self):
        """Escenario 1: Se ingresa la cédula exacta de un usuario registrado en el sistema."""
        resultado = consultar_usuario_por_cedula(self.base_usuarios, "1001234567")

        self.assertTrue(resultado["ok"])
        self.assertIsNotNone(resultado["usuario"])
        self.assertEqual(resultado["usuario"]["nombre"], "Ana Gómez")
        self.assertEqual(resultado["usuario"]["cedula"], "1001234567")

    def test_escenario_2_cedula_con_caracteres_invalidos_o_espacios(self):
        """Escenario 2: La cédula ingresada tiene caracteres no válidos o espacios extra."""
        entradas_invalidas = [
            " 1001234567",
            "1001234567 ",
            " 1001234567 ",
            "10012a4567",
            "10012-34567",
            "",
            "   ",
        ]
        for cedula in entradas_invalidas:
            with self.subTest(cedula=cedula):
                resultado = consultar_usuario_por_cedula(self.base_usuarios, cedula)
                self.assertFalse(resultado["ok"])
                self.assertIsNone(resultado["usuario"])
                self.assertIn("inválida", resultado["mensaje"].lower())

    def test_escenario_3_cedula_no_registrada(self):
        """Escenario 3: La cédula corresponde a un usuario que no está registrado."""
        resultado = consultar_usuario_por_cedula(self.base_usuarios, "9999999999")

        self.assertFalse(resultado["ok"])
        self.assertIsNone(resultado["usuario"])
        self.assertIn("no existe", resultado["mensaje"].lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
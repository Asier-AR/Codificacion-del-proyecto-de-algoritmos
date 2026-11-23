from pathlib import Path
import importlib.util
import sys

RAIZ_CARPETA = Path(__file__).resolve().parent


def cargar_modulo(alias: str, ruta_relativa: str):
    ruta = RAIZ_CARPETA / ruta_relativa
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró '{alias}' en: {ruta}")
    spec = importlib.util.spec_from_file_location(alias, ruta)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[alias] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def cargar_modulos_base():
    cargar_modulo("UsuariosOperadores", "Usuarios y operadores/Usuarios y operadores.py")
    cargar_modulo("Inventarios", "Inventarios/Inventarios.py")
    cargar_modulo("SistemaSedes", "Sistema de sedes/SistemaSedes.py")
    cargar_modulo("deshacer", "Deshacer/deshacer.py")
    cargar_modulo("Prestamos", "Prestamos/Prestamos.py")
    cargar_modulo("Registros", "Registros/Registros.py")
    cargar_modulo("ordenamientos", "Ordenamientos/ordenamientos.py")
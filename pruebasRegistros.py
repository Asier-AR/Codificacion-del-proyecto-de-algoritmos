from Clases import usuario, libro, equipoComputacion, recurso
from Registros import usuarios, sistemaInventario_dict

print("   INICIANDO PRUEBAS DE REGISTROS")

    # 1. Verificar cantidad y validez de los usuarios
print(f"\n[PRUEBA 1] Total de usuarios cargados: {len(usuarios)}")
assert len(usuarios) == 25, "Error: Debería haber exactamente 25 usuarios."
    
print("Verificando que todas las cédulas tengan al menos 10 dígitos:")
for cedula, user in usuarios.items():
    cedula_str = str(cedula)
    print(f" - Usuario: {user._nombre} {user._apellido} | Cédula: {cedula} (Dígitos: {len(cedula_str)})")
    assert len(cedula_str) >= 10, f"Error: La cédula {cedula} tiene menos de 10 dígitos."
print("¡Prueba de usuarios superada con éxito!")

    # 2. Verificar cantidad y tipos de recursos
print(f"\n[PRUEBA 2] Total de recursos en el inventario: {len(sistemaInventario_dict)}")
assert len(sistemaInventario_dict) == 25, "Error: Debería haber exactamente 25 recursos."

print("Listando recursos y sus existencias iniciales:")
for nombre, rec in sistemaInventario_dict.items():
    print(f" - Recurso: {nombre} | Cantidad disponible: {rec._cantidad}")
print("¡Prueba de inventario superada con éxito!")

print("   ¡TODAS LAS PRUEBAS FINALIZARON EXITOSAMENTE!")
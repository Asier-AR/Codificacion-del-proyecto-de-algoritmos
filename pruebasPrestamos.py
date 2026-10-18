from Prestamos import SistemaPrestamos
from Clases import Inventario
from Registros import usuarios, sistemaInventario_dict

print("   INICIANDO PRUEBAS DEL SISTEMA DE PRÉSTAMOS")

# Inicializar el inventario y el sistema de préstamos
inventario_prueba = Inventario(sistemaInventario_dict)
sistema = SistemaPrestamos(inventario_prueba)

# --------------------------------------------------
# 1. PRUEBA DE USUARIO SANCIONADO
# --------------------------------------------------
print("\n[PRUEBA 1] Intentando realizar un préstamo a un usuario sancionado...")
# El usuario con cédula 1000001002 (Luis Gómez) tiene sanción en Registros.py
usuario_sancionado = usuarios[1000001002]
sistema.prestar(usuario_sancionado, "Matemáticas Discretas")

print("\n[PRUEBA 2] Realizando un préstamo exitoso...")
usuario_normal = usuarios[1000001001] # Ana Pérez
nombre_recurso = "Matemáticas Discretas"

# Stock inicial del recurso
stock_inicial = sistema._inventarioDisponible[nombre_recurso]._cantidad
print(f"Stock inicial de '{nombre_recurso}': {stock_inicial}")

resultado = sistema.prestar(usuario_normal, nombre_recurso)
print(f"¿Préstamo exitoso?: {resultado}")

print("\n[PRUEBA 3] Consultando préstamos activos del usuario...")
activos = sistema.prestamosActivos(usuario_normal)
print(f"Total de préstamos activos: {len(activos)}")
for p in activos:
    print(" -", p)


print("\n[PRUEBA 4] Visualizando historiales...")
sistema.verHistorialUsuario(usuario_normal)
sistema.verHistorialRecurso(nombre_recurso)

print("\n[PRUEBA 5] Registrando la devolución del recurso...")
if activos:
    numero_prestamo = activos[0]._numero
    sistema.devolver(usuario_normal, numero_prestamo, usuarios)
    
    # Verificar stock tras la devolución
    stock_final = sistema._inventarioDisponible[nombre_recurso]._cantidad
    print(f"Stock final de '{nombre_recurso}' tras devolver: {stock_final}")

print("   PRUEBAS EJECUTADAS CORRECTAMENTE")
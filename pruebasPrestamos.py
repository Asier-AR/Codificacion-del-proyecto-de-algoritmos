from Registros import usuarios, sistemaInventarioDict
from Prestamos import SistemaPrestamos

print("   INICIANDO PRUEBAS DE PRÉSTAMOS")

    # Inicializar el sistema de préstamos con el inventario importado
sistema = SistemaPrestamos(sistemaInventarioDict)

    # 1. Seleccionar usuarios de prueba
    # Usamos el usuario con cédula 1000001001 (sin sanción)
usuarioNormal = usuarios[1000001001]
    # Usamos el usuario con cédula 1000001002 (con sanción activa)
usuarioSancionado = usuarios[1000001002]

    # 2. Prueba de sanción: un usuario sancionado no puede realizar préstamos
print("\n[PRUEBA 1] Intentando prestar a un usuario sancionado...")
resultadoSancion = sistema.prestar(usuarioSancionado, "Matemáticas Discretas")
assert resultadoSancion == False, "Error: El sistema permitió un préstamo a un usuario sancionado."
print("¡Prueba de usuario sancionado superada con éxito!")

    # 3. Prueba de préstamo exitoso
print("\n[PRUEBA 2] Realizando un préstamo exitoso...")
recursoNombre = "Matemáticas Discretas"
stockInicial = sistemaInventarioDict[recursoNombre]._cantidad
    
resultado_prestamo = sistema.prestar(usuarioNormal, recursoNombre)
    
assert resultado_prestamo == True, "Error: El préstamo no pudo realizarse."
assert sistemaInventarioDict[recursoNombre]._cantidad == stockInicial - 1, "Error: El stock del recurso no disminuyó."
assert recursoNombre in usuarioNormal._objetosReservados, "Error: El recurso no se agregó a los objetos reservados del usuario."
print("¡Prueba de préstamo exitoso superada con éxito!")

    # 4. Verificar préstamos activos e historiales
print("\n[PRUEBA 3] Verificando préstamos activos e historiales...")
activos = sistema.prestamosActivos(usuarioNormal)
assert len(activos) == 1, "Error: Debería haber exactamente 1 préstamo activo."
numero_prestamo = activos[0]._numero
    
sistema.verHistorialUsuario(usuarioNormal, recientePrimero=True)
sistema.verHistorialRecurso(recursoNombre, recientePrimero=True)
print("¡Prueba de historial superada con éxito!")

    # 5. Prueba de devolución
print("\n[PRUEBA 4] Realizando la devolución del recurso...")
stockAntesDevolucion = sistemaInventarioDict[recursoNombre]._cantidad
    
resultado_devolucion = sistema.devolver(usuarioNormal, numero_prestamo)
    
assert resultado_devolucion == True, "Error: La devolución falló."
assert sistemaInventarioDict[recursoNombre]._cantidad == stockAntesDevolucion + 1, "Error: El stock no se restituyó correctamente."
assert len(sistema.prestamosActivos(usuarioNormal)) == 0, "Error: El préstamo sigue figurando como activo."
assert recursoNombre not in usuarioNormal._objetosReservados, "Error: El recurso no fue removido de los objetos reservados."
print("¡Prueba de devolución superada con éxito!")

print("   ¡TODAS LAS PRUEBAS DE PRÉSTAMOS FINALIZARON EXITOSAMENTE!")
# ordenamientos.py  -  Linea 1, requerimiento 6:
# "Listar los recursos ordenados por distintos criterios: mas prestados, mas antiguos,
#  por categoria o por estado."
#
# Los algoritmos de ordenamiento estan hechos a mano (no se usa sort ni sorted).


import time
from Clases import libro, equipoComputacion


def sinTildes(texto): #para ordenar alfabeticamente: sin esto "álgebra" quedaria despues de la "z"
    return texto.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ü", "u")


def categoriaDe(rec): #la categoria sale de la clase del recurso (herencia): libro, equipo o recurso base
    if isinstance(rec, libro):
        return "Libro"
    elif isinstance(rec, equipoComputacion):
        return "Equipo de computación"
    else:
        return "Otro"


def estadoPorUso(cantidadPrestamos):
    """Estima el estado por el uso acumulado del recurso."""
    if cantidadPrestamos >= 15:
        return "Defectuoso"
    if cantidadPrestamos >= 10:
        return "Desgastado"
    if cantidadPrestamos >= 5:
        return "Usado"
    return "En buen estado"


class FilaRecurso: #una fila del listado: los datos del recurso que se muestran y por los que se ordena
    def __init__(self, rec, cantidadPrestamos, sede):
        self._nombre = rec._nombre
        self._sede = sede
        self._nombreOrden = sinTildes(rec._nombre)  # el nombre sin tildes, que es el que se usa para desempatar
        self._categoria = categoriaDe(rec)
        self._estado = estadoPorUso(cantidadPrestamos)
        self._disponibles = rec._cantidad           # unidades que hay ahora
        self._enEspera = len(rec._listaEspera)      # personas esperando el recurso
        self._prestamos = cantidadPrestamos         # prestamos que ha tenido en total
        self._fechaIngreso = rec._fechaIngreso      # fecha en que entro al inventario

    def clave(self, criterio):
        # devuelve lo que se compara. Va con el nombre al final para desempatar.
        # Todos se ordenan de menor a mayor, por eso los mas prestados van en negativo.
        if criterio == "prestamos":
            return (-self._prestamos, self._nombreOrden)             # el que mas se ha prestado queda primero
        elif criterio == "antiguedad":
            return (self._fechaIngreso, self._nombreOrden)           # la fecha mas vieja queda primero (formato AAAA-MM-DD)
        elif criterio == "categoria":
            return (self._categoria, self._nombreOrden)              # orden alfabetico de categoria
        elif criterio == "estado":
            ordenEstados = {"Defectuoso": 0, "Desgastado": 1, "Usado": 2, "En buen estado": 3}
            orden = ordenEstados[self._estado]
            return (orden, self._nombreOrden)
        return (self._nombreOrden, "")


# ---------------------------------------------------------------
# ALGORITMOS DE ORDENAMIENTO (reciben una lista de FilaRecurso y el criterio)
# ---------------------------------------------------------------
def burbuja(lista, criterio): #basico: compara vecinos y los intercambia si estan al reves
    lista = lista[:]                                # se trabaja con una copia
    n = len(lista)
    for i in range(n - 1):
        huboCambio = False
        for j in range(n - 1 - i):
            if lista[j].clave(criterio) > lista[j + 1].clave(criterio):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                huboCambio = True
        if not huboCambio: #si en una pasada no se cambio nada, ya esta ordenada
            break
    return lista


def insercion(lista, criterio): #basico: va armando una parte ordenada y mete cada elemento en su lugar
    lista = lista[:]
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and lista[j].clave(criterio) > actual.clave(criterio):
            lista[j + 1] = lista[j] #se corre el elemento a la derecha
            j -= 1
        lista[j + 1] = actual
    return lista


def mergeSort(lista, criterio): #avanzado: parte la lista en dos, ordena cada mitad (recursion) y las mezcla
    if len(lista) <= 1: #caso base: una lista de 0 o 1 elemento ya esta ordenada
        return lista[:]
    mitad = len(lista) // 2
    izquierda = mergeSort(lista[:mitad], criterio)
    derecha = mergeSort(lista[mitad:], criterio)

    resultado = []
    i = 0
    j = 0
    while i < len(izquierda) and j < len(derecha): #se mezcla escogiendo siempre el menor de los dos
        if izquierda[i].clave(criterio) <= derecha[j].clave(criterio):
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    while i < len(izquierda): #lo que sobre de alguna de las dos mitades se pasa tal cual
        resultado.append(izquierda[i])
        i += 1
    while j < len(derecha):
        resultado.append(derecha[j])
        j += 1
    return resultado


def quickSort(lista, criterio): #avanzado: escoge un pivote y separa menores y mayores (recursion)
    if len(lista) <= 1: #caso base
        return lista[:]
    pivote = lista[len(lista) // 2]
    clavePivote = pivote.clave(criterio)
    menores = []
    iguales = []
    mayores = []
    for fila in lista:
        c = fila.clave(criterio)
        if c < clavePivote:
            menores.append(fila)
        elif c > clavePivote:
            mayores.append(fila)
        else:
            iguales.append(fila)
    return quickSort(menores, criterio) + iguales + quickSort(mayores, criterio)


# ---------------------------------------------------------------
# LISTADO DE RECURSOS
# ---------------------------------------------------------------
def _coleccionInventario(inventario, *nombres):
    """Obtiene una colección del inventario y tolera nombres antiguos."""
    for nombre in nombres:
        coleccion = getattr(inventario, nombre, None)
        if coleccion is not None:
            return coleccion
    nombresTexto = ", ".join(nombres)
    raise AttributeError(f"El inventario no tiene ninguno de estos atributos: {nombresTexto}")


def crearFilas(sistema, sedeFiltro=None): #arma una fila por cada recurso de la sede elegida
    filas = []
    for sede in sistema._sistemaSede._sedes:
        if sedeFiltro is not None and sede != sedeFiltro:
            continue
        inventario = sistema._inv(sede)
        disponibles = _coleccionInventario(inventario, "_inventarioDisponible", "inventarioDisponible")
        noDisponibles = _coleccionInventario(inventario, "_Nodisponible", "Nodisponible", "_inventarioNoDisponible")
        for nombre, rec in disponibles.items():
            prestamos = len(sistema._historialRecursos.get((sede, nombre), []))
            filas.append(FilaRecurso(rec, prestamos, sede))
        for nombre, rec in noDisponibles.items():
            prestamos = len(sistema._historialRecursos.get((sede, nombre), []))
            filas.append(FilaRecurso(rec, prestamos, sede))
    return filas


def ordenarRecursos(sistema, criterio, sedeFiltro=None, invertir=False):
    # criterio: "prestamos", "antiguedad", "categoria" o "estado"
    # devuelve la lista ordenada, el nombre del algoritmo usado y lo que se demoro (en segundos)
    filas = crearFilas(sistema, sedeFiltro)
    inicio = time.perf_counter()
    if criterio == "prestamos":
        ordenadas = mergeSort(filas, criterio)
        algoritmo = "merge sort"
    elif criterio == "antiguedad":
        ordenadas = quickSort(filas, criterio)
        algoritmo = "quick sort"
    elif criterio == "categoria":
        ordenadas = insercion(filas, criterio)
        algoritmo = "inserción"
    elif criterio == "estado":
        ordenadas = burbuja(filas, criterio)
        algoritmo = "burbuja"
    else:
        return [], "ninguno", 0
    segundos = time.perf_counter() - inicio
    if invertir:
        ordenadas = ordenadas[::-1] #lista al reves
    return ordenadas, algoritmo, segundos


def mostrarRecursos(filas, criterio, limite=0): #muestra solo los datos relevantes del orden elegido
    if len(filas) == 0:
        print("No hay recursos para mostrar.")
        return
    columnas = {
        "prestamos": ("RECURSO", "PRÉSTAMOS"),
        "antiguedad": ("RECURSO",),
        "categoria": ("RECURSO", "CATEGORÍA"),
        "estado": ("RECURSO", "ESTADO"),
    }
    nombresColumnas = ("SEDE",) + columnas[criterio]
    print("  ".join(f"{nombre:<24}" for nombre in nombresColumnas))
    print("-" * (26 * len(nombresColumnas)))
    contador = 0
    for fila in filas:
        contador += 1
        if limite > 0 and contador > limite:
            break
        datos = {
            "prestamos": (fila._sede, fila._nombre, fila._prestamos),
            "antiguedad": (fila._sede, fila._nombre),
            "categoria": (fila._sede, fila._nombre, fila._categoria),
            "estado": (fila._sede, fila._nombre, fila._estado),
        }[criterio]
        print("  ".join(f"{str(dato):<24}" for dato in datos))

    print("-" * (26 * len(nombresColumnas)))
    print(f"Total: {len(filas)} recursos")
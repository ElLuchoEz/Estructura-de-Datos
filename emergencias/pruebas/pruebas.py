"""Pruebas del proyecto. Ejecutar:  python pruebas/pruebas.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from estructuras.lista_enlazada import ListaEnlazada
from estructuras.pila import Pila
from estructuras.cola import Cola
from estructuras.arbol_bst import ArbolBST
from estructuras.grafo import Grafo
from modelos.incidente import Incidente
from servicios.gestor_emergencias import GestorEmergencias

_resultados = []


def verificar(caso, condicion, obtenido=""):
    estado = "OK   " if condicion else "FALLA"
    extra = "" if condicion or obtenido == "" else "  (obtenido: %s)" % (obtenido,)
    print("[%s] %s%s" % (estado, caso, extra))
    _resultados.append(condicion)


def seccion(titulo):
    print("\n--- %s ---" % titulo)


def pruebas_lista():
    seccion("LISTA ENLAZADA")
    lista = ListaEnlazada()
    verificar("Lista nueva está vacía", lista.esta_vacia() and lista.tamano() == 0)
    verificar("Eliminar inicio en lista vacía devuelve None", lista.eliminar_inicio() is None)
    verificar("Eliminar final en lista vacía devuelve None", lista.eliminar_final() is None)
    verificar("Buscar en lista vacía devuelve None", lista.buscar(lambda x: x == 1) is None)
    lista.insertar_final(2)
    lista.insertar_final(3)
    lista.insertar_inicio(1)
    verificar("Inserciones inicio/final -> [1,2,3]", list(lista) == [1, 2, 3], list(lista))
    verificar("Tamaño = 3", lista.tamano() == 3)
    verificar("Búsqueda exitosa", lista.buscar(lambda x: x == 2) == 2)
    verificar("Búsqueda sin resultado", lista.buscar(lambda x: x == 99) is None)
    verificar("Eliminar inicio devuelve 1", lista.eliminar_inicio() == 1)
    verificar("Eliminar final devuelve 3", lista.eliminar_final() == 3)
    verificar("Queda [2]", list(lista) == [2], list(lista))
    verificar("Eliminar el único elemento", lista.eliminar_final() == 2 and lista.esta_vacia())
    lista.insertar_final(5)
    verificar("Tras vaciar, insertar al final funciona", list(lista) == [5])
    lista.insertar_final(6)
    lista.insertar_final(7)
    verificar("Eliminar por valor del medio", lista.eliminar_donde(lambda x: x == 6) == 6
              and list(lista) == [5, 7])
    verificar("Eliminar por valor del último mantiene la cola", lista.eliminar_donde(lambda x: x == 7) == 7)
    lista.insertar_final(8)
    verificar("Insertar tras eliminar el último enlaza bien", list(lista) == [5, 8], list(lista))
    verificar("Eliminar por valor inexistente devuelve None", lista.eliminar_donde(lambda x: x == 99) is None)


def pruebas_pila():
    seccion("PILA")
    pila = Pila()
    verificar("Pila nueva vacía", pila.esta_vacia() and pila.tamano() == 0)
    verificar("Desapilar en vacía devuelve None", pila.desapilar() is None)
    verificar("Tope en vacía devuelve None", pila.ver_tope() is None)
    for x in (1, 2, 3):
        pila.apilar(x)
    verificar("Tope = 3 (último en entrar)", pila.ver_tope() == 3)
    verificar("Mostrar no altera la pila", list(pila.recorrer()) == [3, 2, 1] and pila.tamano() == 3)
    verificar("Orden LIFO 3,2,1", [pila.desapilar(), pila.desapilar(), pila.desapilar()] == [3, 2, 1])
    verificar("Pila queda vacía", pila.esta_vacia())


def pruebas_cola():
    seccion("COLA")
    cola = Cola()
    verificar("Cola nueva vacía", cola.esta_vacia() and cola.tamano() == 0)
    verificar("Desencolar en vacía devuelve None", cola.desencolar() is None)
    verificar("Frente/último en vacía devuelven None", cola.ver_frente() is None and cola.ver_ultimo() is None)
    for x in (1, 2, 3):
        cola.encolar(x)
    verificar("Frente = 1, último = 3", cola.ver_frente() == 1 and cola.ver_ultimo() == 3)
    verificar("Orden FIFO 1,2,3", [cola.desencolar(), cola.desencolar(), cola.desencolar()] == [1, 2, 3])
    verificar("Cola queda vacía", cola.esta_vacia())
    cola.encolar(9)
    verificar("Encolar tras vaciar funciona", cola.ver_frente() == 9 and cola.ver_ultimo() == 9)


def pruebas_arbol():
    seccion("ÁRBOL BST")
    arbol = ArbolBST()
    verificar("Árbol vacío: altura 0, hojas 0", arbol.altura() == 0 and arbol.cantidad_hojas() == 0)
    verificar("Buscar en árbol vacío devuelve None", arbol.buscar(5) is None)
    verificar("Eliminar en árbol vacío devuelve False", arbol.eliminar(5) is False)
    for x in (50, 30, 70, 20, 40, 60, 80):
        arbol.insertar(x, x)
    verificar("Inserción duplicada rechazada", arbol.insertar(50, 50) is False)
    verificar("Cantidad de nodos = 7", arbol.cantidad_nodos() == 7)
    verificar("Preorden", list(arbol.preorden()) == [50, 30, 20, 40, 70, 60, 80], list(arbol.preorden()))
    verificar("Inorden ordenado", list(arbol.inorden()) == [20, 30, 40, 50, 60, 70, 80], list(arbol.inorden()))
    verificar("Postorden", list(arbol.postorden()) == [20, 40, 30, 60, 80, 70, 50], list(arbol.postorden()))
    verificar("Altura = 3, hojas = 4", arbol.altura() == 3 and arbol.cantidad_hojas() == 4)
    verificar("Búsqueda exitosa", arbol.buscar(60) == 60)
    verificar("Búsqueda sin resultado", arbol.buscar(65) is None)
    verificar("Eliminar hoja (20)", arbol.eliminar(20) and list(arbol.inorden()) == [30, 40, 50, 60, 70, 80])
    verificar("Eliminar nodo con un hijo (30)", arbol.eliminar(30) and list(arbol.inorden()) == [40, 50, 60, 70, 80])
    verificar("Eliminar nodo con dos hijos (70)", arbol.eliminar(70) and list(arbol.inorden()) == [40, 50, 60, 80],
              list(arbol.inorden()))
    verificar("Eliminar la raíz (50) conserva el orden", arbol.eliminar(50) and list(arbol.inorden()) == [40, 60, 80],
              list(arbol.inorden()))
    verificar("Eliminar clave inexistente devuelve False", arbol.eliminar(1234) is False)
    verificar("Cantidad de nodos coherente = 3", arbol.cantidad_nodos() == 3)


def construir_grafo():
    g = Grafo()
    for z in ("Centro", "Norte", "Sur", "Este", "Oeste", "Puerto", "Isla"):
        g.agregar_vertice(z)
    for a, b, p in (("Centro", "Norte", 4), ("Centro", "Sur", 5), ("Centro", "Este", 3),
                    ("Centro", "Oeste", 6), ("Norte", "Este", 5), ("Sur", "Puerto", 7),
                    ("Este", "Puerto", 4)):
        g.agregar_arista(a, b, p)
    return g
#aca se explica la opcion numero 16. :)

def pruebas_grafo():
    seccion("GRAFO")
    g = construir_grafo()
    verificar("7 vértices", g.cantidad_vertices() == 7)
    verificar("Vértice duplicado rechazado", g.agregar_vertice("Centro") is False)
    verificar("Arista duplicada rechazada", g.agregar_arista("Centro", "Norte", 9) is False)
    verificar("Arista con vértice inexistente rechazada", g.agregar_arista("Centro", "Marte", 3) is False)
    verificar("Arista con peso inválido rechazada", g.agregar_arista("Norte", "Sur", 0) is False)
    verificar("Consultar conexiones de Centro",
              list(g.conexiones("Centro")) == [("Norte", 4), ("Sur", 5), ("Este", 3), ("Oeste", 6)])
    verificar("BFS desde Centro", g.bfs("Centro") == ["Centro", "Norte", "Sur", "Este", "Oeste", "Puerto"],
              g.bfs("Centro"))
    verificar("DFS desde Centro", g.dfs("Centro") == ["Centro", "Norte", "Este", "Puerto", "Sur", "Oeste"],
              g.dfs("Centro"))
    verificar("BFS desde zona inexistente devuelve []", g.bfs("Marte") == [])
    verificar("Existe conexión Centro -> Puerto", g.existe_camino("Centro", "Puerto"))
    verificar("NO existe conexión Centro -> Isla", g.existe_camino("Centro", "Isla") is False)
    verificar("Dijkstra Centro -> Puerto = 7 por Este",
              g.dijkstra("Centro", "Puerto") == (7, ["Centro", "Este", "Puerto"]), g.dijkstra("Centro", "Puerto"))
    verificar("Dijkstra Norte -> Puerto = 9", g.dijkstra("Norte", "Puerto") == (9, ["Norte", "Este", "Puerto"]),
              g.dijkstra("Norte", "Puerto"))
    verificar("Dijkstra hacia Isla devuelve None (sin camino)", g.dijkstra("Centro", "Isla") is None)
    verificar("Dijkstra origen = destino cuesta 0", g.dijkstra("Sur", "Sur") == (0, ["Sur"]))
    verificar("Eliminar conexión Este-Puerto", g.eliminar_arista("Este", "Puerto") and not g.hay_arista("Puerto", "Este"))
    verificar("Con Este-Puerto cerrada, Centro -> Puerto = 12 por Sur",
              g.dijkstra("Centro", "Puerto") == (12, ["Centro", "Sur", "Puerto"]), g.dijkstra("Centro", "Puerto"))
    verificar("Eliminar conexión inexistente devuelve False", g.eliminar_arista("Centro", "Isla") is False)


def pruebas_integracion():
    seccion("INTEGRACIÓN (gestor con las 5 estructuras)")
    g = GestorEmergencias()
    verificar("Atender sin pendientes informa error", g.atender_siguiente()[0] is False)
    verificar("Deshacer con pila vacía informa error", g.deshacer()[0] is False)
    verificar("Registrar incidente con zona inexistente falla", g.registrar_incidente("incendio", "Norte", 1)[0] is False)
    g.cargar_datos_prueba()
    verificar("Centro duplicado rechazado", g.registrar_centro("B01", "Otro", "bomberos", "Sur")[0] is False)
    verificar("Centro con zona inexistente rechazado", g.registrar_centro("X01", "X", "bomberos", "Marte")[0] is False)
    verificar("Centro con tipo inválido rechazado", g.registrar_centro("X01", "X", "ovnis", "Sur")[0] is False)
    verificar("Árbol de centros: 5 nodos, altura 3, 2 hojas inorden ordenado",
              g.centros.cantidad_nodos() == 5 and g.centros.altura() == 3 and g.centros.cantidad_hojas() == 2
              and [c.codigo for c in g.centros.inorden()] == ["B01", "B02", "H01", "H02", "P01"])
    verificar("Tipo de incidente inválido rechazado", g.registrar_incidente("terremoto", "Norte", 1)[0] is False)
    verificar("Prioridad inválida rechazada", g.registrar_incidente("incendio", "Norte", 7)[0] is False)

    verificar("Registrar incendio en Norte (#1)", g.registrar_incidente("incendio", "Norte", 1)[0])
    verificar("Registrar médico en Puerto (#2)", g.registrar_incidente("medico", "Puerto", 2)[0])
    verificar("Duplicado pendiente (incendio en Norte) rechazado", g.registrar_incidente("incendio", "norte", 2)[0] is False)
    verificar("Registrar robo en Isla (#3)", g.registrar_incidente("robo", "Isla", 3)[0])
    verificar("Cola: 3 pendientes, frente #1, último #3",
              g.pendientes.tamano() == 3 and g.pendientes.ver_frente().id == 1 and g.pendientes.ver_ultimo().id == 3)
    verificar("Lista enlazada guarda los 3 incidentes", g.incidentes.tamano() == 3)
    verificar("Pila de historial tiene 3 acciones", g.historial.tamano() == 3)

    ok, msg = g.atender_siguiente()
    i1 = g.buscar_incidente(1)
    verificar("FIFO: se atiende #1 primero; centro B01, costo 4",
              ok and i1.estado == Incidente.ATENDIDO and i1.centro_asignado == "B01" and i1.costo == 4
              and i1.ruta == "Centro -> Norte", msg)
    ok, msg = g.atender_siguiente()
    i2 = g.buscar_incidente(2)
    verificar("#2 médico en Puerto: elige H02 (costo 7) y no H01 (costo 9)",
              ok and i2.centro_asignado == "H02" and i2.costo == 7 and i2.ruta == "Sur -> Puerto", msg)
    ok, msg = g.atender_siguiente()
    i3 = g.buscar_incidente(3)
    verificar("#3 en Isla: no existe camino -> sin cobertura", (not ok) and i3.estado == Incidente.SIN_COBERTURA, msg)
    verificar("Cola vacía tras atender los 3", g.pendientes.esta_vacia() and g.atender_siguiente()[0] is False)

    ok, msg = g.deshacer()
    verificar("Deshacer atención de #3 lo devuelve a pendiente y a la cola",
              ok and i3.estado == Incidente.PENDIENTE and g.pendientes.tamano() == 1, msg)
    verificar("Cancelar #3", g.cancelar_incidente(3)[0] and i3.estado == Incidente.CANCELADO)
    verificar("Cancelar un incidente ya atendido falla", g.cancelar_incidente(1)[0] is False)
    verificar("Cancelar incidente inexistente falla", g.cancelar_incidente(99)[0] is False)
    verificar("Atender salta el cancelado y avisa que no hay pendientes", g.atender_siguiente()[0] is False)
    ok, msg = g.deshacer()
    verificar("Deshacer cancelación reingresa #3 a la cola aunque ya se había saltado",
              ok and i3.estado == Incidente.PENDIENTE and g.pendientes.tamano() == 1, msg)

    verificar("Desconectar Centro-Norte", g.desconectar_zonas("Centro", "Norte")[0])
    verificar("Desconectar de nuevo falla", g.desconectar_zonas("Centro", "Norte")[0] is False)
    verificar("Registrar nuevo incendio en Norte (#4) permitido (el #1 ya no está pendiente)",
              g.registrar_incidente("incendio", "Norte", 1)[0])
    g.atender_siguiente()   # #3 (FIFO) -> sin cobertura
    ok, msg = g.atender_siguiente()
    i4 = g.buscar_incidente(4)
    verificar("Con la conexión cerrada la ruta cambia: B01 por Este, costo 8",
              ok and i4.centro_asignado == "B01" and i4.costo == 8 and i4.ruta == "Centro -> Este -> Norte", msg)

    ok, msg = g.deshacer()
    verificar("Deshacer atención de #4 lo regresa a pendiente", ok and i4.estado == Incidente.PENDIENTE
              and i4.centro_asignado is None, msg)
    n_antes = g.incidentes.tamano()
    ok, msg = g.deshacer()   # deshace sin_cobertura de #3 (acción anterior en la pila)
    ok, msg = g.deshacer()   # y luego sigue
    verificar("Deshacer varias acciones en orden inverso funciona", ok, msg)

    g2 = GestorEmergencias()
    g2.cargar_datos_prueba()
    g2.registrar_incidente("accidente", "Este", 2)
    ok, msg = g2.deshacer()
    verificar("Deshacer un registro elimina el incidente de la lista",
              ok and g2.incidentes.esta_vacia() and g2.atender_siguiente()[0] is False, msg)

    verificar("Buscar incidente inexistente devuelve None", g.buscar_incidente(999) is None)
    verificar("Incidentes por zona sin resultados devuelve lista vacía", g.incidentes_por_zona("Oeste") == [])
    verificar("Buscar centro existente / inexistente",
              g.buscar_centro("h01").nombre == "Hospital Norte" and g.buscar_centro("ZZ9") is None)
    verificar("Eliminar centro B02 (hoja)", g.eliminar_centro("B02")[0] and g.buscar_centro("B02") is None)
    verificar("Eliminar centro H01 (con hijos) conserva el resto",
              g.eliminar_centro("H01")[0] and [c.codigo for c in g.centros.inorden()] == ["B01", "H02", "P01"],
              [c.codigo for c in g.centros.inorden()])
    verificar("Eliminar centro inexistente falla", g.eliminar_centro("NOPE")[0] is False)
    verificar("Mostrar estado devuelve texto con las 5 estructuras",
              all(p in g.estado_estructuras() for p in ("LISTA", "COLA", "PILA", "ÁRBOL", "GRAFO")))


if __name__ == "__main__":
    pruebas_lista()
    pruebas_pila()
    pruebas_cola()
    pruebas_arbol()
    pruebas_grafo()
    pruebas_integracion()
    total = len(_resultados)
    pasadas = sum(1 for r in _resultados if r)
    print("\n=== RESULTADO: %d/%d pruebas exitosas ===" % (pasadas, total))
    sys.exit(0 if pasadas == total else 1)

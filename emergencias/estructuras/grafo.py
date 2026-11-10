from estructuras.lista_enlazada import ListaEnlazada
from estructuras.cola import Cola
from estructuras.pila import Pila

INFINITO = 10 ** 9


class Arista:
    def __init__(self, destino, peso):
        self.destino = destino      # referencia al Vertice destino
        self.peso = peso


class Vertice:
    def __init__(self, nombre):
        self.nombre = nombre
        self.aristas = ListaEnlazada()   # lista de adyacencia
        # campos auxiliares de los algoritmos (se reinician antes de cada uno)
        self.visitado = False
        self.distancia = INFINITO
        self.previo = None


class Grafo:
    """Grafo no dirigido y ponderado con lista de adyacencia.

    Se usa lista de adyacencia (y no matriz) porque el mapa de zonas es
    disperso: ocupa O(V + E) y recorrer los vecinos cuesta O(grado).
    """

    def __init__(self):
        self._vertices = ListaEnlazada()

    # ---------------------------------------------------------- utilidades
    def _obtener(self, nombre):
        return self._vertices.buscar(lambda v: v.nombre == nombre)

    def existe_vertice(self, nombre):
        return self._obtener(nombre) is not None

    def cantidad_vertices(self):
        return self._vertices.tamano()

    def _reiniciar(self):
        for v in self._vertices:
            v.visitado = False
            v.distancia = INFINITO
            v.previo = None

    # ------------------------------------------------------------ vértices
    def agregar_vertice(self, nombre):
        if not nombre or self.existe_vertice(nombre):
            return False
        self._vertices.insertar_final(Vertice(nombre))
        return True

    def vertices(self):
        for v in self._vertices:
            yield v.nombre

    # -------------------------------------------------------------- aristas
    def hay_arista(self, a, b):
        va = self._obtener(a)
        if va is None:
            return False
        return va.aristas.buscar(lambda ar: ar.destino.nombre == b) is not None

    def agregar_arista(self, a, b, peso):
        va, vb = self._obtener(a), self._obtener(b)
        if va is None or vb is None or va is vb or peso <= 0:
            return False
        if self.hay_arista(a, b):
            return False
        va.aristas.insertar_final(Arista(vb, peso))
        vb.aristas.insertar_final(Arista(va, peso))
        return True

    def eliminar_arista(self, a, b):
        va, vb = self._obtener(a), self._obtener(b)
        if va is None or vb is None or not self.hay_arista(a, b):
            return False
        va.aristas.eliminar_donde(lambda ar: ar.destino is vb)
        vb.aristas.eliminar_donde(lambda ar: ar.destino is va)
        return True

    def conexiones(self, nombre):
        v = self._obtener(nombre)
        if v is None:
            return
        for ar in v.aristas:
            yield (ar.destino.nombre, ar.peso)

    # ------------------------------------------------------------ recorridos
    def bfs(self, inicio):
        """Recorrido en anchura usando una Cola propia."""
        v0 = self._obtener(inicio)
        if v0 is None:
            return []
        self._reiniciar()
        orden = []
        cola = Cola()
        v0.visitado = True
        cola.encolar(v0)
        while not cola.esta_vacia():
            v = cola.desencolar()
            orden.append(v.nombre)
            for ar in v.aristas:
                if not ar.destino.visitado:
                    ar.destino.visitado = True
                    cola.encolar(ar.destino)
        return orden

    def dfs(self, inicio):
        """Recorrido en profundidad iterativo usando una Pila propia."""
        v0 = self._obtener(inicio)
        if v0 is None:
            return []
        self._reiniciar()
        orden = []
        pila = Pila()
        pila.apilar(v0)
        while not pila.esta_vacia():
            v = pila.desapilar()
            if v.visitado:
                continue
            v.visitado = True
            orden.append(v.nombre)
            # se invierte el orden de los vecinos para visitar primero el 1.º
            temporal = Pila()
            for ar in v.aristas:
                if not ar.destino.visitado:
                    temporal.apilar(ar.destino)
            while not temporal.esta_vacia():
                pila.apilar(temporal.desapilar())
        return orden

    def existe_camino(self, origen, destino):
        if not self.existe_vertice(destino):
            return False
        for nombre in self.bfs(origen):
            if nombre == destino:
                return True
        return False

    # -------------------------------------------------------------- Dijkstra
    def dijkstra(self, origen, destino):
        """Camino de costo mínimo. Devuelve (costo, [ruta]) o None."""
        vo, vd = self._obtener(origen), self._obtener(destino)
        if vo is None or vd is None:
            return None
        self._reiniciar()
        vo.distancia = 0
        while True:
            actual = None
            for v in self._vertices:
                if (not v.visitado and v.distancia < INFINITO and
                        (actual is None or v.distancia < actual.distancia)):
                    actual = v
            if actual is None:
                break
            actual.visitado = True
            if actual is vd:
                break
            for ar in actual.aristas:
                nueva = actual.distancia + ar.peso
                if not ar.destino.visitado and nueva < ar.destino.distancia:
                    ar.destino.distancia = nueva
                    ar.destino.previo = actual
        if vd.distancia >= INFINITO:
            return None
        # se reconstruye la ruta con una Pila (de destino a origen)
        pila = Pila()
        v = vd
        while v is not None:
            pila.apilar(v.nombre)
            v = v.previo
        ruta = []
        while not pila.esta_vacia():
            ruta.append(pila.desapilar())
        return (vd.distancia, ruta)

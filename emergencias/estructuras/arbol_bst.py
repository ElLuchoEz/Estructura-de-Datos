class NodoArbol:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierdo = None
        self.derecho = None


class ArbolBST:
    """Árbol binario de búsqueda. Las claves duplicadas no se permiten."""

    def __init__(self):
        self._raiz = None
        self._tamano = 0
        self._eliminado = False

    def esta_vacio(self):
        return self._raiz is None

    # ---------------------------------------------------------- inserción
    def insertar(self, clave, valor):
        """Inserta. Devuelve False si la clave ya existe."""
        nuevo = NodoArbol(clave, valor)
        if self._raiz is None:
            self._raiz = nuevo
            self._tamano = 1
            return True
        actual = self._raiz
        while True:
            if clave == actual.clave:
                return False
            if clave < actual.clave:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    break
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    break
                actual = actual.derecho
        self._tamano += 1
        return True

    # ------------------------------------------------------------ búsqueda
    def buscar(self, clave):
        """Devuelve el valor asociado a la clave o None si no existe."""
        actual = self._raiz
        while actual is not None:
            if clave == actual.clave:
                return actual.valor
            actual = actual.izquierdo if clave < actual.clave else actual.derecho
        return None

    # ----------------------------------------------------------- eliminación
    def eliminar(self, clave):
        """Elimina la clave. Devuelve True si existía."""
        self._eliminado = False
        self._raiz = self._eliminar(self._raiz, clave)
        return self._eliminado

    def _eliminar(self, nodo, clave):
        if nodo is None:
            return None
        if clave < nodo.clave:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._eliminar(nodo.derecho, clave)
        else:
            self._eliminado = True
            self._tamano -= 1
            if nodo.izquierdo is None:      # hoja o solo hijo derecho
                return nodo.derecho
            if nodo.derecho is None:        # solo hijo izquierdo
                return nodo.izquierdo
            # dos hijos: se reemplaza por el sucesor inorden
            sucesor = nodo.derecho
            while sucesor.izquierdo is not None:
                sucesor = sucesor.izquierdo
            nodo.clave = sucesor.clave
            nodo.valor = sucesor.valor
            nodo.derecho = self._quitar_minimo(nodo.derecho)
        return nodo

    def _quitar_minimo(self, nodo):
        if nodo.izquierdo is None:
            return nodo.derecho
        nodo.izquierdo = self._quitar_minimo(nodo.izquierdo)
        return nodo

    # ------------------------------------------------------------ recorridos
    def preorden(self):
        yield from self._preorden(self._raiz)

    def _preorden(self, nodo):
        if nodo is None:
            return
        yield nodo.valor
        yield from self._preorden(nodo.izquierdo)
        yield from self._preorden(nodo.derecho)

    def inorden(self):
        yield from self._inorden(self._raiz)

    def _inorden(self, nodo):
        if nodo is None:
            return
        yield from self._inorden(nodo.izquierdo)
        yield nodo.valor
        yield from self._inorden(nodo.derecho)

    def postorden(self):
        yield from self._postorden(self._raiz)

    def _postorden(self, nodo):
        if nodo is None:
            return
        yield from self._postorden(nodo.izquierdo)
        yield from self._postorden(nodo.derecho)
        yield nodo.valor

    # ----------------------------------------------------------- propiedades
    def cantidad_nodos(self):
        return self._tamano

    def altura(self):
        """Altura en nodos: árbol vacío = 0, solo la raíz = 1."""
        return self._altura(self._raiz)

    def _altura(self, nodo):
        if nodo is None:
            return 0
        izq = self._altura(nodo.izquierdo)
        der = self._altura(nodo.derecho)
        return 1 + (izq if izq > der else der)

    def cantidad_hojas(self):
        return self._hojas(self._raiz)

    def _hojas(self, nodo):
        if nodo is None:
            return 0
        if nodo.izquierdo is None and nodo.derecho is None:
            return 1
        return self._hojas(nodo.izquierdo) + self._hojas(nodo.derecho)

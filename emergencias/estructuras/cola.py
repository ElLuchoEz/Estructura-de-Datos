from estructuras.nodo import Nodo


class Cola:
    """Cola simple (FIFO) con referencias al frente y al final."""

    def __init__(self):
        self._frente = None
        self._final = None
        self._tamano = 0

    def encolar(self, dato):
        nuevo = Nodo(dato)
        if self._final is None:
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._tamano += 1

    def desencolar(self):
        """Devuelve y quita el frente. Devuelve None si está vacía."""
        if self.esta_vacia():
            return None
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._tamano -= 1
        return dato

    def ver_frente(self):
        return None if self.esta_vacia() else self._frente.dato

    def ver_ultimo(self):
        return None if self.esta_vacia() else self._final.dato

    def tamano(self):
        return self._tamano

    def esta_vacia(self):
        return self._frente is None

    def contiene(self, predicado):
        actual = self._frente
        while actual is not None:
            if predicado(actual.dato):
                return True
            actual = actual.siguiente
        return False

    def recorrer(self):
        actual = self._frente
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def mostrar(self):
        if self.esta_vacia():
            return "(cola vacía)"
        return " <- ".join(str(d) for d in self.recorrer())

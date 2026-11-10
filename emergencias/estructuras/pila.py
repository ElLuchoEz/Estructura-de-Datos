from estructuras.nodo import Nodo


class Pila:
    """Pila (LIFO) implementada con nodos enlazados."""

    def __init__(self):
        self._tope = None
        self._tamano = 0

    def apilar(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self._tope
        self._tope = nuevo
        self._tamano += 1

    def desapilar(self):
        """Devuelve y quita el tope. Devuelve None si está vacía."""
        if self.esta_vacia():
            return None
        dato = self._tope.dato
        self._tope = self._tope.siguiente
        self._tamano -= 1
        return dato

    def ver_tope(self):
        return None if self.esta_vacia() else self._tope.dato

    def tamano(self):
        return self._tamano

    def esta_vacia(self):
        return self._tope is None

    def recorrer(self):
        """Recorre del tope hacia la base sin modificar la pila."""
        actual = self._tope
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def mostrar(self):
        if self.esta_vacia():
            return "(pila vacía)"
        return " | ".join(str(d) for d in self.recorrer())

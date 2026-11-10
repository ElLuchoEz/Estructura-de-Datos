from estructuras.nodo import Nodo


class ListaEnlazada:
    """Lista simplemente enlazada con referencia a cabeza y cola.

    Se elige simple (y no doble) porque el sistema solo recorre en un sentido
    y la inserción al final es O(1) gracias a la referencia a la cola.
    """

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._tamano = 0

    def esta_vacia(self):
        return self._cabeza is None

    def tamano(self):
        return self._tamano

    def insertar_inicio(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self._cabeza
        self._cabeza = nuevo
        if self._cola is None:
            self._cola = nuevo
        self._tamano += 1

    def insertar_final(self, dato):
        nuevo = Nodo(dato)
        if self._cola is None:
            self._cabeza = nuevo
        else:
            self._cola.siguiente = nuevo
        self._cola = nuevo
        self._tamano += 1

    def eliminar_inicio(self):
        """Elimina y devuelve el primer dato. Devuelve None si está vacía."""
        if self.esta_vacia():
            return None
        dato = self._cabeza.dato
        self._cabeza = self._cabeza.siguiente
        if self._cabeza is None:
            self._cola = None
        self._tamano -= 1
        return dato

    def eliminar_final(self):
        """Elimina y devuelve el último dato. Devuelve None si está vacía."""
        if self.esta_vacia():
            return None
        dato = self._cola.dato
        if self._cabeza is self._cola:
            self._cabeza = None
            self._cola = None
        else:
            penultimo = self._cabeza
            while penultimo.siguiente is not self._cola:
                penultimo = penultimo.siguiente
            penultimo.siguiente = None
            self._cola = penultimo
        self._tamano -= 1
        return dato

    def buscar(self, predicado):
        """Devuelve el primer dato que cumple el predicado, o None."""
        actual = self._cabeza
        while actual is not None:
            if predicado(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def eliminar_donde(self, predicado):
        """Elimina el primer dato que cumple el predicado y lo devuelve."""
        anterior = None
        actual = self._cabeza
        while actual is not None:
            if predicado(actual.dato):
                if anterior is None:
                    self._cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                if actual is self._cola:
                    self._cola = anterior
                self._tamano -= 1
                return actual.dato
            anterior = actual
            actual = actual.siguiente
        return None

    def recorrer(self):
        actual = self._cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __iter__(self):
        return self.recorrer()

    def mostrar(self):
        if self.esta_vacia():
            return "(lista vacía)"
        return " -> ".join(str(d) for d in self.recorrer())

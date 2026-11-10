class Nodo:
    """Nodo simple usado por la lista enlazada, la pila y la cola."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

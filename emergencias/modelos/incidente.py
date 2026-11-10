class Incidente:
    PENDIENTE = "pendiente"
    ATENDIDO = "atendido"
    CANCELADO = "cancelado"
    SIN_COBERTURA = "sin_cobertura"
    ANULADO = "anulado"

    TIPOS = ("incendio", "accidente", "medico", "robo")

    def __init__(self, id_incidente, tipo, zona, prioridad, descripcion=""):
        self.id = id_incidente
        self.tipo = tipo
        self.zona = zona
        self.prioridad = prioridad        # 1 = alta, 2 = media, 3 = baja
        self.descripcion = descripcion
        self.estado = Incidente.PENDIENTE
        self.centro_asignado = None       # código del centro (referencia)
        self.ruta = None
        self.costo = None

    def servicio_requerido(self):
        """Tipo de centro que debe atender este incidente."""
        if self.tipo == "incendio":
            return "bomberos"
        if self.tipo == "robo":
            return "policia"
        return "hospital"                 # accidente y médico

    def limpiar_asignacion(self):
        self.centro_asignado = None
        self.ruta = None
        self.costo = None

    def __str__(self):
        texto = "#%d %s en %s (prioridad %d) [%s]" % (
            self.id, self.tipo, self.zona, self.prioridad, self.estado)
        if self.centro_asignado is not None:
            texto += " -> %s, costo %s, ruta %s" % (
                self.centro_asignado, self.costo, self.ruta)
        return texto

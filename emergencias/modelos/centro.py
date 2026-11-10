class Centro:
    TIPOS = ("bomberos", "hospital", "policia")

    def __init__(self, codigo, nombre, tipo, zona):
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.zona = zona

    def __str__(self):
        return "%s - %s (%s, zona %s)" % (self.codigo, self.nombre, self.tipo, self.zona)

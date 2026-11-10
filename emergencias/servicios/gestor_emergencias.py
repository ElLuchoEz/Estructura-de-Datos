from estructuras.lista_enlazada import ListaEnlazada
from estructuras.pila import Pila
from estructuras.cola import Cola
from estructuras.arbol_bst import ArbolBST
from estructuras.grafo import Grafo
from modelos.incidente import Incidente
from modelos.centro import Centro


class GestorEmergencias:
    """Integra las cinco estructuras en un mismo flujo.

    - ListaEnlazada: registro de TODOS los incidentes (consulta/búsqueda).
    - Cola:          incidentes pendientes, atendidos en orden de llegada.
    - Pila:          historial de acciones para deshacer (LIFO).
    - ArbolBST:      centros de atención ordenados por código.
    - Grafo:         zonas y distancias; calcula la ruta centro -> incidente.

    Consistencia: la lista y la cola guardan la MISMA referencia al objeto
    Incidente (no copias), así el estado nunca se desincroniza. Los incidentes
    guardan solo el código del centro, no el objeto.
    """

    def __init__(self):
        self.incidentes = ListaEnlazada()
        self.pendientes = Cola()
        self.historial = Pila()
        self.centros = ArbolBST()
        self.mapa = Grafo()
        self._siguiente_id = 1

    # ------------------------------------------------------------- mapa
    def registrar_zona(self, nombre):
        nombre = nombre.strip().title()
        if not nombre:
            return False, "El nombre de la zona no puede estar vacío."
        if not self.mapa.agregar_vertice(nombre):
            return False, "La zona '%s' ya existe." % nombre
        return True, "Zona '%s' registrada." % nombre

    def conectar_zonas(self, a, b, distancia):
        a, b = a.strip().title(), b.strip().title()
        if not self.mapa.existe_vertice(a) or not self.mapa.existe_vertice(b):
            return False, "Ambas zonas deben existir."
        if a == b:
            return False, "Una zona no puede conectarse consigo misma."
        if distancia <= 0:
            return False, "La distancia debe ser mayor que cero."
        if not self.mapa.agregar_arista(a, b, distancia):
            return False, "Ya existe una conexión entre %s y %s." % (a, b)
        return True, "Conexión %s <-> %s (%s) creada." % (a, b, distancia)

    def desconectar_zonas(self, a, b):
        a, b = a.strip().title(), b.strip().title()
        if not self.mapa.eliminar_arista(a, b):
            return False, "No existe conexión entre %s y %s." % (a, b)
        return True, "Conexión %s <-> %s deshabilitada." % (a, b)

    # ----------------------------------------------------------- centros
    def registrar_centro(self, codigo, nombre, tipo, zona):
        codigo = codigo.strip().upper()
        tipo = tipo.strip().lower()
        zona = zona.strip().title()
        if not codigo or not nombre.strip():
            return False, "Código y nombre son obligatorios."
        if tipo not in Centro.TIPOS:
            return False, "Tipo inválido. Opciones: %s." % ", ".join(Centro.TIPOS)
        if not self.mapa.existe_vertice(zona):
            return False, "La zona '%s' no existe." % zona
        if not self.centros.insertar(codigo, Centro(codigo, nombre.strip(), tipo, zona)):
            return False, "Ya existe un centro con el código %s." % codigo
        return True, "Centro %s registrado." % codigo

    def buscar_centro(self, codigo):
        return self.centros.buscar(codigo.strip().upper())

    def eliminar_centro(self, codigo):
        if not self.centros.eliminar(codigo.strip().upper()):
            return False, "No existe el centro %s." % codigo.strip().upper()
        return True, "Centro %s eliminado." % codigo.strip().upper()

    # --------------------------------------------------------- incidentes
    def registrar_incidente(self, tipo, zona, prioridad, descripcion=""):
        tipo = tipo.strip().lower()
        zona = zona.strip().title()
        if tipo not in Incidente.TIPOS:
            return False, "Tipo inválido. Opciones: %s." % ", ".join(Incidente.TIPOS)
        if not self.mapa.existe_vertice(zona):
            return False, "La zona '%s' no existe." % zona
        if prioridad not in (1, 2, 3):
            return False, "La prioridad debe ser 1 (alta), 2 (media) o 3 (baja)."
        # Regla de duplicados: no puede haber dos pendientes del mismo tipo y zona
        repetido = self.incidentes.buscar(
            lambda i: i.tipo == tipo and i.zona == zona
            and i.estado == Incidente.PENDIENTE)
        if repetido is not None:
            return False, "Ya hay un incidente pendiente igual (#%d)." % repetido.id
        incidente = Incidente(self._siguiente_id, tipo, zona, prioridad, descripcion)
        self._siguiente_id += 1
        self.incidentes.insertar_final(incidente)
        self.pendientes.encolar(incidente)
        self.historial.apilar(("REGISTRAR", incidente))
        return True, "Incidente #%d registrado." % incidente.id

    def buscar_incidente(self, id_incidente):
        return self.incidentes.buscar(lambda i: i.id == id_incidente)

    def incidentes_por_zona(self, zona):
        zona = zona.strip().title()
        return [i for i in self.incidentes if i.zona == zona]

    def cancelar_incidente(self, id_incidente):
        incidente = self.buscar_incidente(id_incidente)
        if incidente is None:
            return False, "No existe el incidente #%s." % id_incidente
        if incidente.estado != Incidente.PENDIENTE:
            return False, "Solo se cancelan incidentes pendientes (estado: %s)." % incidente.estado
        incidente.estado = Incidente.CANCELADO
        self.historial.apilar(("CANCELAR", incidente))
        return True, "Incidente #%d cancelado." % id_incidente

    # ---------------------------------------------------- flujo principal
    def atender_siguiente(self):
        """Cola -> Árbol -> Grafo -> Lista (estado) -> Pila (historial)."""
        incidente = None
        while not self.pendientes.esta_vacia():
            candidato = self.pendientes.desencolar()
            if candidato.estado == Incidente.PENDIENTE:   # salta cancelados/anulados
                incidente = candidato
                break
        if incidente is None:
            return False, "No hay incidentes pendientes."

        servicio = incidente.servicio_requerido()
        mejor = None
        for centro in self.centros.inorden():               # árbol
            if centro.tipo != servicio:
                continue
            resultado = self.mapa.dijkstra(centro.zona, incidente.zona)   # grafo
            if resultado is None:
                continue
            if mejor is None or resultado[0] < mejor[0]:
                mejor = (resultado[0], resultado[1], centro)

        if mejor is None:
            incidente.estado = Incidente.SIN_COBERTURA
            self.historial.apilar(("ATENDER", incidente))
            return False, ("Incidente #%d sin cobertura: ningún centro de tipo '%s' "
                           "tiene ruta hasta %s." % (incidente.id, servicio, incidente.zona))

        costo, ruta, centro = mejor
        incidente.estado = Incidente.ATENDIDO
        incidente.centro_asignado = centro.codigo
        incidente.costo = costo
        incidente.ruta = " -> ".join(ruta)
        self.historial.apilar(("ATENDER", incidente))
        return True, "Incidente #%d atendido por %s. Costo %s. Ruta: %s." % (
            incidente.id, centro.codigo, costo, incidente.ruta)

    def deshacer(self):
        if self.historial.esta_vacia():
            return False, "No hay acciones para deshacer."
        accion, incidente = self.historial.desapilar()
        if accion == "REGISTRAR":
            incidente.estado = Incidente.ANULADO   # la cola lo saltará
            self.incidentes.eliminar_donde(lambda i: i.id == incidente.id)
            return True, "Se deshizo el registro del incidente #%d." % incidente.id
        # CANCELAR o ATENDER: vuelve a pendiente
        incidente.estado = Incidente.PENDIENTE
        incidente.limpiar_asignacion()
        if not self.pendientes.contiene(lambda i: i is incidente):
            self.pendientes.encolar(incidente)      # reingresa al final de la cola
        return True, "Se deshizo '%s' del incidente #%d (vuelve a pendiente)." % (
            accion.lower(), incidente.id)

    # --------------------------------------------------------- reportes
    def estado_estructuras(self):
        lineas = []
        lineas.append("LISTA ENLAZADA - incidentes (%d):" % self.incidentes.tamano())
        if self.incidentes.esta_vacia():
            lineas.append("   (vacía)")
        for i in self.incidentes:
            lineas.append("   " + str(i))
        lineas.append("COLA - pendientes (%d): %s" % (
            self.pendientes.tamano(),
            " <- ".join("#%d" % i.id for i in self.pendientes.recorrer())
            if not self.pendientes.esta_vacia() else "(vacía)"))
        lineas.append("PILA - historial (%d), tope primero:" % self.historial.tamano())
        if self.historial.esta_vacia():
            lineas.append("   (vacía)")
        for accion, inc in self.historial.recorrer():
            lineas.append("   %s #%d" % (accion, inc.id))
        lineas.append("ÁRBOL - centros (nodos=%d, altura=%d, hojas=%d), inorden:" % (
            self.centros.cantidad_nodos(), self.centros.altura(),
            self.centros.cantidad_hojas()))
        if self.centros.esta_vacio():
            lineas.append("   (vacío)")
        for c in self.centros.inorden():
            lineas.append("   " + str(c))
        lineas.append("GRAFO - zonas (%d):" % self.mapa.cantidad_vertices())
        for zona in self.mapa.vertices():
            vecinos = ", ".join("%s(%s)" % (d, p) for d, p in self.mapa.conexiones(zona))
            lineas.append("   %s: %s" % (zona, vecinos if vecinos else "(aislada)"))
        return "\n".join(lineas)

    # ----------------------------------------------------- datos de prueba
    def cargar_datos_prueba(self):
        for zona in ("Centro", "Norte", "Sur", "Este", "Oeste", "Puerto", "Isla"):
            self.registrar_zona(zona)
        for a, b, d in (("Centro", "Norte", 4), ("Centro", "Sur", 5),
                        ("Centro", "Este", 3), ("Centro", "Oeste", 6),
                        ("Norte", "Este", 5), ("Sur", "Puerto", 7),
                        ("Este", "Puerto", 4)):
            self.conectar_zonas(a, b, d)
        # Isla queda aislada a propósito (caso "no existe camino")
        for datos in (("H01", "Hospital Norte", "hospital", "Norte"),
                      ("B01", "Bomberos Central", "bomberos", "Centro"),
                      ("P01", "Policía Este", "policia", "Este"),
                      ("B02", "Bomberos Puerto", "bomberos", "Puerto"),
                      ("H02", "Hospital Sur", "hospital", "Sur")):
            self.registrar_centro(*datos)

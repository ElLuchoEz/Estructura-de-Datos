from servicios.gestor_emergencias import GestorEmergencias

MENU = """
===== SISTEMA DE GESTIÓN DE EMERGENCIAS =====
 1. Cargar datos de prueba
 2. Registrar zona
 3. Conectar zonas
 4. Deshabilitar conexión entre zonas
 5. Registrar centro de atención
 6. Registrar incidente
 7. Atender siguiente incidente
 8. Cancelar incidente
 9. Deshacer última acción
10. Buscar incidente por id
11. Listar incidentes de una zona
12. Buscar centro por código
13. Eliminar centro
14. Recorridos del árbol (preorden/inorden/postorden)
15. Recorridos del grafo (BFS/DFS)
16. ¿Hay conexión? / Ruta más corta entre zonas
17. Mostrar estado de las estructuras
 0. Salir
"""


def leer_entero(mensaje):
    try:
        return int(input(mensaje))
    except ValueError:
        return None


def mostrar(resultado):
    print(("  OK: " if resultado[0] else "  ERROR: ") + resultado[1])


def main():
    gestor = GestorEmergencias()
    while True:
        print(MENU)
        opcion = input("Opción: ").strip()
        if opcion == "0":
            print("Hasta luego.")
            break
        elif opcion == "1":
            gestor.cargar_datos_prueba()
            print("  Datos de prueba cargados (zonas, conexiones y 5 centros).")
        elif opcion == "2":
            mostrar(gestor.registrar_zona(input("Nombre de la zona: ")))
        elif opcion == "3":
            a = input("Zona A: ")
            b = input("Zona B: ")
            d = leer_entero("Distancia: ")
            if d is None:
                print("  ERROR: la distancia debe ser un número entero.")
            else:
                mostrar(gestor.conectar_zonas(a, b, d))
        elif opcion == "4":
            mostrar(gestor.desconectar_zonas(input("Zona A: "), input("Zona B: ")))
        elif opcion == "5":
            mostrar(gestor.registrar_centro(
                input("Código: "), input("Nombre: "),
                input("Tipo (bomberos/hospital/policia): "), input("Zona: ")))
        elif opcion == "6":
            tipo = input("Tipo (incendio/accidente/medico/robo): ")
            zona = input("Zona: ")
            prioridad = leer_entero("Prioridad (1 alta, 2 media, 3 baja): ")
            if prioridad is None:
                print("  ERROR: la prioridad debe ser un número.")
            else:
                mostrar(gestor.registrar_incidente(tipo, zona, prioridad,
                                                   input("Descripción (opcional): ")))
        elif opcion == "7":
            mostrar(gestor.atender_siguiente())
        elif opcion == "8":
            id_inc = leer_entero("Id del incidente: ")
            if id_inc is None:
                print("  ERROR: el id debe ser un número.")
            else:
                mostrar(gestor.cancelar_incidente(id_inc))
        elif opcion == "9":
            mostrar(gestor.deshacer())
        elif opcion == "10":
            id_inc = leer_entero("Id del incidente: ")
            inc = gestor.buscar_incidente(id_inc) if id_inc is not None else None
            print("  " + str(inc) if inc else "  No se encontró el incidente.")
        elif opcion == "11":
            lista = gestor.incidentes_por_zona(input("Zona: "))
            if not lista:
                print("  No hay incidentes en esa zona.")
            for inc in lista:
                print("  " + str(inc))
        elif opcion == "12":
            centro = gestor.buscar_centro(input("Código: "))
            print("  " + str(centro) if centro else "  No se encontró el centro.")
        elif opcion == "13":
            mostrar(gestor.eliminar_centro(input("Código: ")))
        elif opcion == "14":
            if gestor.centros.esta_vacio():
                print("  El árbol está vacío.")
            else:
                print("  Preorden :", [c.codigo for c in gestor.centros.preorden()])
                print("  Inorden  :", [c.codigo for c in gestor.centros.inorden()])
                print("  Postorden:", [c.codigo for c in gestor.centros.postorden()])
        elif opcion == "15":
            zona = input("Zona de inicio: ").strip().title()
            if not gestor.mapa.existe_vertice(zona):
                print("  La zona no existe.")
            else:
                print("  BFS:", " -> ".join(gestor.mapa.bfs(zona)))
                print("  DFS:", " -> ".join(gestor.mapa.dfs(zona)))
        elif opcion == "16":
            a = input("Zona origen: ").strip().title()
            b = input("Zona destino: ").strip().title()
            if not (gestor.mapa.existe_vertice(a) and gestor.mapa.existe_vertice(b)):
                print("  Ambas zonas deben existir.")
            elif not gestor.mapa.existe_camino(a, b):
                print("  NO existe camino entre %s y %s." % (a, b))
            else:
                costo, ruta = gestor.mapa.dijkstra(a, b)
                print("  Existe camino. Costo mínimo %s. Ruta: %s" % (costo, " -> ".join(ruta)))
        elif opcion == "17":
            print(gestor.estado_estructuras())
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    main()

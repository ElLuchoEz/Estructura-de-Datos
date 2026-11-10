# Sistema de Gestión de Emergencias

Proyecto final de **Estructuras de Datos** (periodo 2620).

## 1. Información general

| Campo | Contenido |
|---|---|
| Proyecto | Sistema de Gestión de Emergencias |
| Integrantes | *(completar: nombres de los integrantes)* |
| Lenguaje | Python 3 (sin dependencias externas) |
| Interfaz | Consola |

**Situación atendida.** Los servicios de emergencia de una ciudad reciben incidentes (incendios, accidentes, emergencias médicas, robos) que deben atenderse en orden de llegada, enviando al centro de atención adecuado más cercano por el mejor camino disponible.

**Problema identificado.** Sin un sistema, es difícil saber qué incidentes siguen pendientes, qué centro conviene enviar, qué ruta es la más corta cuando una vía se cierra y cómo corregir un error de registro.

**Objetivo general.** Gestionar el ciclo de vida de los incidentes (registro, atención, cancelación y deshacer) integrando lista enlazada, cola, pila, árbol y grafo, todos implementados manualmente.

**Actores.** Operador del centro de despacho (usa el sistema), ciudadanos que reportan, centros de atención (bomberos, hospital, policía).

**Alcance.** Incluye registrar zonas, conexiones, centros e incidentes; atender en FIFO; calcular la ruta; cancelar; deshacer; consultar y buscar.
**Fuera del alcance:** mapas reales/GPS, tiempo real, múltiples unidades por centro, interfaz gráfica, persistencia en archivos o base de datos, prioridad como criterio de orden (ver "Limitaciones").

## 2. Descripción de la solución

### Funcionalidades
Registrar zonas / conectar y deshabilitar conexiones / registrar, buscar y eliminar centros / registrar incidentes / atender el siguiente / cancelar / deshacer / buscar por id / listar por zona / recorridos del árbol / BFS y DFS / consultar conexión y ruta mínima / mostrar el estado de todas las estructuras.

### Flujo principal (`atender_siguiente`)
1. El incidente sale del **frente de la cola** (FIFO). Se saltan los cancelados o anulados.
2. Se recorre el **árbol** de centros (inorden) y se filtran los del tipo requerido (incendio → bomberos, robo → policía, accidente/médico → hospital).
3. Para cada centro candidato se calcula con el **grafo** (Dijkstra) la ruta hasta la zona del incidente y se elige la de menor costo.
4. Se actualiza el estado del incidente, que vive en la **lista enlazada**.
5. La acción se registra en la **pila** de historial para poder deshacerla.

### Reglas del sistema
- Los códigos de centro y los nombres de zona se normalizan (mayúsculas / formato título), así `norte` y `Norte` son la misma zona.
- **Duplicados:** no se permiten dos centros con el mismo código, dos zonas con el mismo nombre, dos conexiones entre el mismo par de zonas, ni dos incidentes *pendientes* del mismo tipo y zona.
- La prioridad (1 alta, 2 media, 3 baja) es informativa; el orden de atención es solo por llegada.
- Si ningún centro adecuado tiene camino al incidente, queda en estado `sin_cobertura`.
- Solo se pueden cancelar incidentes pendientes.
- Deshacer una atención o cancelación devuelve el incidente a pendiente y lo reencola **al final** (una cola FIFO no permite insertar al frente).
- **Consistencia:** la lista y la cola guardan la *misma referencia* al objeto `Incidente` (no copias), y cada incidente guarda solo el código del centro. Así el estado nunca se desincroniza entre estructuras.

## 3. Diseño de estructuras

| Estructura | Información almacenada | Operaciones utilizadas | Función dentro del sistema | Razón de selección | Alternativa considerada |
|---|---|---|---|---|---|
| Lista enlazada (simple, con cabeza y cola) | Todos los incidentes registrados | insertar final, eliminar por condición, buscar, recorrer, tamaño | Registro histórico y consulta (por id, por zona) | Se recorre en un solo sentido y insertar al final es O(1) con referencia a la cola | Lista doblemente enlazada (innecesaria: nunca se recorre hacia atrás) |
| Pila | Acciones realizadas (registrar, atender, cancelar) con su incidente | apilar, desapilar, ver tope, recorrer | Deshacer en orden inverso | El comportamiento LIFO coincide exactamente con "deshacer la última acción" | Lista con borrado al final (O(n) por no tener acceso directo al penúltimo) |
| Cola (simple) | Referencias a incidentes pendientes | encolar, desencolar, ver frente/último, contiene | Atender solicitudes en orden de llegada | FIFO: el primero en llegar es el primero en ser atendido | Cola priorizada (se descartó por simplicidad y porque el enunciado pide justificar su uso) |
| Árbol binario de búsqueda | Centros de atención, con el código como clave | insertar, buscar, eliminar, preorden, inorden, postorden, altura, nodos, hojas | Localizar centros por código y recorrerlos ordenados para elegir candidatos | Búsqueda promedio O(log n) y recorrido inorden ordenado | Lista enlazada de centros (búsqueda O(n)) |
| Grafo no dirigido ponderado (lista de adyacencia) | Zonas (vértices) y distancias (aristas) | agregar vértice/arista, eliminar arista, BFS, DFS, existe camino, Dijkstra | Calcular la ruta mínima del centro al incidente y detectar zonas incomunicadas | El mapa es disperso: lista de adyacencia ocupa O(V+E) | Matriz de adyacencia (O(V²) de memoria) |

## 4. Algoritmos

**Operaciones principales.** Lista: insertar inicio/final, eliminar inicio/final/por condición, buscar, recorrer. Pila y cola: operaciones clásicas con nodos enlazados. Árbol: inserción iterativa, eliminación recursiva (hoja, un hijo, dos hijos con sucesor inorden).

**Recorridos del árbol.** Preorden (raíz, izq, der), inorden (izq, raíz, der; da los códigos ordenados) y postorden (izq, der, raíz), todos recursivos.

**BFS.** Usa la `Cola` propia: se marca el vértice al encolarlo y se visitan los vecinos por niveles.

**DFS.** Iterativo con la `Pila` propia: se desapila un vértice, se visita si no lo estaba y se apilan sus vecinos (en orden inverso para visitar primero al primer vecino).

**Camino mínimo: Dijkstra.** Se eligió porque las aristas tienen pesos positivos (distancias). Cada iteración toma el vértice no visitado de menor distancia, lo cierra y relaja sus vecinos. La ruta se reconstruye siguiendo los predecesores con una `Pila`. Implementación de selección lineal, O(V²), suficiente para un mapa de decenas de zonas.

**Interacción entre estructuras.** Cola → Árbol → Grafo → Lista → Pila (ver flujo principal). Además el grafo usa internamente la cola (BFS) y la pila (DFS y reconstrucción de ruta).

**Complejidad temporal aproximada** (n = elementos, h = altura, V = vértices, E = aristas, C = centros):

| Operación | Complejidad |
|---|---|
| Lista: insertar inicio / final | O(1) |
| Lista: eliminar inicio | O(1) |
| Lista: eliminar final / buscar / eliminar por condición | O(n) |
| Pila: apilar / desapilar / tope | O(1) |
| Cola: encolar / desencolar / frente | O(1) |
| Árbol: insertar / buscar / eliminar | O(h): O(log n) promedio, O(n) peor caso (árbol degenerado) |
| Árbol: recorridos, altura, hojas | O(n) |
| Grafo: BFS / DFS | O(V + E) |
| Grafo: Dijkstra | O(V²) |
| Atender un incidente | O(C · V²), dominado por los Dijkstra de los centros candidatos |

## 5. Evidencias de prueba

Se ejecutan con `python pruebas/pruebas.py`. Resultado: **106/106 pruebas exitosas**. Cada prueba imprime `[OK]` o `[FALLA]` junto con el valor obtenido si falla.

| Caso requerido | Dato de entrada | Resultado esperado | Resultado obtenido |
|---|---|---|---|
| Inserciones en cada estructura | Valores 1,2,3 / 50,30,70... / incidentes y centros | Estructuras con los datos y tamaños correctos | OK |
| Eliminaciones en cada estructura | Eliminar inicio, final, hoja, nodo con 1 y 2 hijos, raíz, arista | Estructura consistente y orden conservado | OK |
| Búsqueda exitosa | Buscar 60 en el árbol; centro `h01` | Valor encontrado | OK |
| Búsqueda sin resultado | Buscar 65; centro `ZZ9`; incidente 999 | `None` / mensaje informativo | OK |
| Operaciones sobre estructuras vacías | Desapilar, desencolar, eliminar en árbol y lista vacíos; atender sin pendientes; deshacer sin historial | `None` o mensaje de error, sin excepciones | OK |
| Manejo de duplicados | Centro `B01` repetido; vértice repetido; arista repetida; incendio pendiente repetido | Rechazado con mensaje | OK |
| Recorridos del árbol | Árbol 50,30,70,20,40,60,80 | Pre `50 30 20 40 70 60 80`, in `20..80`, post `20 40 30 60 80 70 50` | OK |
| BFS y DFS | Desde `Centro` | BFS `Centro Norte Sur Este Oeste Puerto`; DFS `Centro Norte Este Puerto Sur Oeste` | OK |
| Camino en el grafo | `Centro -> Puerto` | Costo 7 por `Este` | OK |
| No existe camino | `Centro -> Isla` (zona aislada) | `existe_camino = False`, Dijkstra `None` | OK |
| Cambio de ruta al cerrar una vía | Cerrar `Este-Puerto` | Costo pasa de 7 a 12 por `Sur` | OK |
| Interacción entre varias estructuras | Registrar 3 incidentes y atenderlos | FIFO; #1 → B01 (costo 4); #2 → H02 (costo 7, no H01 con 9); #3 sin cobertura | OK |
| Operaciones inválidas | Zona inexistente, tipo inválido, prioridad 7, cancelar ya atendido | Rechazo con mensaje | OK |
| Deshacer / cancelar | Deshacer atención, cancelar, deshacer cancelación | Estados y cola consistentes | OK |

**Correcciones realizadas durante el desarrollo:** *(completar con los errores reales que encuentren al probar y cómo los corrigieron)*.

## 6. Instrucciones de ejecución

- **Software requerido:** Python 3.8 o superior (probado con Python 3).
- **Dependencias:** ninguna (solo biblioteca estándar; no se usan colecciones nativas como sustituto de las estructuras).
- **Ejecutar el sistema:** `python main.py`
- **Ejecutar las pruebas:** `python pruebas/pruebas.py`
- **Datos de prueba:** en el menú, opción **1** carga 7 zonas (`Isla` queda aislada a propósito), 7 conexiones y 5 centros.
- **Credenciales:** no se necesitan.

Demostración rápida: opción 1, luego opción 6 (registrar incidente), opción 7 (atender), opción 17 (ver estado de las estructuras).

Estructura del repositorio:

```
main.py                         menú de consola
estructuras/                    nodo, lista_enlazada, pila, cola, arbol_bst, grafo
modelos/                        incidente, centro
servicios/gestor_emergencias.py flujo que integra las 5 estructuras
pruebas/pruebas.py              casos de prueba
```

## 7. Distribución de responsabilidades

*(Completar con la información real de cada integrante)*

| Integrante | Componentes en los que participó | Aportes realizados | Evidencia (commits / archivos) |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |

Todos los integrantes revisaron y comprenden la solución completa.

## 8. Limitaciones y mejoras posibles

- La prioridad no altera el orden de atención. Una mejora natural es una cola priorizada.
- Dijkstra usa selección lineal, O(V²). Con muchas zonas convendría un montículo.
- El árbol no se auto-balancea, por lo que puede degenerar si se insertan códigos ya ordenados.
- Deshacer reencola el incidente al final, no en su posición original.
- Un centro se atiende sin límite de capacidad.
- No hay persistencia: los datos se pierden al cerrar.

## 9. Declaración de uso de inteligencia artificial

*(Completar de forma honesta con lo que realmente hizo el equipo. El enunciado pide que cada estudiante pueda explicar y modificar el código.)*

| Aspecto | Detalle |
|---|---|
| Herramientas utilizadas | Claude (Anthropic) |
| Actividades en las que se usó | Elección del tema, diseño de la estructura del proyecto, generación del código base, de los casos de prueba y de la plantilla de documentación |
| Principales consultas realizadas | *(completar)* |
| Resultados aceptados / modificados / descartados | *(completar)* |
| Validaciones efectuadas por el equipo | *(completar: por ejemplo, ejecución de las pruebas, lectura y explicación del código, cambios propios)* |

"""
Módulo del Analizador Semántico para un Subconjunto de Go (Avance 3)
==================================================================
Implementa el recorrido del Árbol de Sintaxis Abstracta (AST) generado por
`src/parser.py`, construye la Tabla de Símbolos jerárquica por ámbitos y
verifica las seis reglas semánticas del subconjunto de Go definido para el
proyecto.

El analizador está estructurado de forma modular y colaborativa entre los
tres integrantes del equipo, siguiendo el contrato de aportes y trazabilidad
establecido en `docs/Plan_Avance_3_Semantico.md`:
- Pablo Naranjo (@PabloNaranjoM):
    * Sección 0: Modelo `Simbolo`, `TablaSimbolos` jerárquica con pila de
      ambientes y formateador `registrar_error_semantico()` /
      `registrar_validacion_semantica()`.
    * Sección 3: Regla Semántica 1 (`RS-2`: Unicidad en el alcance) y Regla
      Semántica 2 (`RS-5`: Validación de tipo y existencia de retorno en
      funciones y llamadas), además del despachador general y la fachada
      `analizar_semantica(codigo, res_sintactico=None)`.
- Hivor Araujo (@AraujoHivor):
    * Sección 1: Regla Semántica 1 (`RS-1`: Declaración previa obligatoria de
      identificadores, indexación y acceso a campos de struct) y Regla
      Semántica 2 (`RS-3`: Compatibilidad estricta en asignaciones, inferencia
      de tipos, inmutabilidad de `const`, lectura por consola y literales
      compuestos).
- Josué Pacheco (@JosuePach3co):
    * Sección 2: Evaluador recursivo de expresiones `evaluar_expresion()`,
      Regla Semántica 1 (`RS-4`: Coherencia en operaciones aritméticas,
      relacionales, lógicas, unarias e incremento/decremento) y Regla Semántica 2
      (`RS-6`: Validez lógica de estructuras de control e interrupciones
      `break`, `continue` y `fallthrough`, condiciones booleanas e iteración
      `for range`).

Autores:
    - Pablo Naranjo (@PabloNaranjoM)
    - Hivor Araujo (@AraujoHivor)
    - Josué Pacheco (@JosuePach3co)
"""

from __future__ import annotations

# =====================================================================
# SECCIÓN 0: IMPORTS, MODELO DE SÍMBOLOS Y TABLA DE SÍMBOLOS JERÁRQUICA
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
from dataclasses import dataclass, field
from typing import Any

TIPOS_NUMERICOS: tuple[str, ...] = ("int", "float64")
TIPOS_PRIMITIVOS: tuple[str, ...] = ("int", "float64", "string", "bool")

# TODO (Paso 1.1 - Estructura Base): Definir la clase/dataclass `Simbolo` para
#       representar cada entrada de la Tabla de Símbolos con los atributos:
#       - nombre: str
#       - categoria: str ("variable", "constante", "funcion", "parametro", "tipo_struct")
#       - tipo_dato: str ("int", "float64", "string", "bool", "void", "[N]T", "[]T", "map[K]V", "<Struct>")
#       - ambito: str (ej. "global", "func:main", "bloque_if_14", "bloque_for_22")
#       - linea: int
#       - mutable: bool = True (False para constantes `const`)
#       - parametros: list[tuple[str, str]] = field(default_factory=list)
#       - tipo_retorno: str = "void"
#       - campos_struct: dict[str, str] = field(default_factory=dict)
#       - valor_inicial: Any = None
#       - Método `to_dict() -> dict[str, Any]` para serialización hacia GUI y logs.

# TODO (Paso 1.1 - Estructura Base): Definir la clase `TablaSimbolos` con soporte
#       de pila de ámbitos (`pila_ambitos`, `nombres_ambitos`, `historial_simbolos`)
#       y los métodos:
#       - entrar_ambito(nombre_ambito: str) -> None
#       - salir_ambito() -> str | None
#       - ambito_actual() -> str
#       - declarar(simbolo: Simbolo) -> tuple[bool, Simbolo | None]
#       - buscar_en_ambito_actual(nombre: str) -> Simbolo | None
#       - buscar_visible(nombre: str) -> Simbolo | None
#       - exportar_lista_diccionarios() -> list[dict[str, Any]]

# TODO (Paso 1.1 - Reporte Oficial de Diagnósticos): Definir la función
#       `registrar_error_semantico(categoria, linea, descripcion)`
#       respetando el formato estandarizado de la instrucción:
#       "Error Semántico <Categoría> en la línea <N>: <Mensaje descriptivo>."
#       y conservando metadatos (`categoria`, `linea`, `descripcion`, `mensaje`)
#       para la consola de diagnóstico de la GUI y el exportador de logs.

# TODO (Paso 1.1 - Auditoría Semántica): Definir la función
#       `registrar_validacion_semantica(linea, regla, detalle)` para registrar
#       en el contexto del análisis cada comprobación semántica exitosa.
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 1: RESOLUCIÓN DE IDENTIFICADORES, DECLARACIONES Y COMPATIBILIDAD DE ASIGNACIONES
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
# TODO (RS-1 | Categoría: "identificadores" - Declaración previa obligatoria):
#       Implementar `resolver_tipo_referencia(nodo_ref, tabla_simbolos, contexto) -> str`
#       para resolver referencias en expresiones y receptores de asignación:
#       - Identificadores simples ("id", nombre, linea) o str: validar con
#         `tabla_simbolos.buscar_visible(nombre)` que exista declaración previa;
#         caso contrario emitir Error Semántico de categoría "identificadores".
#       - Indexaciones ("indice", base, indice, linea): verificar que la base sea
#         arreglo `[N]T`, slice `[]T` o mapa `map[K]V`; validar que el índice
#         sea `int` (en arreglos/slices) o compatible con la clave `K` (en mapas),
#         y retornar el tipo del elemento o valor.
#       - Acceso a campos ("campo", base, campo, linea): verificar que `base`
#         resuelva a un tipo `struct` registrado en la tabla de símbolos y que
#         `campo` pertenezca a su diccionario `campos_struct`.

# TODO (RS-3 | Categoría: "asignación de tipo" - Compatibilidad estricta en asignaciones):
#       Implementar los visitadores de declaraciones simples y cortas:
#       - `visitar_declaracion_var(nodo, tabla_simbolos, contexto)`: validar que el
#         tipo explícito coincida estrictamente con la expresión inicial (sin
#         coerción implícita `int` <-> `float64`) y prohibir tipo `void`.
#       - `visitar_declaracion_const(nodo, tabla_simbolos, contexto)`: validar
#         constantes con `mutable=False` y comprobar compatibilidad si lleva tipo.
#       - `visitar_declaracion_var_inferencia(nodo, tabla_simbolos, contexto)`:
#         inferir el tipo desde la expresión evaluada en `var x = expr`, evitando
#         registrar variables con tipo `void` o `error_tipo`.
#       - `visitar_declaracion_corta(nodo, tabla_simbolos, contexto)`: inferir el
#         tipo en `x := expr` validando unicidad en el alcance (RS-2) y compatibilidad.

# TODO (RS-3 | Declaraciones compuestas e instanciación de struct):
#       Implementar `visitar_declaraciones_compuestas(nodo, tabla_simbolos, contexto)`
#       para manejar las tuplas AST reales (`"arreglo"`, `"slice"`, `"mapa"`),
#       verificando homogeneidad de elementos/claves/valores, y manejar
#       `"struct_init"` evitando falsos positivos de RS-1 sobre sus claves
#       nominales al validarlas directamente contra `campos_struct` del `struct`.

# TODO (RS-3 | Asignaciones, inmutabilidad y lectura por consola):
#       Implementar:
#       - `visitar_asignacion(nodo, tabla_simbolos, contexto)`: verificar existencia
#         previa del receptor (RS-1), impedir reasignación sobre símbolos con
#         `mutable == False` (`const`) y validar igualdad estricta de tipos.
#       - `visitar_asignacion_compuesta(nodo, tabla_simbolos, contexto)`: validar
#         `+=`, `-=`, `*=`, `/=`, `%=` según mutabilidad y tipos permitidos.
#       - `visitar_sentencia_lectura(nodo, tabla_simbolos, contexto)`: validar
#         en nodos `scanln` (`fmt.Scan` / `fmt.Scanln`) que cada referencia
#         esté declarada previamente (RS-1) y sea mutable (no `const`, RS-3).
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================


# =====================================================================
# SECCIÓN 2: EVALUACIÓN DE EXPRESIONES, OPERACIONES PERMITIDAS Y ESTRUCTURAS DE CONTROL
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
# TODO (Evaluador Recursivo de Expresiones):
#       Implementar `evaluar_expresion(nodo, tabla_simbolos, contexto) -> str`
#       para deducir el tipo resultante de cualquier nodo de expresión del AST:
#       - Literales etiquetados ("literal", tipo_go, valor, linea): "int",
#         "float64", "string", "bool".
#       - Referencias ("id", ...), ("campo", ...), ("indice", ...): delegar a
#         `resolver_tipo_referencia()`.
#       - Llamadas ("llamada_funcion", ...), literales compuestos, operaciones
#         binarias y unarias. Propagar `"error_tipo"` cuando un subárbol ya
#         reportó error para evitar falsos positivos en cascada.

# TODO (RS-4 | Categoría: "operaciones permitidas" - Coherencia de tipos en operaciones):
#       Implementar `validar_operacion_binaria(operador, tipo_izq, tipo_der, linea, contexto) -> str`
#       y `validar_operacion_unaria(operador, operando, linea, tabla_simbolos, contexto) -> str`:
#       - `+`: permitido entre `int + int`, `float64 + float64` o `string + string`.
#       - `-`, `*`, `/`: permitidos únicamente entre tipos numéricos iguales
#         (`int` con `int` o `float64` con `float64`), sin promoción implícita.
#       - `%`: exclusivo para `int` con `int`.
#       - Relacionales (`<`, `>`, `<=`, `>=`): ambos operandos del mismo tipo
#         comparable (`int`, `float64` o `string`) -> retorna `"bool"`.
#       - Igualdad (`==`, `!=`): operandos de tipos iguales compatibles -> `"bool"`.
#       - Lógicos (`&&`, `||`) y unario `!`: exclusivos de `"bool"` -> `"bool"`.
#       - Unario `-`: exclusivo de tipos numéricos (`int`, `float64`).
#       - Unario `&`: si aparece como nodo `("unario", "&", ref, ...)`, validar
#         existencia de `ref` (RS-1) sin introducir tipos puntero `*T`.
#       - Incremento/decremento (`++`, `--` en nodo `incremento`): exigir variable
#         declarada, mutable (`mutable=True`) y de tipo numérico (`int` o `float64`).

# TODO (RS-6 | Categoría: "estructuras de control" - Validez lógica de flujos e interrupciones):
#       Implementar los visitadores de bloques y estructuras de control gestionando
#       la pila de ámbitos y los contadores `profundidad_for` / `profundidad_switch`:
#       - `visitar_bloque(lista_sentencias, tabla_simbolos, contexto)`: recibir
#         la `list` de sentencias que entrega `p_bloque`, abrir un ámbito léxico
#         propio, recorrer cada sentencia y cerrar el ámbito en un bloque `try/finally`.
#       - `visitar_sentencia_if(nodo, tabla_simbolos, contexto)`: validar que la
#         condición sea estrictamente `"bool"` y recorrer ramas `then` y `else`.
#       - `visitar_sentencia_for(nodo, tabla_simbolos, contexto)` y el helper
#         `obtener_tipos_iteracion_range(tipo_coleccion)`: manejar variantes
#         `for` infinito, `for_cond`, `for_clasico` (condición `"bool"`) y
#         `for_range` (`[N]T`/`[]T` -> `(int, T)` y `map[K]V` -> `(K, V)`),
#         actualizando `profundidad_for`.
#       - `visitar_sentencia_switch(nodo, tabla_simbolos, contexto)`: actualizar
#         `profundidad_switch`, validar que cada expresión de `case` sea compatible
#         con la expresión selector (o `"bool"` en switch sin expresión).
#       - `visitar_interrupcion_control(nodo, tabla_simbolos, contexto)`: validar
#         `break` (`profundidad_for > 0` o `profundidad_switch > 0`), `continue`
#         (`profundidad_for > 0`) y `fallthrough` (`profundidad_switch > 0`).
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================


# =====================================================================
# SECCIÓN 3: UNICIDAD EN EL ALCANCE, RETORNO DE FUNCIONES Y FACHADA DEL ANALIZADOR
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
# TODO (RS-2 | Categoría: "identificadores" - Unicidad en el alcance):
#       Implementar `verificar_unicidad_alcance(nombre, linea, tabla_simbolos, contexto) -> bool`
#       consultando `tabla_simbolos.buscar_en_ambito_actual(nombre)`:
#       - Impedir la redeclaración de variables, constantes, parámetros, `struct`
#         o funciones en el mismo ámbito actual (manteniendo shadowing válido en
#         bloques internos anidados).

# TODO (RS-5 | Categoría: "retorno de funciones" - Tipos de retorno, firmas y llamadas):
#       Implementar el registro y validación de estructuras, funciones y llamadas:
#       - `visitar_definicion_struct(nodo, tabla_simbolos, contexto)`: registrar
#         `tipo_struct` en la tabla de símbolos y verificar unicidad de campos.
#       - `visitar_declaracion_funcion(nodo, tabla_simbolos, contexto)`: registrar
#         la firma en el ámbito global, abrir ámbito `func:<nombre>`, declarar
#         parámetros formales (registrando parámetros variádicos `...T` como
#         slice `[]T` dentro del cuerpo), fijar `funcion_actual` en el contexto
#         y verificar que toda función con retorno distinto de `"void"` posea al
#         menos una sentencia `return` válida.
#       - `visitar_literal_funcion(nodo, tabla_simbolos, contexto) -> str`: al
#         ser una función anónima, abrir ámbito temporal `func:anonima_<linea>`,
#         validar parámetros y `return` (RS-5) y retornar su tipo firma (ej. `"func(int)->int"`).
#       - `visitar_sentencia_retorno(nodo, tabla_simbolos, contexto)`: validar que
#         `return` vacío corresponda a funciones `"void"` y `return expr` coincida
#         estrictamente con el `tipo_retorno` declarado en la función actual.
#       - `validar_llamada_funcion(nodo, tabla_simbolos, contexto) -> str`: validar
#         llamadas a funciones declaradas por el usuario (y evaluar argumentos de
#         los nodos `println` / `print` de `fmt`), verificando existencia previa
#         (RS-1), cantidad y compatibilidad de tipos de argumentos (incluyendo
#         soporte para parámetros variádicos `...T`).

# TODO (Despachador del AST y Fachada Principal):
#       - Implementar `visitar_nodo(nodo, tabla_simbolos, contexto)` para enrutar
#         cada nodo del AST hacia su visitador correspondiente en las Secciones 1,
#         2 y 3.
#       - Implementar `analizar_semantica(codigo: str, res_sintactico: dict[str, Any] | None = None) -> dict[str, Any]`
#         como punto de entrada público del analizador semántico, reutilizando
#         `res_sintactico` cuando sea provisto para evitar doble parseo e invocando
#         al parser solo si `res_sintactico is None`. Retornar un diccionario
#         compatible con `log_exporter.py` y la GUI con las claves:
#         `tokens`, `errores_lexicos`, `arbol`, `reglas_sintacticas`,
#         `errores_sintacticos`, `simbolos`, `reglas_semanticas`, `errores` y `valido`.
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

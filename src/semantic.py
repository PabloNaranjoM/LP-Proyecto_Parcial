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

errores_semanticos: list[dict[str, Any]] = []
reglas_semanticas_validadas: list[dict[str, Any]] = []


@dataclass
class Simbolo:
    """Representa una entrada declarada en la Tabla de Símbolos."""

    nombre: str
    categoria: str
    tipo_dato: str
    ambito: str
    linea: int
    mutable: bool = True
    inicializado: bool = True
    parametros: list[tuple[str, str]] = field(default_factory=list)
    tipo_retorno: str = "void"
    campos_struct: dict[str, str] = field(default_factory=dict)
    valor_inicial: Any = None

    def to_dict(self) -> dict[str, Any]:
        """Serializa el símbolo a diccionario para GUI y exportador de logs."""
        return {
            "nombre": self.nombre,
            "categoria": self.categoria,
            "tipo_dato": self.tipo_dato,
            "ambito": self.ambito,
            "linea": self.linea,
            "mutable": self.mutable,
            "inicializado": self.inicializado,
            "parametros": list(self.parametros),
            "tipo_retorno": self.tipo_retorno,
            "campos_struct": dict(self.campos_struct),
            "valor_inicial": self.valor_inicial,
        }


class TablaSimbolos:
    """Tabla de Símbolos jerárquica con pila de ámbitos y registro histórico."""

    def __init__(self) -> None:
        self.pila_ambitos: list[dict[str, Simbolo]] = [{}]
        self.nombres_ambitos: list[str] = ["global"]
        self.historial_simbolos: list[Simbolo] = []

    def entrar_ambito(self, nombre_ambito: str) -> None:
        """Abre un nuevo ámbito léxico hijo en el tope de la pila."""
        self.pila_ambitos.append({})
        self.nombres_ambitos.append(nombre_ambito)

    def salir_ambito(self) -> str | None:
        """Cierra el ámbito actual sin eliminar el ámbito global."""
        if len(self.pila_ambitos) <= 1:
            return None
        self.pila_ambitos.pop()
        return self.nombres_ambitos.pop()

    def ambito_actual(self) -> str:
        """Retorna el nombre del ámbito activo en el tope de la pila."""
        return self.nombres_ambitos[-1]

    def declarar(self, simbolo: Simbolo) -> tuple[bool, Simbolo | None]:
        """Registra un símbolo en el ámbito actual si no existe duplicado previo."""
        existente = self.buscar_en_ambito_actual(simbolo.nombre)
        if existente is not None:
            return False, existente
        if not simbolo.ambito:
            simbolo.ambito = self.ambito_actual()
        self.pila_ambitos[-1][simbolo.nombre] = simbolo
        self.historial_simbolos.append(simbolo)
        return True, None

    def buscar_en_ambito_actual(self, nombre: str) -> Simbolo | None:
        """Busca un identificador únicamente en el ámbito activo."""
        return self.pila_ambitos[-1].get(nombre)

    def buscar_visible(self, nombre: str) -> Simbolo | None:
        """Busca un identificador desde el ámbito más interno hacia el global."""
        for ambito in reversed(self.pila_ambitos):
            if nombre in ambito:
                return ambito[nombre]
        return None

    def exportar_lista_diccionarios(self) -> list[dict[str, Any]]:
        """Retorna el historial completo de símbolos en formato diccionario."""
        return [simbolo.to_dict() for simbolo in self.historial_simbolos]


def crear_contexto_semantico(*, usar_globales: bool = False) -> dict[str, Any]:
    """Inicializa el estado compartido de recorrido para el analizador semántico."""
    if usar_globales:
        errores_semanticos.clear()
        reglas_semanticas_validadas.clear()
        errores = errores_semanticos
        reglas = reglas_semanticas_validadas
    else:
        errores = []
        reglas = []

    return {
        "errores": errores,
        "reglas_semanticas": reglas,
        "funcion_actual": None,
        "tiene_retorno": False,
        "profundidad_for": 0,
        "profundidad_switch": 0,
    }


def registrar_error_semantico(
    categoria: str,
    linea: int,
    descripcion: str,
    contexto: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Registra un error semántico siguiendo el formato estándar del proyecto."""
    desc = descripcion.strip()
    if desc and not desc.endswith("."):
        desc = f"{desc}."
    entrada = {
        "linea": linea,
        "categoria": categoria,
        "descripcion": desc,
        "mensaje": f"Error Semántico {categoria} en la línea {linea}: {desc}",
    }
    destino = contexto["errores"] if contexto is not None else errores_semanticos
    destino.append(entrada)
    return entrada


def registrar_validacion_semantica(
    linea: int,
    regla: str,
    detalle: str,
    contexto: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Registra una comprobación semántica válida para la GUI y los logs."""
    descripcion = detalle.strip() if detalle else f"Regla '{regla}' validada."
    entrada = {
        "linea": linea,
        "regla": regla,
        "descripcion": descripcion,
        "mensaje": f"[Semántico - Línea {linea}] {regla}: {descripcion}",
    }
    destino = (
        contexto["reglas_semanticas"]
        if contexto is not None
        else reglas_semanticas_validadas
    )
    destino.append(entrada)
    return entrada
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

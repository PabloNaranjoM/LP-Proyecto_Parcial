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


def _nombre_base_referencia(referencia: Any) -> str | None:
    """Extrae el identificador raíz desde referencias simples, de campo o de índice."""
    base = referencia
    while isinstance(base, tuple) and base[0] in ("campo", "indice"):
        base = base[1]
    if isinstance(base, tuple) and base[0] == "id":
        return str(base[1])
    return base if isinstance(base, str) else None
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 1: RESOLUCIÓN DE IDENTIFICADORES, DECLARACIONES Y COMPATIBILIDAD DE ASIGNACIONES
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

def resolver_tipo_referencia(nodo_ref, tabla_simbolos, contexto):
    """RS-1: Comprueba que un identificador este declarado."""

    # RS-1: Acceso a campos de una estructura
    if isinstance(nodo_ref, tuple) and nodo_ref[0] == "campo":
        base = nodo_ref[1]
        campo = nodo_ref[2]
        linea = nodo_ref[3]

        # Obtener el tipo de la variable
        tipo_base = resolver_tipo_referencia(
            base, tabla_simbolos, contexto
        )

        if tipo_base == "error_tipo":
            return "error_tipo"

        # Buscar la definicion de la estructura
        simbolo_struct = tabla_simbolos.buscar_visible(tipo_base)

        if simbolo_struct is None or simbolo_struct.categoria != "tipo_struct":
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El tipo '{tipo_base}' no es una estructura declarada",
                contexto
            )
            return "error_tipo"

        # Comprobar si el campo existe
        if campo not in simbolo_struct.campos_struct:
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El campo '{campo}' no existe en la estructura '{tipo_base}'",
                contexto
            )
            return "error_tipo"

        registrar_validacion_semantica(
            linea,
            "RS-1",
            f"El campo '{campo}' existe en la estructura '{tipo_base}'",
            contexto
        )

        return simbolo_struct.campos_struct[campo]

    # RS-1: Acceso por indice a arreglos, slices o mapas
    if isinstance(nodo_ref, tuple) and nodo_ref[0] == "indice":
        base = nodo_ref[1]
        indice = nodo_ref[2]
        linea = nodo_ref[3]

        # Obtener el tipo de la coleccion
        tipo_base = resolver_tipo_referencia(
            base, tabla_simbolos, contexto
        )

        # Obtener el tipo del indice
        tipo_indice = evaluar_expresion(
            indice, tabla_simbolos, contexto
        )

        if tipo_base == "error_tipo" or tipo_indice == "error_tipo":
            return "error_tipo"

        # Funcion ya implementada por Josue
        tipos = obtener_tipos_iteracion_range(tipo_base)

        if tipos is None:
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El tipo '{tipo_base}' no permite acceso por indice",
                contexto
            )
            return "error_tipo"

        tipo_clave, tipo_elemento = tipos

        if tipo_indice != tipo_clave:
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El indice debe ser '{tipo_clave}', pero se recibio '{tipo_indice}'",
                contexto
            )
            return "error_tipo"

        registrar_validacion_semantica(
            linea,
            "RS-1",
            f"Acceso por indice valido sobre '{tipo_base}'",
            contexto
        )

        return tipo_elemento

    if isinstance(nodo_ref, tuple) and nodo_ref[0] == "id":
        nombre = nodo_ref[1]
        linea = nodo_ref[2]

    elif isinstance(nodo_ref, str):
        nombre = nodo_ref
        linea = 1

    else:

        return "error_tipo"

    simbolo = tabla_simbolos.buscar_visible(nombre)

    if simbolo is None:
        registrar_error_semantico(
            "identificadores",
            linea,
            f"El identificador '{nombre}' no ha sido declarado",
            contexto
        )
        return "error_tipo"

    registrar_validacion_semantica(
        linea,
        "RS-1",
        f"El identificador '{nombre}' fue declarado previamente",
        contexto
    )

    return simbolo.tipo_dato


def visitar_declaracion_var(nodo, tabla_simbolos, contexto):
    """RS-3: Comprueba el tipo de una variable declarada."""

    nombre = nodo[1]
    tipo_declarado = nodo[2]
    expresion = nodo[3]
    linea = nodo[4]

    # No se permiten variables de tipo void
    if tipo_declarado == "void":
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"La variable '{nombre}' no puede ser de tipo void",
            contexto
        )
        return

    # Si tiene un valor inicial, comprobar su tipo
    if expresion is not None:
        tipo_valor = evaluar_expresion(
            expresion, tabla_simbolos, contexto
        )

        # Evitar registrar otro error si la expresion ya fallo
        if tipo_valor == "error_tipo":
            return

        if tipo_declarado != tipo_valor:
            registrar_error_semantico(
                "asignación de tipo",
                linea,
                f"La variable '{nombre}' es de tipo '{tipo_declarado}', pero recibe '{tipo_valor}'",
                contexto
            )
            return

    # Registrar la variable en la tabla de simbolos
    simbolo = Simbolo(
        nombre=nombre,
        categoria="variable",
        tipo_dato=tipo_declarado,
        ambito=tabla_simbolos.ambito_actual(),
        linea=linea
    )

    registrado, existente = tabla_simbolos.declarar(simbolo)

    if not registrado:
        registrar_error_semantico(
            "identificadores",
            linea,
            f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
            contexto
        )
        return

    registrar_validacion_semantica(
        linea,
        "RS-3",
        f"Variable '{nombre}' declarada correctamente como '{tipo_declarado}'",
        contexto
    )


def visitar_declaracion_const(nodo, tabla_simbolos, contexto):
    """RS-3: Valida el tipo y registra una constante."""

    nombre = nodo[1]
    tipo_declarado = nodo[2]
    expresion = nodo[3]
    linea = nodo[4]

    # Obtener el tipo del valor de la constante
    tipo_valor = evaluar_expresion(
        expresion, tabla_simbolos, contexto
    )

    # No registrar constantes con expresiones incorrectas
    if tipo_valor == "error_tipo":
        return

    if tipo_valor == "void":
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"La constante '{nombre}' no puede tener tipo void",
            contexto
        )
        return

    # Comprobar el tipo cuando fue declarado explicitamente
    if tipo_declarado is not None and tipo_declarado != tipo_valor:
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"La constante '{nombre}' es de tipo '{tipo_declarado}', pero recibe '{tipo_valor}'",
            contexto
        )
        return

    # Si no se especifico el tipo, inferirlo
    tipo_final = tipo_declarado if tipo_declarado is not None else tipo_valor

    simbolo = Simbolo(
        nombre=nombre,
        categoria="constante",
        tipo_dato=tipo_final,
        ambito=tabla_simbolos.ambito_actual(),
        linea=linea,
        mutable=False
    )

    registrado, existente = tabla_simbolos.declarar(simbolo)

    if not registrado:
        registrar_error_semantico(
            "identificadores",
            linea,
            f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
            contexto
        )
        return

    registrar_validacion_semantica(
        linea,
        "RS-3",
        f"Constante '{nombre}' declarada correctamente como '{tipo_final}'",
        contexto
    )


def visitar_declaracion_var_inferencia(nodo, tabla_simbolos, contexto):
    """RS-3: Infiere el tipo de una variable a partir de su valor."""

    nombre = nodo[1]
    expresion = nodo[2]
    linea = nodo[3]

    # Obtener el tipo del valor asignado
    tipo_inferido = evaluar_expresion(
        expresion, tabla_simbolos, contexto
    )

    # Si la expresion tiene errores, no registrar la variable
    if tipo_inferido == "error_tipo":
        return

    # No se puede inferir una variable de tipo void
    if tipo_inferido == "void":
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"No se puede inferir el tipo de '{nombre}' desde una expresion sin valor",
            contexto
        )
        return

    # Crear la variable con el tipo obtenido
    simbolo = Simbolo(
        nombre=nombre,
        categoria="variable",
        tipo_dato=tipo_inferido,
        ambito=tabla_simbolos.ambito_actual(),
        linea=linea,
        mutable=True
    )

    registrado, existente = tabla_simbolos.declarar(simbolo)

    if not registrado:
        registrar_error_semantico(
            "identificadores",
            linea,
            f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
            contexto
        )
        return

    registrar_validacion_semantica(
        linea,
        "RS-3",
        f"Variable '{nombre}' declarada con tipo inferido '{tipo_inferido}'",
        contexto
    )


def visitar_declaracion_corta(nodo, tabla_simbolos, contexto):
    """RS-3: Valida una declaracion corta con :=."""

    nombre = nodo[1]
    expresion = nodo[2]
    linea = nodo[3]

    # En un programa completo (con 'package'), ':=' solo se permite dentro de funciones
    if tabla_simbolos.ambito_actual() == "global" and contexto.get("es_programa_completo"):
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"La declaración corta ':=' para '{nombre}' solo se permite dentro de una función; utilice 'var' en el ámbito global",
            contexto
        )
        return

    # Comprobar si ya existe en el mismo ambito
    existente = tabla_simbolos.buscar_en_ambito_actual(nombre)
    if existente is not None:
        registrar_error_semantico(
            "identificadores",
            linea,
            f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
            contexto
        )
        return

    # Inferir el tipo de la expresion
    tipo_inferido = evaluar_expresion(
        expresion, tabla_simbolos, contexto
    )

    if tipo_inferido == "error_tipo":
        return

    if tipo_inferido == "void":
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"No se puede declarar '{nombre}' con una expresion sin valor",
            contexto
        )
        return

    # Registrar la nueva variable
    simbolo = Simbolo(
        nombre=nombre,
        categoria="variable",
        tipo_dato=tipo_inferido,
        ambito=tabla_simbolos.ambito_actual(),
        linea=linea,
        mutable=True
    )

    registrado, existente = tabla_simbolos.declarar(simbolo)

    if not registrado:
        registrar_error_semantico(
            "identificadores",
            linea,
            f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
            contexto
        )
        return

    registrar_validacion_semantica(
        linea,
        "RS-3",
        f"Declaracion corta de '{nombre}' con tipo '{tipo_inferido}'",
        contexto
    )


def visitar_asignacion(nodo, tabla_simbolos, contexto):
    """RS-3: Valida asignaciones y evita modificar constantes."""

    referencia = nodo[1]
    expresion = nodo[2]
    linea = nodo[3]

    # Verificar que el destino exista y obtener su tipo
    tipo_destino = resolver_tipo_referencia(
        referencia, tabla_simbolos, contexto
    )

    if tipo_destino == "error_tipo":
        return

    # Obtener el identificador base de la referencia
    nombre = _nombre_base_referencia(referencia)
    if nombre is None:
        return

    simbolo = tabla_simbolos.buscar_visible(nombre)

    # Comprobar que no sea una constante
    if simbolo is not None and not simbolo.mutable:
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"No se puede modificar la constante '{nombre}'",
            contexto
        )
        return

    # Obtener el tipo del nuevo valor
    tipo_valor = evaluar_expresion(
        expresion, tabla_simbolos, contexto
    )

    if tipo_valor == "error_tipo":
        return

    # Comparar los tipos sin conversiones implicitas
    if tipo_destino != tipo_valor:
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"No se puede asignar '{tipo_valor}' a '{nombre}' de tipo '{tipo_destino}'",
            contexto
        )
        return

    registrar_validacion_semantica(
        linea,
        "RS-3",
        f"Asignacion valida a '{nombre}' de tipo '{tipo_destino}'",
        contexto
    )


def visitar_asignacion_compuesta(nodo, tabla_simbolos, contexto):
    """RS-3: Valida asignaciones como +=, -=, *=, /= y %=."""

    operador = nodo[1]
    referencia = nodo[2]
    expresion = nodo[3]
    linea = nodo[4]

    # RS-1: Comprobar que el destino exista
    tipo_destino = resolver_tipo_referencia(
        referencia, tabla_simbolos, contexto
    )

    if tipo_destino == "error_tipo":
        return

    # Obtener el nombre de la variable base
    nombre = _nombre_base_referencia(referencia)
    if nombre is None:
        return

    simbolo = tabla_simbolos.buscar_visible(nombre)

    # No se pueden modificar constantes
    if simbolo is not None and not simbolo.mutable:
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"No se puede modificar la constante '{nombre}'",
            contexto
        )
        return

    # Obtener el tipo del valor a asignar
    tipo_valor = evaluar_expresion(
        expresion, tabla_simbolos, contexto
    )

    if tipo_valor == "error_tipo":
        return

    # Convertir += en +, -= en -, etc.
    operadores = {
        "+=": "+",
        "-=": "-",
        "*=": "*",
        "/=": "/",
        "%=": "%"
    }

    if operador not in operadores:
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"Operador de asignacion no reconocido: '{operador}'",
            contexto
        )
        return

    # Utilizar la validacion de operadores de Josue (RS-4)
    tipo_resultado = validar_operacion_binaria(
        operadores[operador],
        tipo_destino,
        tipo_valor,
        linea,
        contexto
    )

    if tipo_resultado == "error_tipo":
        return

    # El resultado debe coincidir con el tipo del destino
    if tipo_resultado != tipo_destino:
        registrar_error_semantico(
            "asignación de tipo",
            linea,
            f"El resultado '{tipo_resultado}' no coincide con '{tipo_destino}'",
            contexto
        )
        return

    registrar_validacion_semantica(
        linea,
        "RS-3",
        f"Asignacion '{operador}' valida sobre '{nombre}'",
        contexto
    )


def visitar_sentencia_lectura(nodo, tabla_simbolos, contexto):
    """RS-1 y RS-3: Valida las variables usadas en fmt.Scan y fmt.Scanln."""

    referencias = nodo[1]
    linea = nodo[2]

    for referencia in referencias:

        # Comprobar que exista la referencia
        tipo = resolver_tipo_referencia(
            referencia, tabla_simbolos, contexto
        )

        if tipo == "error_tipo":
            continue

        # Obtener el identificador principal
        nombre = _nombre_base_referencia(referencia)
        if nombre is None:
            continue

        simbolo = tabla_simbolos.buscar_visible(nombre)

        # No se permite ingresar datos en constantes
        if simbolo is not None and not simbolo.mutable:
            registrar_error_semantico(
                "asignación de tipo",
                linea,
                f"No se puede modificar la constante '{nombre}' mediante lectura",
                contexto
            )
            continue

        registrar_validacion_semantica(
            linea,
            "RS-3",
            f"Lectura valida sobre '{nombre}' de tipo '{tipo}'",
            contexto
        )


def visitar_declaraciones_compuestas(nodo, tabla_simbolos, contexto):
    """RS-3: Valida arreglos, slices, mapas y estructuras."""

    etiqueta = nodo[0]

    # Primera parte: declaraciones de arreglos
    if etiqueta == "arreglo":
        nombre = nodo[1]
        nodo_tamano = nodo[2]
        tipo_elemento = nodo[3]
        elementos = nodo[4]
        linea = nodo[5]

        # Por ahora trabajamos con tamaños enteros literales
        if (
            not isinstance(nodo_tamano, tuple)
            or nodo_tamano[0] != "literal"
            or nodo_tamano[1] != "int"
            or type(nodo_tamano[2]) is not int
            or nodo_tamano[2] < 0
        ):
            registrar_error_semantico(
                "asignación de tipo",
                linea,
                f"El arreglo '{nombre}' debe tener un tamaño entero constante",
                contexto
            )
            return "error_tipo"

        tamano = nodo_tamano[2]

        # Revisar los valores iniciales, si existen
        if elementos is not None:


            if len(elementos) > tamano:
                registrar_error_semantico(
                    "asignación de tipo",
                    linea,
                    f"El arreglo '{nombre}' admite maximo {tamano} elementos, pero recibe {len(elementos)}",
                    contexto
                )
                return "error_tipo"


            for elemento in elementos:
                tipo_valor = evaluar_expresion(
                    elemento, tabla_simbolos, contexto
                )

                if tipo_valor == "error_tipo":
                    return "error_tipo"

                if tipo_valor != tipo_elemento:
                    registrar_error_semantico(
                        "asignación de tipo",
                        linea,
                        f"El arreglo '{nombre}' espera '{tipo_elemento}', pero recibe '{tipo_valor}'",
                        contexto
                    )
                    return "error_tipo"

        # Crear el tipo del arreglo: [3]int
        tipo_arreglo = f"[{tamano}]{tipo_elemento}"

        simbolo = Simbolo(
            nombre=nombre,
            categoria="arreglo",
            tipo_dato=tipo_arreglo,
            ambito=tabla_simbolos.ambito_actual(),
            linea=linea,
            inicializado=True
        )

        registrado, existente = tabla_simbolos.declarar(simbolo)

        if not registrado:
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
                contexto
            )
            return "error_tipo"

        registrar_validacion_semantica(
            linea,
            "RS-3",
            f"Arreglo '{nombre}' declarado como '{tipo_arreglo}'",
            contexto
        )

        return tipo_arreglo


    # Segunda parte: declaraciones de slices
    if etiqueta == "slice":
        nombre = nodo[1]
        tipo_elemento = nodo[2]
        elementos = nodo[3]
        linea = nodo[4]

        # Comprobar que todos los elementos tengan el mismo tipo
        for elemento in elementos:
            tipo_valor = evaluar_expresion(
                elemento, tabla_simbolos, contexto
            )

            if tipo_valor == "error_tipo":
                return "error_tipo"

            if tipo_valor != tipo_elemento:
                registrar_error_semantico(
                    "asignación de tipo",
                    linea,
                    f"El slice '{nombre}' espera '{tipo_elemento}', pero recibe '{tipo_valor}'",
                    contexto
                )
                return "error_tipo"

        # Construir el tipo del slice
        tipo_slice = f"[]{tipo_elemento}"

        simbolo = Simbolo(
            nombre=nombre,
            categoria="slice",
            tipo_dato=tipo_slice,
            ambito=tabla_simbolos.ambito_actual(),
            linea=linea
        )

        registrado, existente = tabla_simbolos.declarar(simbolo)

        if not registrado:
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
                contexto
            )
            return "error_tipo"

        registrar_validacion_semantica(
            linea,
            "RS-3",
            f"Slice '{nombre}' declarado como '{tipo_slice}'",
            contexto
        )

        return tipo_slice


    # Tercera parte: declaraciones de mapas
    if etiqueta == "mapa":
        nombre = nodo[1]
        tipo_clave = nodo[2]
        tipo_valor = nodo[3]
        elementos = nodo[4]
        linea = nodo[5]

        # Revisar cada pareja de clave y valor
        for clave, valor in elementos:
            tipo_clave_actual = evaluar_expresion(
                clave, tabla_simbolos, contexto
            )

            tipo_valor_actual = evaluar_expresion(
                valor, tabla_simbolos, contexto
            )

            # Evitar errores adicionales si una expresion fallo
            if (
                tipo_clave_actual == "error_tipo"
                or tipo_valor_actual == "error_tipo"
            ):
                return "error_tipo"

            # Comprobar el tipo de la clave
            if tipo_clave_actual != tipo_clave:
                registrar_error_semantico(
                    "asignación de tipo",
                    linea,
                    f"El mapa '{nombre}' espera claves '{tipo_clave}', pero recibe '{tipo_clave_actual}'",
                    contexto
                )
                return "error_tipo"

            # Comprobar el tipo del valor
            if tipo_valor_actual != tipo_valor:
                registrar_error_semantico(
                    "asignación de tipo",
                    linea,
                    f"El mapa '{nombre}' espera valores '{tipo_valor}', pero recibe '{tipo_valor_actual}'",
                    contexto
                )
                return "error_tipo"

        # Construir el tipo completo del mapa
        tipo_mapa = f"map[{tipo_clave}]{tipo_valor}"

        simbolo = Simbolo(
            nombre=nombre,
            categoria="mapa",
            tipo_dato=tipo_mapa,
            ambito=tabla_simbolos.ambito_actual(),
            linea=linea
        )

        registrado, existente = tabla_simbolos.declarar(simbolo)

        if not registrado:
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
                contexto
            )
            return "error_tipo"

        registrar_validacion_semantica(
            linea,
            "RS-3",
            f"Mapa '{nombre}' declarado como '{tipo_mapa}'",
            contexto
        )

        return tipo_mapa


    # Cuarta parte: inicializacion de estructuras
    if etiqueta == "struct_init":
        referencia_tipo = nodo[1]
        campos_iniciales = nodo[2]
        linea = nodo[3]

        # Obtener el nombre de la estructura
        if isinstance(referencia_tipo, tuple) and referencia_tipo[0] == "id":
            nombre_tipo = referencia_tipo[1]
        elif isinstance(referencia_tipo, str):
            nombre_tipo = referencia_tipo
        else:
            registrar_error_semantico(
                "identificadores",
                linea,
                "Referencia de estructura no valida",
                contexto
            )
            return "error_tipo"

        # Buscar la definicion del struct
        simbolo_struct = tabla_simbolos.buscar_visible(nombre_tipo)

        if simbolo_struct is None or simbolo_struct.categoria != "tipo_struct":
            registrar_error_semantico(
                "identificadores",
                linea,
                f"La estructura '{nombre_tipo}' no ha sido declarada",
                contexto
            )
            return "error_tipo"

        campos_usados = set()

        for clave, valor in campos_iniciales:
            # La clave es el nombre de un campo, no una variable
            if isinstance(clave, tuple) and clave[0] == "id":
                nombre_campo = clave[1]
            elif isinstance(clave, str):
                nombre_campo = clave
            else:
                registrar_error_semantico(
                    "identificadores",
                    linea,
                    f"Nombre de campo no valido en '{nombre_tipo}'",
                    contexto
                )
                return "error_tipo"

            # Comprobar que el campo exista
            if nombre_campo not in simbolo_struct.campos_struct:
                registrar_error_semantico(
                    "identificadores",
                    linea,
                    f"El campo '{nombre_campo}' no existe en la estructura '{nombre_tipo}'",
                    contexto
                )
                return "error_tipo"

            # Evitar repetir un mismo campo
            if nombre_campo in campos_usados:
                registrar_error_semantico(
                    "identificadores",
                    linea,
                    f"El campo '{nombre_campo}' esta repetido",
                    contexto
                )
                return "error_tipo"

            campos_usados.add(nombre_campo)

            # Comparar el tipo del valor
            tipo_esperado = simbolo_struct.campos_struct[nombre_campo]
            tipo_actual = evaluar_expresion(
                valor, tabla_simbolos, contexto
            )

            if tipo_actual == "error_tipo":
                return "error_tipo"

            if tipo_actual != tipo_esperado:
                registrar_error_semantico(
                    "asignación de tipo",
                    linea,
                    f"El campo '{nombre_campo}' espera '{tipo_esperado}', pero recibe '{tipo_actual}'",
                    contexto
                )
                return "error_tipo"

        registrar_validacion_semantica(
            linea,
            "RS-3",
            f"Estructura '{nombre_tipo}' inicializada correctamente",
            contexto
        )

        return nombre_tipo

    return "error_tipo"





# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================


# =====================================================================
# SECCIÓN 2: EVALUACIÓN DE EXPRESIONES, OPERACIONES PERMITIDAS Y ESTRUCTURAS DE CONTROL
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

def _extraer_linea(nodo: Any, por_defecto: int = 1) -> int:
    """Obtiene de forma segura la línea adjunta al final de una tupla AST."""
    if isinstance(nodo, tuple) and nodo and isinstance(nodo[-1], int):
        return nodo[-1]
    return por_defecto


def evaluar_expresion(
    nodo: Any,
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> str:
    """Deduce recursivamente el tipo de dato de cualquier expresión del AST."""
    if nodo is None:
        return "void"

    if not isinstance(nodo, tuple):
        if isinstance(nodo, bool):
            return "bool"
        if isinstance(nodo, int):
            return "int"
        if isinstance(nodo, float):
            return "float64"
        if isinstance(nodo, str):
            return "string"
        return "error_tipo"

    etiqueta = nodo[0]
    linea = _extraer_linea(nodo)

    # 1. Literales etiquetados: ("literal", tipo_go, valor, linea)
    if etiqueta == "literal":
        return str(nodo[1])

    # 2. Referencias: ("id", ...), ("campo", ...), ("indice", ...)
    if etiqueta in ("id", "campo", "indice"):
        return resolver_tipo_referencia(nodo, tabla_simbolos, contexto)

    # 3. Llamadas a funciones
    if etiqueta == "llamada_funcion":
        return validar_llamada_funcion(nodo, tabla_simbolos, contexto)

    # 4. Funciones anónimas / literales de función
    if etiqueta == "literal_funcion":
        return visitar_literal_funcion(nodo, tabla_simbolos, contexto)

    # 5. Instanciación de struct: ("struct_init", ref_tipo, campos, linea)
    if etiqueta == "struct_init":
        return visitar_declaraciones_compuestas(nodo, tabla_simbolos, contexto)

    # 6. Operaciones binarias aritméticas, relacionales y lógicas
    mapa_binarios = {
        "suma": "+",
        "resta": "-",
        "multiplicacion": "*",
        "division": "/",
        "modulo": "%",
        "and": "&&",
        "or": "||",
    }
    if etiqueta in mapa_binarios:
        tipo_izq = evaluar_expresion(nodo[1], tabla_simbolos, contexto)
        tipo_der = evaluar_expresion(nodo[2], tabla_simbolos, contexto)
        return validar_operacion_binaria(
            mapa_binarios[etiqueta], tipo_izq, tipo_der, linea, contexto
        )

    if etiqueta == "comparacion":
        operador = str(nodo[1])
        tipo_izq = evaluar_expresion(nodo[2], tabla_simbolos, contexto)
        tipo_der = evaluar_expresion(nodo[3], tabla_simbolos, contexto)
        return validar_operacion_binaria(
            operador, tipo_izq, tipo_der, linea, contexto
        )

    # 7. Operaciones unarias: ("not", expr, linea) o ("unario", op, expr, linea)
    if etiqueta == "not":
        return validar_operacion_unaria("!", nodo[1], linea, tabla_simbolos, contexto)

    if etiqueta == "unario":
        operador = str(nodo[1])
        return validar_operacion_unaria(
            operador, nodo[2], linea, tabla_simbolos, contexto
        )

    return "error_tipo"


def validar_operacion_binaria(
    operador: str,
    tipo_izq: str,
    tipo_der: str,
    linea: int,
    contexto: dict[str, Any],
) -> str:
    """Valida RS-4 (operaciones permitidas) para operadores binarios."""
    if tipo_izq == "error_tipo" or tipo_der == "error_tipo":
        return "error_tipo"

    if tipo_izq == "void" or tipo_der == "void":
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"No se puede aplicar el operador '{operador}' sobre una expresión sin valor ('void').",
            contexto,
        )
        return "error_tipo"

    # Suma (+) / Concatenación
    if operador == "+":
        if tipo_izq == tipo_der and tipo_izq in ("int", "float64", "string"):
            registrar_validacion_semantica(
                linea,
                "RS-4 (Operaciones permitidas)",
                f"Operación '{operador}' válida entre operandos '{tipo_izq}'.",
                contexto,
            )
            return tipo_izq
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"Operación '+' no válida entre tipos incompatibles '{tipo_izq}' y '{tipo_der}'.",
            contexto,
        )
        return "error_tipo"

    # Resta, multiplicación y división (-, *, /)
    if operador in ("-", "*", "/"):
        if tipo_izq == tipo_der and tipo_izq in TIPOS_NUMERICOS:
            registrar_validacion_semantica(
                linea,
                "RS-4 (Operaciones permitidas)",
                f"Operación '{operador}' válida entre operandos '{tipo_izq}'.",
                contexto,
            )
            return tipo_izq
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"Operación '{operador}' requiere operandos numéricos del mismo tipo, se recibió '{tipo_izq}' y '{tipo_der}'.",
            contexto,
        )
        return "error_tipo"

    # Módulo (%) exclusivo de int
    if operador == "%":
        if tipo_izq == "int" and tipo_der == "int":
            registrar_validacion_semantica(
                linea,
                "RS-4 (Operaciones permitidas)",
                "Operación '%' válida entre operandos 'int'.",
                contexto,
            )
            return "int"
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"El operador '%' solo admite operandos de tipo 'int', se recibió '{tipo_izq}' y '{tipo_der}'.",
            contexto,
        )
        return "error_tipo"

    # Relacionales (<, >, <=, >=)
    if operador in ("<", ">", "<=", ">="):
        if tipo_izq == tipo_der and tipo_izq in ("int", "float64", "string"):
            registrar_validacion_semantica(
                linea,
                "RS-4 (Operaciones permitidas)",
                f"Comparación '{operador}' válida entre '{tipo_izq}'.",
                contexto,
            )
            return "bool"
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"No se pueden comparar los tipos '{tipo_izq}' y '{tipo_der}' con '{operador}'.",
            contexto,
        )
        return "error_tipo"

    # Igualdad (==, !=)
    if operador in ("==", "!="):
        if tipo_izq == tipo_der:
            registrar_validacion_semantica(
                linea,
                "RS-4 (Operaciones permitidas)",
                f"Comparación de igualdad '{operador}' válida para tipo '{tipo_izq}'.",
                contexto,
            )
            return "bool"
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"No se puede comparar igualdad '{operador}' entre tipos distintos '{tipo_izq}' y '{tipo_der}'.",
            contexto,
        )
        return "error_tipo"

    # Lógicos (&&, ||)
    if operador in ("&&", "||"):
        if tipo_izq == "bool" and tipo_der == "bool":
            registrar_validacion_semantica(
                linea,
                "RS-4 (Operaciones permitidas)",
                f"Operador lógico '{operador}' válido entre booleanos.",
                contexto,
            )
            return "bool"
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"El operador lógico '{operador}' requiere operandos 'bool', se recibió '{tipo_izq}' y '{tipo_der}'.",
            contexto,
        )
        return "error_tipo"

    registrar_error_semantico(
        "operaciones permitidas",
        linea,
        f"Operador binario no soportado '{operador}'.",
        contexto,
    )
    return "error_tipo"


def validar_operacion_unaria(
    operador: str,
    operando: Any,
    linea: int,
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> str:
    """Valida RS-4 para operadores unarios (!, -, &) e incremento/decremento (++, --)."""
    if operador == "&":
        tipo_ref = resolver_tipo_referencia(operando, tabla_simbolos, contexto)
        if tipo_ref == "error_tipo":
            return "error_tipo"

        nombre_base = _nombre_base_referencia(operando)
        simbolo = tabla_simbolos.buscar_visible(nombre_base) if nombre_base else None
        if simbolo is not None and not simbolo.mutable:
            detalle = (
                f"No se puede obtener la dirección de la constante '{simbolo.nombre}'."
                if simbolo.categoria == "constante"
                else f"No se puede obtener la dirección del identificador no direccionable '{simbolo.nombre}'."
            )
            registrar_error_semantico("asignación de tipo", linea, detalle, contexto)
            return "error_tipo"

        registrar_validacion_semantica(
            linea,
            "RS-4 (Operaciones permitidas)",
            f"Referencia '&' válida sobre '{tipo_ref}'.",
            contexto,
        )
        return f"*{tipo_ref}"

    if operador in ("++", "--"):
        tipo_ref = resolver_tipo_referencia(operando, tabla_simbolos, contexto)
        if tipo_ref == "error_tipo":
            return "error_tipo"

        if isinstance(operando, tuple) and operando[0] == "id":
            simbolo = tabla_simbolos.buscar_visible(operando[1])
            if simbolo is not None and not simbolo.mutable:
                registrar_error_semantico(
                    "asignación de tipo",
                    linea,
                    f"No se puede aplicar '{operador}' sobre la constante '{simbolo.nombre}'.",
                    contexto,
                )
                return "error_tipo"

        if tipo_ref not in TIPOS_NUMERICOS:
            registrar_error_semantico(
                "operaciones permitidas",
                linea,
                f"El operador '{operador}' requiere un operando numérico ('int' o 'float64'), se recibió '{tipo_ref}'.",
                contexto,
            )
            return "error_tipo"

        registrar_validacion_semantica(
            linea,
            "RS-4 (Operaciones permitidas)",
            f"Operador '{operador}' válido sobre tipo '{tipo_ref}'.",
            contexto,
        )
        return tipo_ref

    tipo_op = evaluar_expresion(operando, tabla_simbolos, contexto)
    if tipo_op == "error_tipo":
        return "error_tipo"

    if operador == "!":
        if tipo_op == "bool":
            registrar_validacion_semantica(
                linea,
                "RS-4 (Operaciones permitidas)",
                "Negación lógica '!' válida sobre 'bool'.",
                contexto,
            )
            return "bool"
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"El operador '!' requiere un operando de tipo 'bool', se recibió '{tipo_op}'.",
            contexto,
        )
        return "error_tipo"

    if operador == "-":
        if tipo_op in TIPOS_NUMERICOS:
            registrar_validacion_semantica(
                linea,
                "RS-4 (Operaciones permitidas)",
                f"Negación aritmética '-' válida sobre '{tipo_op}'.",
                contexto,
            )
            return tipo_op
        registrar_error_semantico(
            "operaciones permitidas",
            linea,
            f"El operador unario '-' requiere un tipo numérico, se recibió '{tipo_op}'.",
            contexto,
        )
        return "error_tipo"

    return "error_tipo"


def obtener_tipos_iteracion_range(tipo_coleccion: str) -> tuple[str, str] | None:
    """Retorna (tipo_clave_o_indice, tipo_valor) para colecciones soportadas en for range."""
    if tipo_coleccion.startswith("[]"):
        return ("int", tipo_coleccion[2:])

    if tipo_coleccion.startswith("[") and "]" in tipo_coleccion:
        idx_cierre = tipo_coleccion.index("]")
        return ("int", tipo_coleccion[idx_cierre + 1 :])

    if tipo_coleccion.startswith("map["):
        profundidad = 0
        for i in range(3, len(tipo_coleccion)):
            if tipo_coleccion[i] == "[":
                profundidad += 1
            elif tipo_coleccion[i] == "]":
                profundidad -= 1
                if profundidad == 0:
                    tipo_clave = tipo_coleccion[4:i]
                    tipo_valor = tipo_coleccion[i + 1 :]
                    return (tipo_clave, tipo_valor)

    return None


def visitar_bloque(
    lista_sentencias: list[Any] | None,
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
    nombre_ambito: str = "bloque",
) -> None:
    """Abre un ámbito léxico hijo, recorre las sentencias del bloque y lo cierra."""
    tabla_simbolos.entrar_ambito(nombre_ambito)
    try:
        if lista_sentencias:
            for sentencia in lista_sentencias:
                if sentencia is not None:
                    visitar_nodo(sentencia, tabla_simbolos, contexto)
    finally:
        tabla_simbolos.salir_ambito()


def visitar_sentencia_if(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> None:
    """Valida RS-6 en estructuras condicionales if / else if / else."""
    linea = _extraer_linea(nodo)
    condicion = nodo[1]
    bloque_then = nodo[2]
    rama_else = nodo[3] if len(nodo) == 5 else None

    tipo_cond = evaluar_expresion(condicion, tabla_simbolos, contexto)
    if tipo_cond != "error_tipo" and tipo_cond != "bool":
        registrar_error_semantico(
            "estructuras de control",
            linea,
            f"La condición de la sentencia 'if' debe ser de tipo 'bool', se recibió '{tipo_cond}'.",
            contexto,
        )
    elif tipo_cond == "bool":
        registrar_validacion_semantica(
            linea,
            "RS-6 (Estructuras de control)",
            "Condición booleana válida en sentencia 'if'.",
            contexto,
        )

    visitar_bloque(bloque_then, tabla_simbolos, contexto, f"if_{linea}")

    if rama_else is not None:
        if isinstance(rama_else, tuple) and rama_else[0] == "if":
            visitar_sentencia_if(rama_else, tabla_simbolos, contexto)
        elif isinstance(rama_else, list):
            visitar_bloque(rama_else, tabla_simbolos, contexto, f"else_{linea}")


def visitar_sentencia_for(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> None:
    """Valida RS-6 en ciclos for (infinito, condicional, clásico y range)."""
    etiqueta = nodo[0]
    linea = _extraer_linea(nodo)

    tabla_simbolos.entrar_ambito(f"for_{linea}")
    contexto["profundidad_for"] += 1
    try:
        if etiqueta == "for_infinito":
            cuerpo = nodo[1]
            registrar_validacion_semantica(
                linea,
                "RS-6 (Estructuras de control)",
                "Bucle 'for' infinito validado.",
                contexto,
            )
            if cuerpo:
                for sent in cuerpo:
                    visitar_nodo(sent, tabla_simbolos, contexto)

        elif etiqueta == "for_cond":
            condicion, cuerpo = nodo[1], nodo[2]
            tipo_cond = evaluar_expresion(condicion, tabla_simbolos, contexto)
            if tipo_cond != "error_tipo" and tipo_cond != "bool":
                registrar_error_semantico(
                    "estructuras de control",
                    linea,
                    f"La condición del ciclo 'for' debe ser de tipo 'bool', se recibió '{tipo_cond}'.",
                    contexto,
                )
            elif tipo_cond == "bool":
                registrar_validacion_semantica(
                    linea,
                    "RS-6 (Estructuras de control)",
                    "Condición booleana válida en ciclo 'for'.",
                    contexto,
                )
            if cuerpo:
                for sent in cuerpo:
                    visitar_nodo(sent, tabla_simbolos, contexto)

        elif etiqueta == "for_clasico":
            init_nodo, condicion, post_nodo, cuerpo = nodo[1], nodo[2], nodo[3], nodo[4]
            if init_nodo is not None:
                visitar_nodo(init_nodo, tabla_simbolos, contexto)

            tipo_cond = evaluar_expresion(condicion, tabla_simbolos, contexto)
            if tipo_cond != "error_tipo" and tipo_cond != "bool":
                registrar_error_semantico(
                    "estructuras de control",
                    linea,
                    f"La condición del ciclo 'for' clásico debe ser 'bool', se recibió '{tipo_cond}'.",
                    contexto,
                )
            elif tipo_cond == "bool":
                registrar_validacion_semantica(
                    linea,
                    "RS-6 (Estructuras de control)",
                    "Ciclo 'for' clásico con condición 'bool' validado.",
                    contexto,
                )

            if post_nodo is not None:
                visitar_nodo(post_nodo, tabla_simbolos, contexto)

            if cuerpo:
                for sent in cuerpo:
                    visitar_nodo(sent, tabla_simbolos, contexto)

        elif etiqueta == "for_range":
            var_clave, var_valor, expr_coleccion, cuerpo = nodo[1], nodo[2], nodo[3], nodo[4]
            tipo_coleccion = evaluar_expresion(expr_coleccion, tabla_simbolos, contexto)

            if tipo_coleccion != "error_tipo":
                tipos_iter = obtener_tipos_iteracion_range(tipo_coleccion)
                if tipos_iter is None:
                    registrar_error_semantico(
                        "estructuras de control",
                        linea,
                        f"No se puede iterar con 'range' sobre el tipo '{tipo_coleccion}'; se esperaba arreglo, slice o mapa.",
                        contexto,
                    )
                else:
                    tipo_k, tipo_v = tipos_iter
                    if var_clave == var_valor:
                        registrar_error_semantico(
                            "identificadores",
                            linea,
                            f"El identificador '{var_valor}' ya fue declarado previamente en este bloque.",
                            contexto,
                        )
                    tabla_simbolos.declarar(
                        Simbolo(
                            nombre=var_clave,
                            categoria="variable",
                            tipo_dato=tipo_k,
                            ambito=tabla_simbolos.ambito_actual(),
                            linea=linea,
                        )
                    )
                    tabla_simbolos.declarar(
                        Simbolo(
                            nombre=var_valor,
                            categoria="variable",
                            tipo_dato=tipo_v,
                            ambito=tabla_simbolos.ambito_actual(),
                            linea=linea,
                        )
                    )
                    registrar_validacion_semantica(
                        linea,
                        "RS-6 (Estructuras de control)",
                        f"Iteración 'for range' válida sobre '{tipo_coleccion}'.",
                        contexto,
                    )

            if cuerpo:
                for sent in cuerpo:
                    visitar_nodo(sent, tabla_simbolos, contexto)
    finally:
        contexto["profundidad_for"] -= 1
        tabla_simbolos.salir_ambito()


def visitar_sentencia_switch(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> None:
    """Valida RS-6 en sentencias switch (con y sin selector) y sus cláusulas case/default."""
    linea = _extraer_linea(nodo)
    expr_selector = nodo[1]
    lista_casos = nodo[2]

    if expr_selector is not None:
        tipo_selector = evaluar_expresion(expr_selector, tabla_simbolos, contexto)
    else:
        tipo_selector = "bool"

    contexto["profundidad_switch"] += 1
    try:
        for caso in lista_casos:
            tipo_nodo_caso = caso[0]
            linea_caso = _extraer_linea(caso, linea)

            if tipo_nodo_caso == "case":
                expr_caso = caso[1]
                sents_caso = caso[2]
                tipo_caso = evaluar_expresion(expr_caso, tabla_simbolos, contexto)

                if (
                    tipo_selector != "error_tipo"
                    and tipo_caso != "error_tipo"
                    and tipo_caso != tipo_selector
                ):
                    registrar_error_semantico(
                        "estructuras de control",
                        linea_caso,
                        f"La expresión del 'case' es de tipo '{tipo_caso}' y no coincide con el tipo '{tipo_selector}' del 'switch'.",
                        contexto,
                    )
                elif tipo_caso == tipo_selector and tipo_selector != "error_tipo":
                    registrar_validacion_semantica(
                        linea_caso,
                        "RS-6 (Estructuras de control)",
                        f"Cláusula 'case' compatible con tipo '{tipo_selector}'.",
                        contexto,
                    )

                visitar_bloque(sents_caso, tabla_simbolos, contexto, f"case_{linea_caso}")

            elif tipo_nodo_caso == "default":
                sents_default = caso[1]
                visitar_bloque(
                    sents_default, tabla_simbolos, contexto, f"default_{linea_caso}"
                )
    finally:
        contexto["profundidad_switch"] -= 1


def visitar_interrupcion_control(
    nodo: tuple[Any, ...],
    _tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> None:
    """Valida RS-6 para el uso contextual de break, continue y fallthrough."""
    palabra = str(nodo[1])
    linea = _extraer_linea(nodo)

    if palabra == "break":
        if contexto["profundidad_for"] <= 0 and contexto["profundidad_switch"] <= 0:
            registrar_error_semantico(
                "estructuras de control",
                linea,
                "La instrucción 'break' solo puede usarse dentro de un bucle 'for' o un 'switch'.",
                contexto,
            )
        else:
            registrar_validacion_semantica(
                linea,
                "RS-6 (Estructuras de control)",
                "Instrucción 'break' utilizada en un contexto válido.",
                contexto,
            )

    elif palabra == "continue":
        if contexto["profundidad_for"] <= 0:
            registrar_error_semantico(
                "estructuras de control",
                linea,
                "La instrucción 'continue' solo puede usarse dentro de un bucle 'for'.",
                contexto,
            )
        else:
            registrar_validacion_semantica(
                linea,
                "RS-6 (Estructuras de control)",
                "Instrucción 'continue' utilizada dentro de un bucle 'for'.",
                contexto,
            )

    elif palabra == "fallthrough":
        if contexto["profundidad_switch"] <= 0:
            registrar_error_semantico(
                "estructuras de control",
                linea,
                "La instrucción 'fallthrough' solo puede usarse dentro de un bloque 'switch'.",
                contexto,
            )
        else:
            registrar_validacion_semantica(
                linea,
                "RS-6 (Estructuras de control)",
                "Instrucción 'fallthrough' utilizada dentro de un bloque 'switch'.",
                contexto,
            )
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================


# =====================================================================
# SECCIÓN 3: UNICIDAD EN EL ALCANCE, RETORNO DE FUNCIONES Y FACHADA DEL ANALIZADOR
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def _extraer_linea_nodo(nodo: Any, por_defecto: int = 1) -> int:
    """Obtiene la línea adjunta al final de una tupla AST cuando es entera."""
    if isinstance(nodo, tuple) and nodo and isinstance(nodo[-1], int):
        return nodo[-1]
    return por_defecto


def _construir_firma_funcion(
    parametros: list[tuple[str, str]],
    tipo_retorno: str | None,
) -> str:
    """Construye la representación canónica `func(t1, t2)->ret` de una función."""
    tipos_param = ", ".join(tipo for _, tipo in parametros)
    ret = tipo_retorno if tipo_retorno else "void"
    return f"func({tipos_param})->{ret}"


def _descomponer_firma_funcion(
    firma: str,
) -> tuple[list[tuple[str, str]], str] | None:
    """Extrae lista de parámetros sintéticos y tipo de retorno desde una firma."""
    if not firma.startswith("func(") or ")->" not in firma:
        return None
    cuerpo_params, tipo_ret = firma[len("func("):].rsplit(")->", 1)
    if not cuerpo_params.strip():
        return [], tipo_ret
    params = [
        (f"arg{idx}", parte.strip())
        for idx, parte in enumerate(cuerpo_params.split(","), start=1)
        if parte.strip()
    ]
    return params, tipo_ret


def verificar_unicidad_alcance(
    nombre: str,
    linea: int,
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any] | None = None,
) -> bool:
    """RS-2: Verifica que `nombre` no exista previamente en el ámbito actual."""
    existente = tabla_simbolos.buscar_en_ambito_actual(nombre)
    if existente is not None:
        registrar_error_semantico(
            "identificadores",
            linea,
            f"El identificador '{nombre}' ya fue declarado previamente en este bloque (línea {existente.linea}).",
            contexto,
        )
        return False
    return True


def visitar_definicion_struct(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> None:
    """RS-2 y RS-5: Registra un tipo `struct` y valida la unicidad de sus campos."""
    nombre = str(nodo[1])
    campos_crudos = nodo[2] or []
    linea = _extraer_linea_nodo(nodo)

    if not verificar_unicidad_alcance(nombre, linea, tabla_simbolos, contexto):
        return

    campos_struct: dict[str, str] = {}
    tiene_error_campos = False
    for campo_nombre, campo_tipo in campos_crudos:
        if campo_nombre in campos_struct:
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El campo '{campo_nombre}' está duplicado en la estructura '{nombre}'.",
                contexto,
            )
            tiene_error_campos = True
            continue
        campos_struct[str(campo_nombre)] = str(campo_tipo)

    if tiene_error_campos:
        return

    simbolo = Simbolo(
        nombre=nombre,
        categoria="tipo_struct",
        tipo_dato=nombre,
        ambito=tabla_simbolos.ambito_actual(),
        linea=linea,
        mutable=False,
        inicializado=True,
        campos_struct=campos_struct,
    )
    tabla_simbolos.declarar(simbolo)
    registrar_validacion_semantica(
        linea,
        "RS-2 (Unicidad en el alcance)",
        f"Estructura '{nombre}' declarada con {len(campos_struct)} campo(s).",
        contexto,
    )


def _registrar_firma_funcion(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> Simbolo | None:
    """Registra la firma de una función en el ámbito actual respetando RS-2."""
    nombre = str(nodo[1])
    parametros = [(str(n), str(t)) for n, t in (nodo[2] or [])]
    tipo_retorno = str(nodo[3]) if nodo[3] else "void"
    linea = _extraer_linea_nodo(nodo)

    if not verificar_unicidad_alcance(nombre, linea, tabla_simbolos, contexto):
        return None

    firma = _construir_firma_funcion(parametros, tipo_retorno)
    simbolo = Simbolo(
        nombre=nombre,
        categoria="funcion",
        tipo_dato=firma,
        ambito=tabla_simbolos.ambito_actual(),
        linea=linea,
        mutable=False,
        inicializado=True,
        parametros=parametros,
        tipo_retorno=tipo_retorno,
    )
    tabla_simbolos.declarar(simbolo)
    registrar_validacion_semantica(
        linea,
        "RS-2 (Unicidad en el alcance)",
        f"Función '{nombre}' declarada con firma '{firma}'.",
        contexto,
    )
    return simbolo


def _declarar_parametros_en_ambito(
    parametros: list[tuple[str, str]],
    linea: int,
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> None:
    """Declara los parámetros formales dentro del ámbito de la función."""
    for nombre_param, tipo_param in parametros:
        if not verificar_unicidad_alcance(nombre_param, linea, tabla_simbolos, contexto):
            continue
        tipo_interno = (
            f"[]{tipo_param[3:]}"
            if tipo_param.startswith("...")
            else tipo_param
        )
        tabla_simbolos.declarar(
            Simbolo(
                nombre=nombre_param,
                categoria="parametro",
                tipo_dato=tipo_interno,
                ambito=tabla_simbolos.ambito_actual(),
                linea=linea,
                mutable=True,
                inicializado=True,
            )
        )


def _como_bloque(rama: Any) -> list[Any]:
    """Normaliza una rama (`list` o nodo `if` anidado de `else if`) a lista de sentencias."""
    if isinstance(rama, list):
        return rama
    return [rama] if isinstance(rama, tuple) else []


def _tiene_break(sentencias: list[Any] | None) -> bool:
    """Detecta un `break` directo o dentro de un `if` (sin entrar en bucles internos)."""
    for sent in sentencias or []:
        if not isinstance(sent, tuple):
            continue
        if sent[0] == "interrupcion" and sent[1] == "break":
            return True
        if sent[0] == "if" and (
            _tiene_break(sent[2]) or (len(sent) == 5 and _tiene_break(_como_bloque(sent[3])))
        ):
            return True
    return False


def _switch_garantiza_retorno(casos: list[Any]) -> bool:
    """Un `switch` garantiza retorno si tiene `default` y cada rama aplicable retorna sin `break`."""
    tiene_default = False
    for idx, caso in enumerate(casos):
        if not isinstance(caso, tuple) or caso[0] not in ("case", "default"):
            continue
        tiene_default = tiene_default or caso[0] == "default"
        sents = (caso[1] if caso[0] == "default" else caso[2]) or []

        if _tiene_break(sents):
            return False
        termina_fallthrough = (
            bool(sents)
            and isinstance(sents[-1], tuple)
            and sents[-1][:2] == ("interrupcion", "fallthrough")
        )
        if termina_fallthrough and idx + 1 < len(casos):
            continue
        if not _bloque_garantiza_retorno(sents):
            return False
    return tiene_default


def _sentencia_garantiza_retorno(sent: Any) -> bool:
    """Verifica si una sentencia (`return`, `if/else` o `switch`) retorna en todas sus rutas."""
    if not isinstance(sent, tuple):
        return False
    etiqueta = sent[0]
    if etiqueta == "return":
        return True
    if etiqueta == "if" and len(sent) == 5:
        return _bloque_garantiza_retorno(sent[2]) and _bloque_garantiza_retorno(_como_bloque(sent[3]))
    if etiqueta == "switch":
        return _switch_garantiza_retorno(sent[2] or [])
    return False


def _bloque_garantiza_retorno(sentencias: list[Any] | None) -> bool:
    """Verifica estructuralmente si algún paso del bloque garantiza un `return`."""
    return any(_sentencia_garantiza_retorno(sent) for sent in (sentencias or []))


def _ejecutar_cuerpo_funcion(
    simbolo_func: Simbolo,
    parametros: list[tuple[str, str]],
    bloque: list[Any],
    linea: int,
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
    *,
    etiqueta_funcion: str,
) -> bool:
    """Valida parámetros, cuerpo y retorno de una función aislando ámbito y contexto."""
    func_anterior = contexto["funcion_actual"]
    retorno_anterior = contexto["tiene_retorno"]
    for_anterior = contexto["profundidad_for"]
    switch_anterior = contexto["profundidad_switch"]

    tabla_simbolos.entrar_ambito(f"func:{simbolo_func.nombre}")
    contexto["funcion_actual"] = simbolo_func
    contexto["tiene_retorno"] = False
    contexto["profundidad_for"] = 0
    contexto["profundidad_switch"] = 0

    try:
        _declarar_parametros_en_ambito(parametros, linea, tabla_simbolos, contexto)
        for sentencia in bloque:
            if isinstance(sentencia, tuple):
                visitar_nodo(sentencia, tabla_simbolos, contexto)

        tipo_retorno = simbolo_func.tipo_retorno or "void"
        if tipo_retorno != "void" and not _bloque_garantiza_retorno(bloque):
            registrar_error_semantico(
                "retorno de funciones",
                linea,
                f"{etiqueta_funcion} no contiene una sentencia 'return' que devuelva el tipo esperado '{tipo_retorno}'.",
                contexto,
            )
            return False
        return True
    finally:
        tabla_simbolos.salir_ambito()
        contexto["funcion_actual"] = func_anterior
        contexto["tiene_retorno"] = retorno_anterior
        contexto["profundidad_for"] = for_anterior
        contexto["profundidad_switch"] = switch_anterior


def visitar_declaracion_funcion(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
    simbolo_preregistrado: Simbolo | None = None,
) -> None:
    """RS-2 y RS-5: Valida declaración, parámetros, cuerpo y retorno de funciones."""
    nombre = str(nodo[1])
    parametros = [(str(n), str(t)) for n, t in (nodo[2] or [])]
    tipo_retorno = str(nodo[3]) if nodo[3] else "void"
    bloque = nodo[4] or []
    linea = _extraer_linea_nodo(nodo)

    simbolo_func = (
        simbolo_preregistrado
        if simbolo_preregistrado is not None
        else _registrar_firma_funcion(nodo, tabla_simbolos, contexto)
    )
    if simbolo_func is None:
        return

    valido = _ejecutar_cuerpo_funcion(
        simbolo_func,
        parametros,
        bloque,
        linea,
        tabla_simbolos,
        contexto,
        etiqueta_funcion=f"La función '{nombre}'",
    )
    if valido and tipo_retorno == "void":
        registrar_validacion_semantica(
            linea,
            "RS-5 (Retorno de funciones)",
            f"Función '{nombre}' sin retorno ('void') validada.",
            contexto,
        )


def visitar_literal_funcion(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> str:
    """RS-5: Valida una función anónima en ámbito temporal y retorna su firma."""
    parametros = [(str(n), str(t)) for n, t in (nodo[1] or [])]
    tipo_retorno = str(nodo[2]) if nodo[2] else "void"
    bloque = nodo[3] or []
    linea = _extraer_linea_nodo(nodo)
    firma = _construir_firma_funcion(parametros, tipo_retorno)

    simbolo_anonima = Simbolo(
        nombre=f"anonima_{linea}",
        categoria="funcion",
        tipo_dato=firma,
        ambito=tabla_simbolos.ambito_actual(),
        linea=linea,
        mutable=False,
        inicializado=True,
        parametros=parametros,
        tipo_retorno=tipo_retorno,
    )

    valido = _ejecutar_cuerpo_funcion(
        simbolo_anonima,
        parametros,
        bloque,
        linea,
        tabla_simbolos,
        contexto,
        etiqueta_funcion="La función anónima",
    )
    if not valido:
        return "error_tipo"

    registrar_validacion_semantica(
        linea,
        "RS-5 (Retorno de funciones)",
        f"Literal de función con firma '{firma}' validado.",
        contexto,
    )
    return firma


def visitar_sentencia_retorno(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> None:
    """RS-5: Valida existencia y compatibilidad del tipo en sentencias `return`."""
    expr = nodo[1]
    linea = _extraer_linea_nodo(nodo)
    funcion_actual: Simbolo | None = contexto.get("funcion_actual")

    if funcion_actual is None:
        registrar_error_semantico(
            "retorno de funciones",
            linea,
            "La sentencia 'return' solo puede utilizarse dentro de una función.",
            contexto,
        )
        return

    tipo_esperado = funcion_actual.tipo_retorno or "void"
    nombre_func = funcion_actual.nombre

    if expr is None:
        contexto["tiene_retorno"] = True
        if tipo_esperado != "void":
            registrar_error_semantico(
                "retorno de funciones",
                linea,
                f"La función '{nombre_func}' debe retornar un valor de tipo '{tipo_esperado}'.",
                contexto,
            )
            return
        registrar_validacion_semantica(
            linea,
            "RS-5 (Retorno de funciones)",
            f"Retorno vacío válido en función '{nombre_func}'.",
            contexto,
        )
        return

    tipo_ret = evaluar_expresion(expr, tabla_simbolos, contexto)
    contexto["tiene_retorno"] = True

    if tipo_ret == "error_tipo":
        return

    if tipo_esperado == "void":
        registrar_error_semantico(
            "retorno de funciones",
            linea,
            f"La función '{nombre_func}' no declara tipo de retorno pero intenta retornar un valor de tipo '{tipo_ret}'.",
            contexto,
        )
        return

    if tipo_ret != tipo_esperado:
        registrar_error_semantico(
            "retorno de funciones",
            linea,
            f"El valor retornado '{tipo_ret}' no coincide con el tipo esperado '{tipo_esperado}' en la función '{nombre_func}'.",
            contexto,
        )
        return

    registrar_validacion_semantica(
        linea,
        "RS-5 (Retorno de funciones)",
        f"Retorno de tipo '{tipo_ret}' válido en '{nombre_func}'.",
        contexto,
    )


def validar_llamada_funcion(
    nodo: tuple[Any, ...],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> str:
    """RS-1 y RS-5: Valida llamadas a funciones de usuario y `fmt.Print`/`fmt.Println`."""
    etiqueta = nodo[0]
    linea = _extraer_linea_nodo(nodo)

    if etiqueta in ("println", "print"):
        argumentos = nodo[1] or []
        nombre_fn = "fmt.Println" if etiqueta == "println" else "fmt.Print"
        for arg in argumentos:
            tipo_arg = evaluar_expresion(arg, tabla_simbolos, contexto)
            if tipo_arg == "void":
                registrar_error_semantico(
                    "asignación de tipo",
                    linea,
                    f"La expresión pasada a '{nombre_fn}' no produce ningún valor (tipo 'void').",
                    contexto,
                )
        registrar_validacion_semantica(
            linea,
            "RS-1 (Identificadores)",
            f"Invocación a '{nombre_fn}' validada con {len(argumentos)} argumento(s).",
            contexto,
        )
        return "void"

    nombre = str(nodo[1])
    argumentos = nodo[2] or []
    simbolo = tabla_simbolos.buscar_visible(nombre)

    if simbolo is None:
        registrar_error_semantico(
            "identificadores",
            linea,
            f"La función '{nombre}' no ha sido declarada en este alcance.",
            contexto,
        )
        return "error_tipo"

    if simbolo.categoria == "funcion":
        parametros = list(simbolo.parametros)
        tipo_retorno = simbolo.tipo_retorno or "void"
    else:
        descompuesta = _descomponer_firma_funcion(simbolo.tipo_dato)
        if descompuesta is None:
            registrar_error_semantico(
                "identificadores",
                linea,
                f"El identificador '{nombre}' de tipo '{simbolo.tipo_dato}' no es una función invocable.",
                contexto,
            )
            return "error_tipo"
        parametros, tipo_retorno = descompuesta

    es_variadica = bool(parametros and parametros[-1][1].startswith("..."))
    if es_variadica:
        min_args = len(parametros) - 1
        if len(argumentos) < min_args:
            registrar_error_semantico(
                "retorno de funciones",
                linea,
                f"La función variádica '{nombre}' requiere al menos {min_args} argumento(s), pero recibió {len(argumentos)}.",
                contexto,
            )
            return "error_tipo"
    elif len(argumentos) != len(parametros):
        registrar_error_semantico(
            "retorno de funciones",
            linea,
            f"La función '{nombre}' espera {len(parametros)} argumento(s), pero recibió {len(argumentos)}.",
            contexto,
        )
        return "error_tipo"

    tiene_error_arg = False
    for idx, arg in enumerate(argumentos):
        tipo_arg = evaluar_expresion(arg, tabla_simbolos, contexto)
        if tipo_arg == "error_tipo":
            tiene_error_arg = True
            continue

        if es_variadica and idx >= len(parametros) - 1:
            tipo_esperado = parametros[-1][1][3:]
        else:
            tipo_esperado = parametros[idx][1]

        if tipo_arg != tipo_esperado:
            registrar_error_semantico(
                "asignación de tipo",
                linea,
                f"El argumento {idx + 1} de '{nombre}' espera '{tipo_esperado}', pero recibió '{tipo_arg}'.",
                contexto,
            )
            tiene_error_arg = True

    if tiene_error_arg:
        return "error_tipo"

    registrar_validacion_semantica(
        linea,
        "RS-5 (Retorno de funciones)",
        f"Llamada a '{nombre}' válida (retorna '{tipo_retorno}').",
        contexto,
    )
    return tipo_retorno


def _visitar_raiz_programa(
    elementos_top: list[Any],
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> None:
    """Pre-registra structs y firmas de funciones globales, y luego recorre sus cuerpos."""
    firmas_preregistradas: dict[int, Simbolo | None] = {}
    structs_procesados: set[int] = set()

    for elem in elementos_top:
        if not isinstance(elem, tuple):
            continue
        if elem[0] == "struct":
            visitar_definicion_struct(elem, tabla_simbolos, contexto)
            structs_procesados.add(id(elem))
        elif elem[0] in ("declaracion_funcion", "declaracion_funcion_variadica"):
            firmas_preregistradas[id(elem)] = _registrar_firma_funcion(
                elem, tabla_simbolos, contexto
            )

    for elem in elementos_top:
        if not isinstance(elem, tuple):
            continue
        if id(elem) in structs_procesados:
            continue
        if elem[0] in ("declaracion_funcion", "declaracion_funcion_variadica"):
            simbolo_pre = firmas_preregistradas.get(id(elem))
            if simbolo_pre is not None:
                visitar_declaracion_funcion(
                    elem,
                    tabla_simbolos,
                    contexto,
                    simbolo_preregistrado=simbolo_pre,
                )
            continue
        visitar_nodo(elem, tabla_simbolos, contexto)


_DESPACHADORES_AST: dict[str, Any] = {
    # Sección 3 (Pablo): Structs, funciones, retorno y llamadas
    "struct": visitar_definicion_struct,
    "declaracion_funcion": visitar_declaracion_funcion,
    "declaracion_funcion_variadica": visitar_declaracion_funcion,
    "return": visitar_sentencia_retorno,
    "llamada_funcion": validar_llamada_funcion,
    "println": validar_llamada_funcion,
    "print": validar_llamada_funcion,
    # Sección 1 (Hivor): Declaraciones, asignaciones, compuestas y lectura
    "declaracion_var": visitar_declaracion_var,
    "declaracion_const": visitar_declaracion_const,
    "declaracion_var_inferencia": visitar_declaracion_var_inferencia,
    "declaracion_corta": visitar_declaracion_corta,
    "asignacion": visitar_asignacion,
    "asignacion_compuesta": visitar_asignacion_compuesta,
    "scanln": visitar_sentencia_lectura,
    "arreglo": visitar_declaraciones_compuestas,
    "slice": visitar_declaraciones_compuestas,
    "mapa": visitar_declaraciones_compuestas,
    "struct_init": visitar_declaraciones_compuestas,
    # Sección 2 (Josué): Control de flujo e interrupciones
    "if": visitar_sentencia_if,
    "for_infinito": visitar_sentencia_for,
    "for_cond": visitar_sentencia_for,
    "for_clasico": visitar_sentencia_for,
    "for_range": visitar_sentencia_for,
    "switch": visitar_sentencia_switch,
    "interrupcion": visitar_interrupcion_control,
}


def visitar_nodo(
    nodo: Any,
    tabla_simbolos: TablaSimbolos,
    contexto: dict[str, Any],
) -> Any:
    """Despachador general del AST hacia los visitadores de las Secciones 1, 2 y 3."""
    if nodo is None or not isinstance(nodo, tuple):
        return None

    etiqueta = nodo[0]

    if etiqueta == "programa":
        contexto["es_programa_completo"] = True
        _visitar_raiz_programa(nodo[3] or [], tabla_simbolos, contexto)
        return None

    if etiqueta == "fragmento":
        contexto["es_programa_completo"] = False
        _visitar_raiz_programa(nodo[1] or [], tabla_simbolos, contexto)
        return None

    if etiqueta == "import":
        return None

    if etiqueta == "incremento":
        return validar_operacion_unaria(
            str(nodo[1]),
            nodo[2],
            _extraer_linea_nodo(nodo),
            tabla_simbolos,
            contexto,
        )

    visitador = _DESPACHADORES_AST.get(etiqueta)
    if visitador is not None:
        return visitador(nodo, tabla_simbolos, contexto)

    return evaluar_expresion(nodo, tabla_simbolos, contexto)


def analizar_semantica(
    codigo: str,
    res_sintactico: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Fachada principal del Analizador Semántico.
    Reutiliza `res_sintactico` si se provee (evitando doble parseo) e inspecciona
    el AST para construir la tabla de símbolos y validar las reglas RS-1 a RS-6.
    """
    if res_sintactico is None:
        from src.parser import analizar_sintaxis

        res_sintactico = analizar_sintaxis(codigo)

    tabla = TablaSimbolos()
    contexto = crear_contexto_semantico(usar_globales=True)

    arbol = res_sintactico.get("arbol")
    if arbol is not None:
        visitar_nodo(arbol, tabla, contexto)

    errores_lexicos = list(res_sintactico.get("errores_lexicos", []))
    errores_sintacticos = list(res_sintactico.get("errores", []))
    contexto["errores"].sort(key=lambda e: e["linea"])
    errores_sem = list(contexto["errores"])

    valido = (
        not errores_lexicos
        and not errores_sintacticos
        and not errores_sem
        and (arbol is not None or not codigo.strip())
    )

    return {
        "tokens": list(res_sintactico.get("tokens", [])),
        "errores_lexicos": errores_lexicos,
        "arbol": arbol,
        "reglas_sintacticas": list(res_sintactico.get("reglas", [])),
        "errores_sintacticos": errores_sintacticos,
        "simbolos": tabla.exportar_lista_diccionarios(),
        "reglas_semanticas": list(contexto["reglas_semanticas"]),
        "errores": errores_sem,
        "valido": valido,
    }
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

"""
Módulo del Analizador Sintáctico para un Subconjunto de Go (Avance 2)
=====================================================================
Implementa la gramática libre de contexto LALR(1) con `ply.yacc` consumiendo
los tokens estandarizados en español de `src/lexer.py`.

Autores:
    - Pablo Naranjo (@PabloNaranjoM)
    - Hivor Araujo (@AraujoHivor)
    - Josué Pacheco (@JosuePach3co)
"""

from __future__ import annotations

from typing import Any

# =====================================================================
# SECCIÓN 0: IMPORTS, TOKENS Y CONFIGURACIÓN GLOBAL DEL PARSER
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
try:
    import ply.yacc as yacc
except ImportError:
    yacc = None

from src.lexer import (
    build_lexer,
    calcular_columna,
    formatear_categoria_token,
    tokens,
)

start = "programa"

errores_sintacticos: list[dict[str, Any]] = []
reglas_validadas: list[dict[str, Any]] = []
_codigo_actual: str = ""


def _linea_de_produccion(p: Any) -> int:
    """Retorna la línea inicial de la producción; contrato base al final de cada tupla AST."""
    for idx in range(1, len(p)):
        linea = p.lineno(idx)
        if linea:
            return linea
    return 1


def registrar_regla(p: Any, nombre_regla: str, descripcion: str = "") -> None:
    linea = _linea_de_produccion(p)
    reglas_validadas.append({
        "linea": linea,
        "regla": nombre_regla,
        "descripcion": descripcion or f"Regla '{nombre_regla}' validada.",
        "mensaje": f"[Línea {linea}] Regla '{nombre_regla}' validada.",
    })
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 1: ESTRUCTURA RAÍZ DEL PROGRAMA, PAQUETES Y BLOQUES
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def p_programa_completo(p):
    """programa : PAQUETE ID fin_opc lista_imports_opc lista_elementos_top_opc"""
    registrar_regla(p, "programa")
    p[0] = ("programa", p[2], p[4], p[5], _linea_de_produccion(p))


def p_programa_fragmento(p):
    """programa : lista_elementos_top"""
    registrar_regla(p, "programa")
    p[0] = ("fragmento", p[1], _linea_de_produccion(p))


def p_fin_opc(p):
    """fin_opc : PUNTO_COMA
               | vacio"""
    p[0] = p[1]
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
def p_lista_imports_opc(p):
    """lista_imports_opc : lista_imports
                         | vacio"""
    p[0] = p[1]


def p_lista_imports(p):
    """lista_imports : declaracion_import
                     | lista_imports declaracion_import"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


def p_declaracion_import_simple(p):
    """declaracion_import : IMPORTAR LITERAL_CADENA fin_opc"""
    registrar_regla(p, "declaracion_import")
    p[0] = ("import", [p[2]])


def p_declaracion_import_grupo(p):
    """declaracion_import : IMPORTAR PAR_IZQ lista_cadenas_import PAR_DER fin_opc"""
    registrar_regla(p, "declaracion_import")
    p[0] = ("import", p[3])


def p_lista_cadenas_import(p):
    """lista_cadenas_import : LITERAL_CADENA fin_opc
                            | lista_cadenas_import LITERAL_CADENA fin_opc"""
    p[0] = [p[1]] if len(p) == 3 else p[1] + [p[2]]


def p_lista_elementos_top_opc(p):
    """lista_elementos_top_opc : lista_elementos_top
                               | vacio"""
    p[0] = p[1]


def p_lista_elementos_top(p):
    """lista_elementos_top : elemento_top
                           | lista_elementos_top elemento_top"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


def p_elemento_top(p):
    """elemento_top : declaracion_funcion fin_opc
                    | definicion_struct fin_opc
                    | sentencia fin_opc"""
    p[0] = p[1]


def p_bloque(p):
    """bloque : LLAVE_IZQ lista_sentencias_opc LLAVE_DER"""
    p[0] = p[2]


def p_lista_sentencias_opc(p):
    """lista_sentencias_opc : lista_sentencias
                            | vacio"""
    p[0] = p[1]


def p_lista_sentencias(p):
    """lista_sentencias : sentencia_bloque
                        | lista_sentencias sentencia_bloque"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


def p_sentencia_bloque(p):
    """sentencia_bloque : sentencia fin_opc
                        | error fin_opc"""
    p[0] = p[1]


def p_sentencia(p):
    """sentencia : declaracion_var
                 | declaracion_const
                 | declaracion_corta
                 | declaracion_arreglo
                 | declaracion_slice
                 | declaracion_mapa
                 | asignacion
                 | incremento
                 | sentencia_if
                 | sentencia_for
                 | sentencia_switch
                 | sentencia_retorno
                 | sentencia_interrupcion
                 | sentencia_impresion
                 | sentencia_lectura
                 | llamada_funcion"""
    p[0] = p[1]
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================


# =====================================================================
# SECCIÓN 2: DECLARACIÓN DE VARIABLES
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
# TODO (Avance 3 - Paso 2.1 | Hivor Araujo @AraujoHivor):
#       - Agregar regla `p_declaracion_const` para soportar declaraciones `const`
#         (con y sin tipo explícito) adjuntando `linea`.
#       - Adjuntar `linea` en `declaracion_var`.

def p_declaracion_const(p):
    """declaracion_const : CONSTANTE ID tipo ASIGNACION expresion
                         | CONSTANTE ID ASIGNACION expresion"""

    registrar_regla(p, "declaracion_const")
    linea = _linea_de_produccion(p)

    if len(p) == 6:
        # Constante con tipo explicito
        p[0] = ("declaracion_const", p[2], p[3], p[5], linea)
    else:
        # Constante con tipo inferido
        p[0] = ("declaracion_const", p[2], None, p[4], linea)

def p_declaracion_var_tipada(p):
    """declaracion_var : VARIABLE ID tipo ASIGNACION expresion"""
    registrar_regla(p, "declaracion_var")
    linea = _linea_de_produccion(p)
    p[0] = ("declaracion_var", p[2], p[3], p[5], linea)


def p_declaracion_var_sin_valor(p):
    """declaracion_var : VARIABLE ID tipo"""
    registrar_regla(p, "declaracion_var")
    linea = _linea_de_produccion(p)
    p[0] = ("declaracion_var", p[2], p[3], None, linea)

# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
def p_declaracion_var_inferencia(p):
    """declaracion_var : VARIABLE ID ASIGNACION expresion"""
    registrar_regla(p, "declaracion_var")
    p[0] = ("declaracion_var_inferencia", p[2], p[4])
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def p_declaracion_corta(p):
    """declaracion_corta : ID ASIGNACION_CORTA expresion"""
    registrar_regla(p, "declaracion_corta")
    p[0] = ("declaracion_corta", p[1], p[3], _linea_de_produccion(p))
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 3: EXPRESIONES ARITMÉTICAS
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
# TODO (Avance 3 - Paso 2.1 | Hivor Araujo @AraujoHivor):
#       - Etiquetar `p_factor_literales` para distinguir literales de variables:
#         ("literal", tipo_go, valor, linea) en enteros, flotantes, cadenas y booleanos.
#       - Modificar `p_referencia` para etiquetar identificadores simples como
#         ("id", nombre, linea) y agregar `linea` a `campo`, `indice`, `suma` y `multiplicacion`.
def p_expresion_aritmetica_suma(p):
    """expresion_aritmetica : expresion_aritmetica SUMA termino"""
    registrar_regla(p, "expresion_aritmetica")

    linea = _linea_de_produccion(p)
    p[0] = ("suma", p[1], p[3], linea)




def p_termino_multiplicacion(p):
    """termino : termino MULTIPLICACION factor"""
    registrar_regla(p, "termino")

    linea = _linea_de_produccion(p)
    p[0] = ("multiplicacion", p[1], p[3], linea)


def p_factor_literales(p):
    """factor : LITERAL_ENTERO
              | LITERAL_FLOTANTE
              | LITERAL_CADENA
              | VERDADERO
              | FALSO
              | referencia
              | llamada_funcion"""

    tipos = {
        "LITERAL_ENTERO": "int",
        "LITERAL_FLOTANTE": "float64",
        "LITERAL_CADENA": "string",
        "VERDADERO": "bool",
        "FALSO": "bool",
    }

    tipo_token = p.slice[1].type

    if tipo_token in tipos:
        linea = p.lineno(1)
        p[0] = ("literal", tipos[tipo_token], p[1], linea)
    else:
        # Las referencias y llamadas ya tienen su propia estructura.
        p[0] = p[1]




def p_referencia(p):
    """referencia : ID
                  | referencia PUNTO ID
                  | referencia CORCHETE_IZQ expresion CORCHETE_DER"""
    if len(p) == 2:
        # Referencia sencilla: edad
        p[0] = ("id", p[1], p.lineno(1))

    elif len(p) == 4:
        # Acceso a un campo: persona.nombre
        p[0] = ("campo", p[1], p[3], p.lineno(2))

    else:
        # Acceso por indice: numeros[0]
        p[0] = ("indice", p[1], p[3], p.lineno(2))

# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
def p_expresion_aritmetica_resta(p):
    """expresion_aritmetica : expresion_aritmetica RESTA termino"""
    registrar_regla(p, "expresion_aritmetica")
    p[0] = ("resta", p[1], p[3])


def p_expresion_aritmetica_termino(p):
    """expresion_aritmetica : termino"""
    p[0] = p[1]
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def p_termino_division(p):
    """termino : termino DIVISION factor"""
    registrar_regla(p, "termino")
    p[0] = ("division", p[1], p[3], _linea_de_produccion(p))


def p_termino_modulo(p):
    """termino : termino MODULO factor"""
    registrar_regla(p, "termino")
    p[0] = ("modulo", p[1], p[3], _linea_de_produccion(p))


def p_termino_factor(p):
    """termino : factor"""
    p[0] = p[1]


def p_factor_agrupacion(p):
    """factor : PAR_IZQ expresion PAR_DER"""
    p[0] = p[2]


def p_factor_unario(p):
    """factor : AMPERSAND referencia
              | RESTA factor"""
    p[0] = ("unario", p[1], p[2], _linea_de_produccion(p))
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 4: EXPRESIONES BOOLEANAS
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
def p_expresion_booleana_or(p):
    """expresion_booleana : expresion_booleana O_LOGICO conjuncion"""
    registrar_regla(p, "expresion_booleana")
    p[0] = ("or", p[1], p[3])


def p_expresion_booleana_base(p):
    """expresion_booleana : conjuncion"""
    p[0] = p[1]


def p_expresion(p):
    """expresion : expresion_booleana
                 | literal_funcion"""
    p[0] = p[1]
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
def p_conjuncion_and(p):
    """conjuncion : conjuncion Y_LOGICO comparacion"""
    registrar_regla(p, "conjuncion")

    linea = _linea_de_produccion(p)
    p[0] = ("and", p[1], p[3], linea)



def p_conjuncion_base(p):
    """conjuncion : comparacion"""
    p[0] = p[1]
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def p_comparacion_relacional(p):
    """comparacion : expresion_aritmetica op_relacional expresion_aritmetica"""
    registrar_regla(p, "comparacion")
    p[0] = ("comparacion", p[2], p[1], p[3], _linea_de_produccion(p))


def p_op_relacional(p):
    """op_relacional : IGUAL_IGUAL
                     | DIFERENTE
                     | MENOR
                     | MAYOR
                     | MENOR_IGUAL
                     | MAYOR_IGUAL"""
    p[0] = p[1]


def p_comparacion_negacion(p):
    """comparacion : NEGACION comparacion"""
    registrar_regla(p, "comparacion")
    p[0] = ("not", p[2], _linea_de_produccion(p))


def p_comparacion_base(p):
    """comparacion : expresion_aritmetica"""
    p[0] = p[1]
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 5: ESTRUCTURAS DE CONTROL Y ASIGNACIONES
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
def p_sentencia_if(p):
    """sentencia_if : SI expresion_booleana bloque
                    | SI expresion_booleana bloque SINO bloque
                    | SI expresion_booleana bloque SINO sentencia_if"""

    registrar_regla(p, "sentencia_if")
    linea = _linea_de_produccion(p)

    if len(p) == 4:
        # if sencillo
        p[0] = ("if", p[2], p[3], linea)
    else:
        # if-else o else if
        p[0] = ("if", p[2], p[3], p[5], linea)
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def p_sentencia_for_infinito(p):
    """sentencia_for : PARA bloque"""
    registrar_regla(p, "sentencia_for")
    p[0] = ("for_infinito", p[2], _linea_de_produccion(p))


def p_sentencia_for_condicional(p):
    """sentencia_for : PARA expresion_booleana bloque"""
    registrar_regla(p, "sentencia_for")
    p[0] = ("for_cond", p[2], p[3], _linea_de_produccion(p))


def p_sentencia_for_clasico(p):
    """sentencia_for : PARA inicializacion_for PUNTO_COMA expresion_booleana PUNTO_COMA post_sentencia bloque"""
    registrar_regla(p, "sentencia_for")
    p[0] = ("for_clasico", p[2], p[4], p[6], p[7], _linea_de_produccion(p))


def p_sentencia_for_range(p):
    """sentencia_for : PARA ID COMA ID ASIGNACION_CORTA RANGO expresion_booleana bloque"""
    registrar_regla(p, "sentencia_for")
    p[0] = ("for_range", p[2], p[4], p[7], p[8], _linea_de_produccion(p))


def p_inicializacion_for(p):
    """inicializacion_for : declaracion_corta
                          | asignacion"""
    p[0] = p[1]


def p_post_sentencia(p):
    """post_sentencia : incremento
                      | referencia ASIGNACION expresion_booleana
                      | referencia op_asignacion_compuesta expresion_booleana"""
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "=":
        registrar_regla(p, "asignacion")
        p[0] = ("asignacion", p[1], p[3], _linea_de_produccion(p))
    else:
        registrar_regla(p, "asignacion_compuesta")
        p[0] = ("asignacion_compuesta", p[2], p[1], p[3], _linea_de_produccion(p))
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
# TODO (Avance 3 - Paso 2.2 | Josué Pacheco @JosuePach3co):
#       - Soportar `switch` sin expresión booleana (`SEGUN LLAVE_IZQ lista_casos LLAVE_DER`).
#       - Adjuntar `linea` en todas las tuplas AST de sus bloques (`declaracion_var_inferencia`,
#         `resta`, `or`, `and`, `not`, `switch`, `case`, `default`, `interrupcion`,
#         `asignacion`, `asignacion_compuesta`, `incremento`, `slice` y `literal_funcion`).
def p_sentencia_switch(p):
    """sentencia_switch : SEGUN expresion_booleana LLAVE_IZQ lista_casos LLAVE_DER"""
    registrar_regla(p, "sentencia_switch")
    p[0] = ("switch", p[2], p[4])


def p_lista_casos(p):
    """lista_casos : caso
                   | lista_casos caso"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


def p_caso(p):
    """caso : CASO expresion DOS_PUNTOS lista_sentencias_opc
            | DEFECTO DOS_PUNTOS lista_sentencias_opc"""
    if len(p) == 5:
        p[0] = ("case", p[2], p[4])
    else:
        p[0] = ("default", p[3])


def p_sentencia_interrupcion(p):
    """sentencia_interrupcion : ROMPER
                              | CONTINUAR
                              | CAIDA"""
    registrar_regla(p, "sentencia_interrupcion")
    p[0] = ("interrupcion", p[1])


def p_asignacion_simple(p):
    """asignacion : referencia ASIGNACION expresion"""
    registrar_regla(p, "asignacion")
    p[0] = ("asignacion", p[1], p[3])


def p_asignacion_compuesta(p):
    """asignacion : referencia op_asignacion_compuesta expresion"""
    registrar_regla(p, "asignacion_compuesta")
    p[0] = ("asignacion_compuesta", p[2], p[1], p[3])


def p_op_asignacion_compuesta(p):
    """op_asignacion_compuesta : MAS_IGUAL
                               | MENOS_IGUAL
                               | MULT_IGUAL
                               | DIV_IGUAL
                               | MOD_IGUAL"""
    p[0] = p[1]


def p_incremento(p):
    """incremento : referencia INCREMENTO
                  | referencia DECREMENTO"""
    registrar_regla(p, "incremento")
    p[0] = ("incremento", p[2], p[1])
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================


# =====================================================================
# SECCIÓN 6: ESTRUCTURAS DE DATOS Y TIPOS
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
def p_declaracion_arreglo(p):
    """declaracion_arreglo : VARIABLE ID CORCHETE_IZQ expresion CORCHETE_DER tipo
                           | ID ASIGNACION_CORTA CORCHETE_IZQ expresion CORCHETE_DER tipo LLAVE_IZQ lista_expresiones_opc LLAVE_DER"""

    registrar_regla(p, "declaracion_arreglo")
    linea = _linea_de_produccion(p)

    if len(p) == 7:
        # Declaracion de arreglo sin valores iniciales
        p[0] = ("arreglo", p[2], p[4], p[6], None, linea)
    else:
        # Declaracion de arreglo con valores iniciales
        p[0] = ("arreglo", p[1], p[4], p[6], p[8], linea)


def p_tipo(p):
    """tipo : TIPO_ENTERO
            | TIPO_FLOTANTE
            | TIPO_CADENA
            | TIPO_BOOLEANO"""
    p[0] = p[1]
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
def p_declaracion_slice(p):
    """declaracion_slice : ID ASIGNACION_CORTA CORCHETE_IZQ CORCHETE_DER tipo LLAVE_IZQ lista_expresiones_opc LLAVE_DER"""
    registrar_regla(p, "declaracion_slice")
    p[0] = ("slice", p[1], p[5], p[7])


def p_lista_expresiones_opc(p):
    """lista_expresiones_opc : lista_expresiones
                             | vacio"""
    p[0] = p[1]


def p_lista_expresiones(p):
    """lista_expresiones : expresion
                         | lista_expresiones COMA expresion"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def p_declaracion_mapa(p):
    """declaracion_mapa : ID ASIGNACION_CORTA MAPA CORCHETE_IZQ tipo CORCHETE_DER tipo LLAVE_IZQ lista_elementos_mapa_opc LLAVE_DER"""
    registrar_regla(p, "declaracion_mapa")
    p[0] = ("mapa", p[1], p[5], p[7], p[9], _linea_de_produccion(p))


def p_lista_elementos_mapa_opc(p):
    """lista_elementos_mapa_opc : lista_elementos_mapa coma_opc
                                | vacio"""
    p[0] = p[1]


def p_coma_opc(p):
    """coma_opc : COMA
                | vacio"""
    p[0] = p[1]


def p_lista_elementos_mapa(p):
    """lista_elementos_mapa : elemento_mapa
                            | lista_elementos_mapa COMA elemento_mapa"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_elemento_mapa(p):
    """elemento_mapa : expresion DOS_PUNTOS expresion"""
    p[0] = (p[1], p[3])


def p_definicion_struct(p):
    """definicion_struct : TIPO ID ESTRUCTURA LLAVE_IZQ lista_campos LLAVE_DER"""
    registrar_regla(p, "definicion_struct")
    p[0] = ("struct", p[2], p[5], _linea_de_produccion(p))


def p_lista_campos(p):
    """lista_campos : campo
                    | lista_campos campo"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


def p_campo(p):
    """campo : ID tipo fin_opc"""
    p[0] = (p[1], p[2])


def p_instanciacion_struct(p):
    """expresion : referencia LLAVE_IZQ lista_elementos_mapa_opc LLAVE_DER"""
    registrar_regla(p, "instanciacion_struct")
    p[0] = ("struct_init", p[1], p[3], _linea_de_produccion(p))
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 7: DECLARACIONES Y LLAMADAS DE FUNCIONES
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
def p_declaracion_funcion(p):
    """declaracion_funcion : FUNCION ID PAR_IZQ parametros_opc PAR_DER tipo bloque
                           | FUNCION ID PAR_IZQ parametros_opc PAR_DER bloque"""

    registrar_regla(p, "declaracion_funcion")
    linea = _linea_de_produccion(p)

    if len(p) == 8:
        # Funcion que declara un tipo de retorno
        p[0] = ("declaracion_funcion", p[2], p[4], p[6], p[7], linea)
    else:
        # Funcion sin tipo de retorno
        p[0] = ("declaracion_funcion", p[2], p[4], None, p[6], linea)


def p_parametros_opc(p):
    """parametros_opc : lista_parametros
                      | vacio"""
    p[0] = p[1]


def p_lista_parametros(p):
    """lista_parametros : parametro
                        | lista_parametros COMA parametro"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_parametro(p):
    """parametro : ID tipo"""
    p[0] = (p[1], p[2])



def p_sentencia_retorno(p):
    """sentencia_retorno : RETORNAR expresion
                         | RETORNAR"""

    registrar_regla(p, "sentencia_retorno")
    linea = _linea_de_produccion(p)

    if len(p) == 3:
        # return con un valor
        p[0] = ("return", p[2], linea)
    else:
        # return sin valor
        p[0] = ("return", None, linea)


def p_argumentos_opc(p):
    """argumentos_opc : lista_argumentos
                      | vacio"""
    p[0] = p[1]


def p_lista_argumentos(p):
    """lista_argumentos : expresion
                        | lista_argumentos COMA expresion"""
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_vacio(p):
    """vacio :"""
    p[0] = []
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
def p_literal_funcion(p):
    """literal_funcion : FUNCION PAR_IZQ parametros_opc PAR_DER tipo bloque"""
    registrar_regla(p, "literal_funcion")
    p[0] = ("literal_funcion", p[3], p[5], p[6])
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def p_declaracion_funcion_variadica(p):
    """declaracion_funcion : FUNCION ID PAR_IZQ parametros_variadicos PAR_DER tipo bloque"""
    registrar_regla(p, "declaracion_funcion_variadica")
    p[0] = ("declaracion_funcion_variadica", p[2], p[4], p[6], p[7], _linea_de_produccion(p))


def p_parametros_variadicos(p):
    """parametros_variadicos : ID ELIPSIS tipo
                             | lista_parametros COMA ID ELIPSIS tipo"""
    if len(p) == 4:
        p[0] = [(p[1], f"...{p[3]}")]
    else:
        p[0] = p[1] + [(p[3], f"...{p[5]}")]


def p_llamada_funcion(p):
    """llamada_funcion : ID PAR_IZQ argumentos_opc PAR_DER"""
    registrar_regla(p, "llamada_funcion")
    p[0] = ("llamada_funcion", p[1], p[3], _linea_de_produccion(p))
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 8: IMPRESIÓN Y SOLICITUD DE DATOS (paquete fmt)
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
def p_sentencia_impresion_ln(p):
    """sentencia_impresion : PAQUETE_FMT PUNTO IMPRIMIR_LN PAR_IZQ argumentos_opc PAR_DER"""
    registrar_regla(p, "sentencia_impresion")
    p[0] = ("println", p[5])
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
def p_sentencia_impresion_simple(p):
    """sentencia_impresion : PAQUETE_FMT PUNTO IMPRIMIR PAR_IZQ argumentos_opc PAR_DER"""
    registrar_regla(p, "sentencia_impresion")
    p[0] = ("print", p[5])
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def p_sentencia_lectura(p):
    """sentencia_lectura : PAQUETE_FMT PUNTO LEER_LN PAR_IZQ lista_referencias PAR_DER
                         | PAQUETE_FMT PUNTO LEER PAR_IZQ lista_referencias PAR_DER"""
    registrar_regla(p, "sentencia_lectura")
    p[0] = ("scanln", p[5], _linea_de_produccion(p))


def p_lista_referencias(p):
    """lista_referencias : AMPERSAND referencia
                         | lista_referencias COMA AMPERSAND referencia"""
    p[0] = [p[2]] if len(p) == 3 else p[1] + [p[4]]
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# SECCIÓN 9: MANEJO DE ERRORES SINTÁCTICOS Y CONSTRUCTOR DEL PARSER
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
def _esperado_para_token(tipo_tok: str) -> str:
    if tipo_tok == "SINO":
        return "una sentencia válida o el cierre de bloque '}'"
    if tipo_tok in ("LLAVE_DER", "PAR_DER", "CORCHETE_DER"):
        return "completar la expresión o instrucción previa antes del delimitador de cierre"
    if tipo_tok in ("ASIGNACION", "ASIGNACION_CORTA"):
        return "un identificador o especificación de tipo antes del operador de asignación"
    return "una expresión, delimitador o sentencia válida según la gramática de Go"


def p_error(p):
    if p is not None:
        col = calcular_columna(_codigo_actual, p.lexpos) if _codigo_actual else 1
        esperado = _esperado_para_token(p.type)
        mensaje = (
            f"Error sintáctico en la línea {p.lineno}, columna {col}: "
            f"Token inesperado '{p.value}', se esperaba {esperado}."
        )
        errores_sintacticos.append({
            "linea": p.lineno,
            "columna": col,
            "token": str(p.value),
            "tipo": p.type,
            "mensaje": mensaje,
        })
    else:
        lineas = _codigo_actual.splitlines() if _codigo_actual else [""]
        ult_linea = max(1, len(lineas))
        ult_col = len(lineas[-1]) + 1 if lineas else 1
        mensaje = (
            f"Error sintáctico en la línea {ult_linea}, columna {ult_col}: "
            "Token inesperado 'EOF', se esperaba completar la sentencia o el cierre de bloque '}'."
        )
        errores_sintacticos.append({
            "linea": ult_linea,
            "columna": ult_col,
            "token": "EOF",
            "tipo": "EOF",
            "mensaje": mensaje,
        })
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
_PARSER_CACHE: Any = None


class _TokenStreamLexer:
    """Reproduce un flujo pre-escaneado de tokens PLY sin re-tokenizar el código fuente."""

    def __init__(self, lista_tokens: list[Any]) -> None:
        self._iter = iter(lista_tokens)
        self.lineno = 1
        self.lexpos = 0

    def input(self, _codigo: str) -> None:
        return None

    def token(self):
        tok = next(self._iter, None)
        if tok is not None:
            self.lineno = tok.lineno
            self.lexpos = tok.lexpos
        return tok


def build_parser(**kwargs):
    """Construye y retorna una instancia del analizador sintáctico LALR(1)."""
    global _PARSER_CACHE
    if not kwargs and _PARSER_CACHE is not None:
        return _PARSER_CACHE
    opciones = {
        "start": start,
        "debug": False,
        "write_tables": False,
        "errorlog": yacc.NullLogger(),
    }
    opciones.update(kwargs)
    instancia = yacc.yacc(**opciones)
    if not kwargs:
        _PARSER_CACHE = instancia
    return instancia


def analizar_sintaxis(codigo: str) -> dict[str, Any]:
    """
    Ejecuta el análisis léxico y sintáctico en una sola pasada léxica sobre
    `codigo` y retorna tokens, errores_lexicos, arbol, reglas, errores y valido.
    """
    global _codigo_actual
    _codigo_actual = codigo
    errores_sintacticos.clear()
    reglas_validadas.clear()

    lexer_parser = build_lexer()
    lexer_parser.errores_lexicos = []
    lexer_parser.input(codigo)
    tokens_raw = list(lexer_parser)
    errores_lexicos = list(lexer_parser.errores_lexicos)

    tokens_reconocidos = [
        {
            "indice": i,
            "linea": tok.lineno,
            "columna": calcular_columna(codigo, tok.lexpos),
            "tipo": tok.type,
            "categoria": formatear_categoria_token(tok.type, tok.value),
            "valor": tok.value,
        }
        for i, tok in enumerate(tokens_raw, start=1)
    ]

    parser = build_parser()
    arbol = (
        parser.parse(codigo, lexer=_TokenStreamLexer(tokens_raw), tracking=True)
        if codigo.strip()
        else None
    )

    valido = not errores_lexicos and not errores_sintacticos and (arbol is not None or not codigo.strip())
    return {
        "tokens": tokens_reconocidos,
        "errores_lexicos": errores_lexicos,
        "arbol": arbol,
        "reglas": list(reglas_validadas),
        "errores": list(errores_sintacticos),
        "valido": valido,
    }
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

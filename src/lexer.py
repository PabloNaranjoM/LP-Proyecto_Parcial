"""
Módulo del Analizador Léxico para un Subconjunto de Go
======================================================
Este módulo define la especificación léxica para un subconjunto representativo
del lenguaje de programación Go, utilizando la biblioteca PLY (Python Lex-Yacc).

El analizador está estructurado de forma modular y colaborativa entre los
tres integrantes del equipo, siguiendo el contrato de nombres establecido
en CONTRIBUTING.md y en el documento de propuesta técnica:
- Hivor Araujo (@AraujoHivor): 23 palabras reservadas base de Go (excluyendo map y struct),
  tipo predefinido 'string' ('TIPO_STRING'), identificadores ('ID'), literales enteros
  ('LITERAL_INT'), operadores aritméticos ('SUMA', 'RESTA', 'MULT', 'DIV', 'MOD'),
  asignación simple ('ASIGNACION') y delimitadores básicos ('PAR_IZQ', 'PAR_DER',
  'LLAVE_IZQ', 'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER').
- Pablo Naranjo (@PabloNaranjoM): Palabras reservadas 'map' ('MAP') y 'struct' ('STRUCT'),
  tipos numéricos 'int' ('TIPO_INT') y 'float64' ('TIPO_FLOAT64'), literales flotantes
  ('LITERAL_FLOAT'), literales de cadena ('LITERAL_STRING'), asignación corta
  ('ASIGNACION_CORTA'), asignaciones compuestas ('MAS_IGUAL', 'MENOS_IGUAL', 'MULT_IGUAL',
  'DIV_IGUAL', 'MOD_IGUAL'), incremento/decremento ('INCREMENTO', 'DECREMENTO'),
  comentarios (// y /* */), delimitadores/operadores ('DOS_PUNTOS', 'PUNTO_COMA',
  'AMPERSAND'), manejador de errores y constructor del lexer.
- Josué Pacheco (@JosuePach3co): Tipo predefinido 'bool' ('TIPO_BOOL'), constantes
  booleanas 'true' ('TRUE') y 'false' ('FALSE'), operadores relacionales ('IGUAL_IGUAL',
  'DIFERENTE', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL'), operadores lógicos
  ('AND', 'OR', 'NOT'), delimitadores ('COMA', 'PUNTO'), espacios ignorados y
  seguimiento de saltos de línea.

Autores:
    - Pablo Naranjo (@PabloNaranjoM)
    - Hivor Araujo (@AraujoHivor)
    - Josué Pacheco (@JosuePach3co)
"""

try:
    import ply.lex as lex
except ImportError:
    lex = None  # PLY se requiere al instanciar el analizador en build_lexer()


# =====================================================================
# SECCIÓN 1: DICCIONARIOS DE PALABRAS RESERVADAS Y LISTAS DE TOKENS
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
# TODO: Definir diccionario keywords_hivor con las 23 palabras reservadas base de Go
#       (excluyendo 'map' y 'struct') mapeadas a sus tokens en mayúsculas:
#       'break': 'BREAK', 'case': 'CASE', 'chan': 'CHAN', 'const': 'CONST',
#       'continue': 'CONTINUE', 'default': 'DEFAULT', 'defer': 'DEFER',
#       'else': 'ELSE', 'fallthrough': 'FALLTHROUGH', 'for': 'FOR',
#       'func': 'FUNC', 'go': 'GO', 'goto': 'GOTO', 'if': 'IF',
#       'import': 'IMPORT', 'interface': 'INTERFACE', 'package': 'PACKAGE',
#       'range': 'RANGE', 'return': 'RETURN', 'select': 'SELECT',
#       'switch': 'SWITCH', 'type': 'TYPE', 'var': 'VAR'.
# TODO: Mapear el tipo de dato predefinido 'string': 'TIPO_STRING' en keywords_hivor.
# TODO: Definir lista tokens_hivor con los nombres oficiales del contrato:
#       - Identificadores: 'ID'
#       - Literales enteros: 'LITERAL_INT'
#       - Operadores aritméticos: 'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD'
#       - Asignación simple: 'ASIGNACION'
#       - Delimitadores: 'PAR_IZQ', 'PAR_DER', 'LLAVE_IZQ', 'LLAVE_DER',
#         'CORCHETE_IZQ', 'CORCHETE_DER'
keywords_hivor: dict[str, str] = {}
tokens_hivor: list[str] = []
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
# TODO: Definir diccionario keywords_pablo con las palabras reservadas asignadas:
#       'map': 'MAP', 'struct': 'STRUCT'.
# TODO: Mapear los tipos de datos predefinidos en keywords_pablo:
#       'int': 'TIPO_INT', 'float64': 'TIPO_FLOAT64'.
# TODO: Definir lista tokens_pablo con los nombres oficiales del contrato:
#       - Literales numéricos de punto flotante: 'LITERAL_FLOAT'
#       - Literales de cadena con secuencias de escape: 'LITERAL_STRING'
#       - Declaración y asignación corta: 'ASIGNACION_CORTA' (:=)
#       - Asignaciones compuestas: 'MAS_IGUAL', 'MENOS_IGUAL', 'MULT_IGUAL',
#         'DIV_IGUAL', 'MOD_IGUAL'
#       - Incremento y decremento: 'INCREMENTO', 'DECREMENTO'
#       - Delimitadores y operadores: 'DOS_PUNTOS' (:), 'PUNTO_COMA' (;), 'AMPERSAND' (&)
keywords_pablo: dict[str, str] = {
    # Palabras reservadas oficiales de Go
    'map' : 'MAP',
    'struct' : 'STRUCT',

    # Identificadores predefinidos
    'int' : 'TIPO_INT',
    'float64' : 'TIPO_FLOAT64'
}

tokens_pablo: list[str] = [
    # Literales
    'LITERAL_FLOAT', 'LITERAL_STRING',
    
    # Operadores
    'ASIGNACION_CORTA', 'MAS_IGUAL', 'MENOS_IGUAL', 'MULT_IGUAL', 'DIV_IGUAL', 'MOD_IGUAL', 
    'INCREMENTO', 'DECREMENTO',

    # Delimitadores
    'DOS_PUNTOS', 'PUNTO_COMA', 'AMPERSAND'
    ]
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
# TODO: Mapear el tipo de dato predefinido en keywords_josue:
#       'bool': 'TIPO_BOOL'.
# TODO: Mapear las constantes booleanas predefinidas en keywords_josue:
#       'true': 'TRUE', 'false': 'FALSE'.
# TODO: Definir lista tokens_josue con los nombres oficiales del contrato:
#       - Operadores relacionales: 'IGUAL_IGUAL', 'DIFERENTE', 'MENOR',
#         'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL'
#       - Operadores lógicos: 'AND', 'OR', 'NOT'
#       - Delimitadores: 'COMA' (,), 'PUNTO' (.)
keywords_josue: dict[str, str] = {}
tokens_josue: list[str] = []
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# Unión estructural de palabras reservadas y consolidación de la tupla de tokens para PLY
KEYWORDS_MAP: dict[str, str] = {**keywords_hivor, **keywords_pablo, **keywords_josue}
tokens: tuple[str, ...] = tuple(tokens_hivor + tokens_pablo + tokens_josue + list(KEYWORDS_MAP.values()))


# =====================================================================
# SECCIÓN 2: REGLAS LÉXICAS SIMPLES (STRINGS t_...)
# =====================================================================

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
# TODO: Definir reglas regex en string (t_...) para operadores y delimitadores:
#       - Aritméticos: t_SUMA = r'\+', t_RESTA = r'-', t_MULT = r'\*',
#         t_DIV = r'/', t_MOD = r'%'
#       - Asignación simple: t_ASIGNACION = r'='
#       - Delimitadores: t_PAR_IZQ = r'\(', t_PAR_DER = r'\)',
#         t_LLAVE_IZQ = r'\{', t_LLAVE_DER = r'\}',
#         t_CORCHETE_IZQ = r'\[', t_CORCHETE_DER = r'\]'
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
# TODO: Definir reglas regex en string (t_...) para asignaciones, incremento y delimitadores:
#       - Asignación corta: t_ASIGNACION_CORTA = r':='
#       - Asignaciones compuestas: t_MAS_IGUAL = r'\+=', t_MENOS_IGUAL = r'-=',
#         t_MULT_IGUAL = r'\*=', t_DIV_IGUAL = r'/=', t_MOD_IGUAL = r'%='
#       - Incremento / Decremento: t_INCREMENTO = r'\+\+', t_DECREMENTO = r'--'
#       - Delimitadores / operadores: t_DOS_PUNTOS = r':', t_PUNTO_COMA = r';',
#         t_AMPERSAND = r'&'
#       (Nota de diseño: operadores multicarácter como :=, +=, ++ deben definirse
#        con prioridad frente a caracteres individuales cuando se usen strings).
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
# TODO: Definir reglas regex en string (t_...) para relacionales, lógicos y delimitadores:
#       - Operadores relacionales: t_IGUAL_IGUAL = r'==', t_DIFERENTE = r'!=',
#         t_MENOR_IGUAL = r'<=', t_MAYOR_IGUAL = r'>=', t_MENOR = r'<', t_MAYOR = r'>'
#       - Operadores lógicos: t_AND = r'&&', t_OR = r'\|\|', t_NOT = r'!'
#       - Delimitadores: t_COMA = r',', t_PUNTO = r'\.'
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================


# =====================================================================
# SECCIÓN 3: REGLAS LÉXICAS COMPLEJAS (FUNCIONES def t_...)
# =====================================================================
# ---------------------------------------------------------------------
# NOTA TÉCNICA SOBRE PRIORIDAD EN PLY (ply.lex):
# En PLY, todas las reglas definidas como funciones (def t_...) tienen
# precedencia sobre las reglas definidas como simples cadenas de texto.
# Entre las funciones, PLY las evalúa exactamente en el orden de aparición
# por número de línea en el archivo fuente.
#
# Por esta razón, la estructura de ordenación a continuación es fundamental:
#   1. Comentarios y Literales Complejos (Pablo Naranjo):
#      - Los comentarios deben descartarse antes de que su contenido interno
#        sea analizado como tokens válidos.
#      - El literal flotante (t_LITERAL_FLOAT) DEBE definirse antes que el
#        literal entero (t_LITERAL_INT), de lo contrario el prefijo entero
#        absorbería la parte decimal (ej. "3" de "3.14"), dejando el punto
#        decimal huérfano y provocando un error léxico o sintáctico posterior.
#      - Las cadenas de texto (t_LITERAL_STRING) con secuencias de escape deben
#        capturar la totalidad del literal entre comillas, procesando escapes
#        como \", \\, \n, \t.
#   2. Enteros e Identificadores (Hivor Araujo):
#      - t_LITERAL_INT captura secuencias numéricas enteras decimales (\d+).
#      - t_ID captura identificadores ([a-zA-Z_][a-zA-Z0-9_]*) y debe consultar
#        KEYWORDS_MAP para discriminar palabras reservadas y tipos de datos
#        de los identificadores creados por el usuario.
#   3. Utilidades del Analizador (Josué Pacheco):
#      - t_ignore descarta espacios en blanco y tabuladores (' \t').
#      - t_newline actualiza t.lexer.lineno para mantener el seguimiento exacto de líneas.
#   4. Manejador de Errores y Constructor del Lexer (Pablo Naranjo):
#      - t_error captura cualquier carácter no reconocido, reporta el error
#        y salta el carácter con t.lexer.skip(1) para continuar el análisis.
#      - build_lexer(**kwargs) construye y retorna la instancia de lex.
# ---------------------------------------------------------------------

# 1) Bloque de Pablo Naranjo (@PabloNaranjoM): Comentarios, Cadenas y Flotantes
# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
# TODO: def t_COMMENT_SINGLE(t): Regla para comentarios de línea (//...) que
#       descarte el token sin emitirlo.
# TODO: def t_COMMENT_MULTI(t): Regla para comentarios de bloque (/* ... */) que
#       incremente lineno según saltos de línea encontrados y detecte/reporte
#       error léxico en caso de comentario multilínea no cerrado al fin de archivo.
# TODO: def t_LITERAL_FLOAT(t): Regla para números en punto flotante (\d+\.\d+).
#       Debe ubicarse ANTES de t_LITERAL_INT para evitar consumo parcial del prefijo.
# TODO: def t_LITERAL_STRING(t): Regla para literales de cadena ("...") soportando
#       caracteres escapados (\", \\, \n, \t) y control de líneas internas.
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

# 2) Bloque de Hivor Araujo (@AraujoHivor): Enteros e Identificadores
# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
# TODO: def t_LITERAL_INT(t): Regla para números enteros decimales (\d+), convirtiendo
#       el lexema a entero en t.value.
# TODO: def t_ID(t): Regla para identificadores ([a-zA-Z_][a-zA-Z0-9_]*),
#       consultando KEYWORDS_MAP.get(t.value, 'ID') para discriminar palabras
#       reservadas y tipos predefinidos de nombres de variables/funciones.
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# 3) Bloque de Josué Pacheco (@JosuePach3co): Ignorados y Saltos de Línea
# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
# TODO: t_ignore = ' \t' para descartar espacios en blanco y tabulaciones.
# TODO: def t_newline(t): Regla para saltos de línea (\n+) que incremente
#       el contador t.lexer.lineno += len(t.value).
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# 4) Bloque de Pablo Naranjo (@PabloNaranjoM): Manejador de Errores y Constructor
# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
# TODO: def t_error(t): Manejador de errores léxicos que registre el carácter
#       ilegal, su número de línea y posición, e invoque t.lexer.skip(1).
# TODO: def build_lexer(**kwargs): Función fábrica que invoque y retorne
#       lex.lex(**kwargs) para instanciar el analizador léxico.
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

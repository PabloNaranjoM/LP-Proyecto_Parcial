"""
Módulo del Analizador Léxico para un Subconjunto de Go
======================================================
Este módulo define la especificación léxica para un subconjunto representativo
del lenguaje de programación Go, utilizando la biblioteca PLY (Python Lex-Yacc).

El analizador está estructurado de forma modular y colaborativa entre los
tres integrantes del equipo, siguiendo el contrato de nombres establecido
en el documento de propuesta técnica:
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
# Las palabras reservadas se reconocen desde t_ID para no dividir nombres
# como "variable" en "var" y "iable".
keywords_hivor: dict[str, str] = {
    'break': 'BREAK',
    'case': 'CASE',
    'chan': 'CHAN',
    'const': 'CONST',
    'continue': 'CONTINUE',
    'default': 'DEFAULT',
    'defer': 'DEFER',
    'else': 'ELSE',
    'fallthrough': 'FALLTHROUGH',
    'for': 'FOR',
    'func': 'FUNC',
    'go': 'GO',
    'goto': 'GOTO',
    'if': 'IF',
    'import': 'IMPORT',
    'interface': 'INTERFACE',
    'package': 'PACKAGE',
    'range': 'RANGE',
    'return': 'RETURN',
    'select': 'SELECT',
    'switch': 'SWITCH',
    'type': 'TYPE',
    'var': 'VAR',
    'string': 'TIPO_STRING',  # En Go es un tipo predefinido, no palabra reservada.
}

tokens_hivor: list[str] = [
    'ID', 'LITERAL_INT',
    'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD', 'ASIGNACION',
    'PAR_IZQ', 'PAR_DER', 'LLAVE_IZQ', 'LLAVE_DER',
    'CORCHETE_IZQ', 'CORCHETE_DER',
]

# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
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
keywords_josue: dict[str, str] = {
    'bool': 'TIPO_BOOL',
    'true': 'TRUE',
    'false': 'FALSE'
}

tokens_josue: list[str] = [
    'IGUAL_IGUAL', 'DIFERENTE', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL',
    'AND', 'OR', 'NOT',
    'COMA', 'PUNTO'
]
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
# Operadores aritmeticos y asignacion simple.
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_ASIGNACION = r'='

# Delimitadores que se usan en expresiones, bloques y arreglos.
t_PAR_IZQ = r'\('
t_PAR_DER = r'\)'
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'

# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

# Reglas para operadores
t_ASIGNACION_CORTA = r':='
t_MAS_IGUAL = r'\+='
t_MENOS_IGUAL = r'-='
t_MULT_IGUAL = r'\*='
t_DIV_IGUAL = r'/='
t_MOD_IGUAL = r'%='
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'

# Reglas para delimintadores
t_DOS_PUNTOS = r':'
t_PUNTO_COMA = r';'
t_AMPERSAND = r'&'
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
t_IGUAL_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MENOR_IGUAL = r'<='
t_MAYOR_IGUAL = r'>='
t_MENOR = r'<'
t_MAYOR = r'>'

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'

t_COMA = r','
t_PUNTO = r'\.'
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

# -----------------------------------------------------------------------------
# FUNCIÓN AUXILIAR PARA ERRORES LÉXICOS
# -----------------------------------------------------------------------------
def calcular_columna(data, lexpos):
    """Columna (1-based) de la posición lexpos dentro del texto data."""
    return lexpos - data.rfind('\n', 0, lexpos)


def registrar_error_lexico(lexer, linea, caracter, mensaje, lexpos=0):
    """Encapsula el reporte y almacenamiento de errores para main.py y la GUI."""
    print(mensaje)
    if not hasattr(lexer, 'errores_lexicos'):
        lexer.errores_lexicos = []
    lexer.errores_lexicos.append({
        'linea': linea,
        'columna': calcular_columna(lexer.lexdata, lexpos),
        'caracter': caracter,
        'mensaje': mensaje
    })

# Comentarios
def t_COMENTARIO_SIMPLE(t):
    r'//[^\n]*'
    pass

def t_COMENTARIO_MULTI(t):
    r'/\*([\s\S]*?\*/|[\s\S]*)'

    # Valida si el comentario no se cerró antes del EOF
    if not t.value[2:].endswith('*/'):
        mensaje = f"Error léxico en la línea {t.lineno}: comentario multilínea no cerrado al fin de archivo"
        registrar_error_lexico(t.lexer, t.lineno, '/*', mensaje, t.lexpos)
        return None

    t.lexer.lineno += t.value.count('\n')
    pass

# Literales
def t_LITERAL_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_LITERAL_STRING(t):
    #Soporta los escapes: \n, \t, \", \\, \r, \'
    r'"([^"\n\\]|\\[nrt\\\'"])*"'
    t.lexer.lineno += t.value.count('\n')
    return t
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

# 2) Bloque de Hivor Araujo (@AraujoHivor): Enteros e Identificadores
# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
def t_LITERAL_INT(t):
    r'[0-9]+'
    # Esta primera version reconoce enteros basicos, sin prefijos ni guiones bajos.
    t.value = int(t.value)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Primero se busca el nombre completo en el diccionario de palabras clave.
    t.type = KEYWORDS_MAP.get(t.value, 'ID')
    return t

# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

# 3) Bloque de Josué Pacheco (@JosuePach3co): Ignorados y Saltos de Línea
# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

# 4) Bloque de Pablo Naranjo (@PabloNaranjoM): Manejador de Errores y Constructor
# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def t_error(t):
    mensaje = f"Error léxico en la línea {t.lineno}: carácter no reconocido '{t.value[0]}'"
    registrar_error_lexico(t.lexer, t.lineno, t.value[0], mensaje, t.lexpos)
    t.lexer.skip(1)


def formatear_categoria_token(tipo, lexema=''):
    """Convierte el tipo de token de PLY a la categoría mostrada en la Tabla de Tokens."""
    if tipo.startswith('TIPO_'):
        return f"TIPO_DATO ({str(lexema).upper() or tipo[5:]})"
    if tipo in ('TRUE', 'FALSE'):
        return f"LITERAL_BOOL ({tipo})"
    if tipo in KEYWORDS_MAP.values():
        return f"RESERVADA ({tipo})"
    return tipo


def build_lexer(**kwargs):
    """Construye e inicializa una nueva instancia del analizador lexico PLY."""
    return lex.lex(**kwargs)


def analizar(codigo):
    """
    Tokeniza `codigo` y retorna (tokens, errores). Cada token incluye
    indice, linea, columna, tipo, categoria y valor.
    """
    lexer = build_lexer()
    lexer.errores_lexicos = []
    lexer.input(codigo)
    tokens = [
        {
            'indice': i,
            'linea': tok.lineno,
            'columna': calcular_columna(codigo, tok.lexpos),
            'tipo': tok.type,
            'categoria': formatear_categoria_token(tok.type, tok.value),
            'valor': tok.value,
        }
        for i, tok in enumerate(lexer, start=1)
    ]
    return tokens, lexer.errores_lexicos
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

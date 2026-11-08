import os
import ply.yacc as yacc
from datetime import datetime
from src.lexer import tokens, build_lexer

# =====================================================================
# REGLAS SINTACTICAS - Josue Pacheco (@JosuePach3co)
# =====================================================================

# 1. Declaración explicita con inferencia de tipo
def p_declaracion_var_inferencia(p):
    'declaracion_var : VAR ID ASIGNACION expresion'
    p[0] = ("var_inferencia", p[2], p[4])

# 2. Expresiones aritmeticas: Regla aditiva de resta
def p_expresion_resta(p):
    'expresion : expresion RESTA termino'
    p[0] = ("resta", p[1], p[3])

# 3. Expresiones booleanas: Regla de disyuncion logica (OR)
def p_expresion_booleana_or(p):
    'expresion_booleana : expresion_booleana OR conjuncion'
    p[0] = ("or", p[1], p[3])

def p_expresion_booleana_base(p):
    'expresion_booleana : conjuncion'
    p[0] = p[1]

# 4. Estructura de selección múltiple switch
def p_sentencia_switch(p):
    'sentencia_switch : SWITCH expresion LLAVE_IZQ lista_casos LLAVE_DER'
    p[0] = ("switch", p[2], p[4])

def p_lista_casos(p):
    '''lista_casos : caso
                   | lista_casos caso'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_caso(p):
    '''caso : CASE expresion DOS_PUNTOS lista_sentencias_opc
            | DEFAULT DOS_PUNTOS lista_sentencias_opc'''
    if p[1] == 'case':
        p[0] = ("case", p[2], p[4])
    else:
        p[0] = ("default", p[3])

def p_lista_sentencias_opc(p):
    '''lista_sentencias_opc : lista_sentencias
                            | vacio'''
    p[0] = p[1]

# 5. Declaracion e inicializacion de Slices dinamicos
def p_declaracion_slice(p):
    'declaracion_slice : ID ASIGNACION_CORTA CORCHETE_IZQ CORCHETE_DER tipo LLAVE_IZQ lista_expresiones_opc LLAVE_DER'
    p[0] = ("slice", p[1], p[5], p[7])

def p_lista_expresiones_opc(p):
    '''lista_expresiones_opc : lista_expresiones
                             | vacio'''
    p[0] = p[1]

def p_lista_expresiones(p):
    '''lista_expresiones : expresion
                         | lista_expresiones COMA expresion'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# 6. Funciones anonimas o expresiones lambda
def p_literal_funcion(p):
    'literal_funcion : FUNC PAR_IZQ parametros_opc PAR_DER tipo bloque'
    p[0] = ("func_anonima", p[3], p[5], p[6])

# 7. Impresion simple en consola con fmt.Print
def p_sentencia_impresion_simple(p):
    'sentencia_impresion : ID PUNTO ID PAR_IZQ argumentos_opc PAR_DER'
    if p[1] == "fmt" and p[3] == "Print":
        p[0] = ("print", p[5])
    else:
        mensaje = f"Llamada no soportada: {p[1]}.{p[3]}"
        errores_sintacticos.append(mensaje)
        p[0] = None

# =====================================================================
# REGLAS DE INTEGRACION BASE
# =====================================================================
def p_sentencia_josue(p):
    '''sentencia : declaracion_var
                 | sentencia_switch
                 | declaracion_slice
                 | sentencia_impresion
                 | ID ASIGNACION_CORTA literal_funcion''' 
    p[0] = p[1]

def p_programa(p):
    '''programa : sentencia'''
    p[0] = p[1]

def p_expresion_termino_base(p):
    '''expresion : termino
                 | literal_funcion'''
    p[0] = p[1]

def p_termino_factor_base(p):
    'termino : factor'
    p[0] = p[1]

def p_factor_base(p):
    '''factor : LITERAL_INT
              | LITERAL_FLOAT
              | LITERAL_STRING
              | ID
              | TRUE
              | FALSE'''
    p[0] = p[1]

def p_tipo_base(p):
    '''tipo : TIPO_INT
            | TIPO_FLOAT64
            | TIPO_STRING
            | TIPO_BOOL'''
    p[0] = p[1]

def p_conjuncion_base(p):
    '''conjuncion : ID
                  | TRUE
                  | FALSE'''
    p[0] = p[1]

def p_bloque_base(p):
    'bloque : LLAVE_IZQ lista_sentencias_opc LLAVE_DER'
    p[0] = p[2]

def p_lista_sentencias(p):
    '''lista_sentencias : sentencia
                        | lista_sentencias sentencia'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_parametros_opc_base(p):
    '''parametros_opc : ID tipo
                      | vacio'''
    if len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = p[1]

def p_argumentos_opc_base(p):
    '''argumentos_opc : lista_expresiones_opc'''
    p[0] = p[1]

def p_vacio(p):
    'vacio :'
    p[0] = []

errores_sintacticos = []

def p_error(p):
    if p:
        mensaje = f"Error sintactico en linea {p.lineno}: token inesperado '{p.value}'"
    else:
        mensaje = "Error sintactico: final inesperado del codigo"
    errores_sintacticos.append(mensaje)

# =====================================================================
# BATERIA DE PRUEBAS Y GENERACIÓN DE LOG - Josue Pacheco
# =====================================================================
if __name__ == "__main__":
    parser = yacc.yacc(start="programa", debug=False, write_tables=False)

    pruebas_josue = [
        "var promedio = 9.45",
        "var total = 10 - 5",
        """switch opcion {
            case 1:
                fmt.Print("Uno")
            default:
                fmt.Print("Otro")
        }""",
        "notas := []float64{8.5, 9.0, 10.0}",
        "duplicar := func(n int) int { var x = n }",
        "fmt.Print(\"Resultado: \", 10)",
        
        # --- ERRORES SINTACTICOS INTENCIONALES ---
        "var = 10", 
        "switch opcion { case 1 fmt.Print(1) }", 
        "fmt.Print(\"Hola\", )", 
    ]

    # Ejecutar pruebas y recolectar logs
    log_content = [
        "=" * 80,
        "REPORTE DE ANÁLISIS SINTÁCTICO - COMPILADOR GO (ESPOL)",
        "Desarrollador    : Josue Pacheco (@JosuePach3co)",
        "=" * 80,
        ""
    ]

    for i, codigo in enumerate(pruebas_josue, 1):
        errores_sintacticos.clear()
        resultado = parser.parse(codigo, lexer=build_lexer())
        
        log_content.append(f"PRUEBA {i}: \n{codigo.strip()}")
        if errores_sintacticos or resultado is None:
            log_content.append(f">>> Estado: INVALIDO")
            for err in errores_sintacticos:
                log_content.append(f"    - {err}")
        else:
            log_content.append(f">>> Estado: VALIDO")
            log_content.append(f"    - Arbol Yacc: {resultado}")
        log_content.append("-" * 80)

    # Crear carpeta y archivo de log con formato: sintactico-usuarioGit-fecha-hora.txt
    os.makedirs("logs", exist_ok=True)
    ahora = datetime.now()
    # Formato fecha DDMMYYYY-HHhMM (ej: 20102026-23h32)
    fecha_hora_str = ahora.strftime("%d%m%Y-%Hh%M")
    nombre_log = f"sintactico-JosuePach3co-{fecha_hora_str}.txt"
    ruta_log = os.path.join("logs", nombre_log)

    with open(ruta_log, "w", encoding="utf-8") as f_log:
        f_log.write("\n".join(log_content))

    print(f"[OK] Pruebas sintacticas completadas.")
    print(f"[OK] Log generado en: {ruta_log}")
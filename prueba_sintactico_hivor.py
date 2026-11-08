from datetime import datetime
from pathlib import Path
import ply.yacc as yacc
from src.lexer import tokens, build_lexer

# Prueba inicial de las reglas de Hivor.
# Por ahora, la regla inicial solo reconoce una declaracion.

def p_declaracion_var(p):
    'declaracion_var : VARIABLE ID tipo ASIGNACION expresion'
    p[0] = ("variable", p[2], p[3], p[5])


def p_tipo(p):
    '''tipo : TIPO_ENTERO
            | TIPO_FLOTANTE
            | TIPO_CADENA
            | TIPO_BOOLEANO'''
    p[0] = p[1]


# Suma: se puede repetir y combina expresiones con terminos.
def p_expresion_suma(p):
    'expresion : expresion SUMA termino'
    p[0] = ("suma", p[1], p[3])


def p_expresion_termino(p):
    'expresion : termino'
    p[0] = p[1]


# Multiplicacion: tiene mayor prioridad que la suma.
def p_termino_mult(p):
    'termino : termino MULTIPLICACION factor'
    p[0] = ("multiplicacion", p[1], p[3])


def p_termino_factor(p):
    'termino : factor'
    p[0] = p[1]


def p_factor(p):
    '''factor : LITERAL_ENTERO
              | LITERAL_FLOTANTE
              | LITERAL_CADENA
              | ID
              | VERDADERO
              | FALSO'''
    p[0] = p[1]



# Comparaciones que usaremos en nuestras condiciones.
# Por ahora probamos >= y <=.

def p_comparacion(p):
    '''comparacion : expresion MAYOR_IGUAL expresion
                   | expresion MENOR_IGUAL expresion'''
    p[0] = ("comparacion", p[2], p[1], p[3])


# Conjuncion logica: permite unir varias condiciones con &&.
def p_conjuncion(p):
    '''conjuncion : comparacion
                 | conjuncion Y_LOGICO comparacion'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("and", p[1], p[3])



# Condicional if, if-else y else if.
def p_sentencia_if(p):
    '''sentencia_if : SI conjuncion bloque
                    | SI conjuncion bloque SINO bloque
                    | SI conjuncion bloque SINO sentencia_if'''

    if len(p) == 4:
        # Solo if
        p[0] = ("if", p[2], p[3])
    else:
        # if-else o else if
        p[0] = ("if", p[2], p[3], p[5])



# Bloque entre llaves.
def p_bloque(p):
    'bloque : LLAVE_IZQ lista_sentencias LLAVE_DER'
    p[0] = p[2]


# Permite tener una o varias instrucciones dentro del bloque.
def p_lista_sentencias(p):
    '''lista_sentencias : sentencia
                        | lista_sentencias sentencia'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# Une las instrucciones que llevamos implementadas.

def p_sentencia(p):
    '''sentencia : declaracion_var
                 | sentencia_if
                 | declaracion_arreglo
                 | sentencia_retorno
                 | sentencia_impresion'''
    p[0] = p[1]



# Regla principal de esta prueba.
def p_programa(p):
    '''programa : sentencia
                | declaracion_funcion'''
    p[0] = p[1]




# Declaracion de arreglos de longitud fija.
# Ejemplo: var numeros [3]int

def p_declaracion_arreglo(p):
    'declaracion_arreglo : VARIABLE ID CORCHETE_IZQ expresion CORCHETE_DER tipo'

    p[0] = ("arreglo", p[2], p[4], p[6])



# Funcion normal con tipo de retorno.
# Ejemplo: func sumar(a int, b int) int { return a + b }

def p_declaracion_funcion(p):
    '''declaracion_funcion : FUNCION ID PAR_IZQ parametros_opc PAR_DER tipo bloque'''
    p[0] = ("funcion", p[2], p[4], p[6], p[7])


# Una funcion puede tener parametros o ninguno.
def p_parametros_opc(p):
    '''parametros_opc : lista_parametros
                      | vacio'''
    p[0] = p[1]


# Permite recibir uno o varios parametros.
def p_lista_parametros(p):
    '''lista_parametros : parametro
                        | lista_parametros COMA parametro'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# Cada parametro tiene nombre y tipo.
def p_parametro(p):
    'parametro : ID tipo'
    p[0] = (p[1], p[2])


# Instruccion return.
def p_sentencia_retorno(p):
    'sentencia_retorno : RETORNAR expresion'
    p[0] = ("return", p[2])


# Produccion vacia para funciones sin parametros.
def p_vacio(p):
    'vacio :'
    p[0] = []


# Impresion por consola con fmt.Println.
# Ejemplo: fmt.Println("Hola", edad)

def p_sentencia_impresion(p):
    'sentencia_impresion : PAQUETE_FMT PUNTO IMPRIMIR_LN PAR_IZQ argumentos_opc PAR_DER'
    p[0] = ("imprimir", p[5])


# Permite imprimir con argumentos o sin ellos.
def p_argumentos_opc(p):
    '''argumentos_opc : lista_argumentos
                      | vacio'''
    p[0] = p[1]


# Permite uno o varios argumentos separados por comas.
def p_lista_argumentos(p):
    '''lista_argumentos : expresion
                        | lista_argumentos COMA expresion'''

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


errores_sintacticos = []

def p_error(p):
    if p:
        mensaje = f"Error sintactico en linea {p.lineno}: {p.value}"
    else:
        mensaje = "Error sintactico: final inesperado del codigo"

    errores_sintacticos.append(mensaje)
    print(mensaje)




if __name__ == "__main__":
    parser = yacc.yacc(
        start="programa",
        debug=False,
        write_tables=False
    )

    pruebas = [
        "var edad int = 20",

        "var total int = 2 + 3 * 4",

        """if edad >= 18 && edad <= 60 {
            var estado string = "Permitido"
        }""",

        "var edad int =",

        
        # Prueba incorrecta: falta una comparacion despues de &&
        """if edad >= 18 && {
            var estado string = "Permitido"
        }""",

        # Prueba correcta de if-else
        """if edad >= 18 {
            var mensaje string = "Mayor de edad"
        } else {
            var mensaje string = "Menor de edad"
        }""",

        # Prueba correcta de else if
        """if edad >= 18 && edad <= 60 {
            var estado string = "Adulto"
        } else if edad >= 13 && edad <= 17 {
            var estado string = "Adolescente"
        } else {
            var estado string = "Otro"
        }""",

        
        # Arreglo sencillo
        "var numeros [3]int",

        # Arreglo con expresion de longitud
        "var notas [2 + 1]float64",

        # Error: falta cerrar el corchete
        "var edades [3 int",


        
        # Valida: funcion con dos parametros y retorno
        """func sumar(a int, b int) int {
            return a + b
        }""",

        # Valida: funcion sin parametros y con retorno
        """func obtenerNumero() int {
            return 10
        }""",

        # Invalida: falta el parentesis de cierre
        """func sumar(a int, b int {
            return a + b
        }""",

        # Invalida: return sin expresion
        """func fallida(a int) int {
            return
        }""",

        
        # Valida: impresion sencilla
        'fmt.Println("Hola mundo")',

        # Valida: varios argumentos y una operacion
        'fmt.Println("Total:", 2 + 3 * 4)',

        # Valida: funcion con impresion y retorno
        """func mostrarNumero(numero int) int {
            fmt.Println("Numero:", numero)
            return numero
        }""",

        # Invalida: falta un argumento despues de la coma
        'fmt.Println("Hola",)',


    ]


    
    # Guardar los resultados de las pruebas de Hivor.
    log = [
        "=" * 70,
        "REPORTE DE ANALISIS SINTACTICO - GO",
        "Desarrollador: Hivor Araujo (@AraujoHivor)",
        "=" * 70,
        ""
    ]

    validas = 0
    invalidas = 0

    for numero, codigo in enumerate(pruebas, start=1):
        errores_sintacticos.clear()

        print("\nProbando:", codigo)
        resultado = parser.parse(codigo, lexer=build_lexer())

        valido = not errores_sintacticos and resultado is not None
        estado = "VALIDO" if valido else "INVALIDO"

        print("Estado:", estado)

        log.append(f"PRUEBA {numero}")
        log.append("Codigo:")
        log.append(codigo.strip())
        log.append(f"Estado: {estado}")

        if valido:
            validas += 1
            print("Resultado:", resultado)
            log.append(f"Resultado: {resultado}")
        else:
            invalidas += 1
            for error in errores_sintacticos:
                log.append(f"Error: {error}")

            if not errores_sintacticos:
                log.append("Error: no se obtuvo un resultado valido")

        log.append("-" * 70)

    log.append(f"Pruebas validas: {validas}")
    log.append(f"Pruebas invalidas: {invalidas}")
    log.append(f"Total de pruebas: {len(pruebas)}")

    # Crear el archivo en la carpeta logs.
    carpeta = Path("logs")
    carpeta.mkdir(exist_ok=True)

    fecha = datetime.now().strftime("%d%m%Y-%Hh%M")
    nombre = f"sintactico-AraujoHivor-{fecha}.txt"
    ruta = carpeta / nombre

    ruta.write_text("\n".join(log) + "\n", encoding="utf-8")

    print("\nResumen de pruebas:")
    print(f"Validas: {validas}")
    print(f"Invalidas: {invalidas}")
    print(f"Log generado: {ruta}")



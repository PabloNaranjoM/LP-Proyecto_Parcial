# Compilador para Subconjunto de Go (ESPOL)

Analizador Léxico, Sintáctico y Semántico para un subconjunto del lenguaje de programación **Go**, desarrollado en **Python 3** mediante la herramienta de análisis léxico y sintáctico **PLY (`ply.lex` y `ply.yacc`)**, complementado con una interfaz gráfica moderna e interactiva implementada en **CustomTkinter**.

Este proyecto corresponde al desarrollo práctico de la materia **Lenguajes de Programación** de la Escuela Superior Politécnica del Litoral (**ESPOL**), bajo la dirección del profesor Ing. Rodrigo Saraguro.

---

## 👥 Equipo de Desarrollo

| Integrante | Rol / Usuario GitHub | Módulos Asignados (Avances 1, 2 y 3 - Léxico, Sintáctico, Semántico y GUI) |
| :--- | :--- | :--- |
| **Pablo Naranjo** | `@PabloNaranjoM` | **Léxico (`src/lexer.py`):** Palabras reservadas `ESTRUCTURA` (`struct`) y `MAPA` (`map`), paquete y lectura estándar (`PAQUETE_FMT`, `LEER_LN`, `LEER`), tipos numéricos (`TIPO_ENTERO`, `TIPO_FLOTANTE`), literales (`LITERAL_FLOTANTE`, `LITERAL_CADENA`), asignación corta (`ASIGNACION_CORTA`), asignaciones compuestas (`MAS_IGUAL`, `MENOS_IGUAL`, `MULT_IGUAL`, `DIV_IGUAL`, `MOD_IGUAL`), incremento/decremento (`INCREMENTO`, `DECREMENTO`), comentarios, delimitadores (`DOS_PUNTOS`, `PUNTO_COMA`, `AMPERSAND`, `ELIPSIS`), manejador `t_error` y `build_lexer()`.<br>**Sintáctico (`src/parser.py`):** Infraestructura del parser LALR(1) y jerarquía de precedencia de operadores, declaraciones cortas (`:=`), mapas y estructuras (`type ... struct`) e instanciación compuesta, funciones variádicas (`...`) y llamadas, entrada estándar (`fmt.Scanln`, `fmt.Scan`), bucle `for` en sus 4 variantes (`while`, clásico, infinito y `for ... range`), comparaciones (`>`, `<`, `>=`, `<=`), división/módulo y fachada `analizar_sintaxis()`.<br>**Semántico (`src/semantic.py`):** Modelo `Simbolo` y `TablaSimbolos` jerárquica con pila de ámbitos, formateadores `registrar_error_semantico()` / `registrar_validacion_semantica()`, **RS-2** (`identificadores`: unicidad en el alcance y definiciones `struct`), **RS-5** (`retorno de funciones`: tipo/existencia de `return`, firmas y llamadas), despachador del AST (`visitar_nodo()`) y fachada `analizar_semantica()`.<br>**GUI, CLI y Logs (`src/gui/app.py`, `src/gui/log_exporter.py`, `main.py`):** Orquestación PLY + CustomTkinter (`Léxico`, `Sintáctico`, `Semántico`, `▶ Ejecutar Todo`), Banner de Estado (`[VÁLIDO]` / `[ERROR]`), flujo completo en `ejecutar_analisis_completo_codigo()` y soporte CLI `--fase semantico`.<br>**Algoritmos de prueba:** `algoritmos/algoritmo1.go`, `algoritmos/algoritmo1_error.go`, `algoritmo1_sintactico.go`, `algoritmo1_error_sintactico.go`, `algoritmo1_semantico.go`, `algoritmo1_error_semantico.go`. |
| **Hivor Araujo** | `@AraujoHivor` | **Léxico (`src/lexer.py`):** Palabras reservadas principales del subconjunto de Go en español (`PAQUETE`, `IMPORTAR`, `FUNCION`, `VARIABLE`, `CONSTANTE`, `RETORNAR`, `SI`, `SINO`, `PARA`, `RANGO`, `SEGUN`, `CASO`, `DEFECTO`, `ROMPER`, `CONTINUAR`, `CAIDA`, `TIPO`), operadores aritméticos (`SUMA`, `RESTA`, `MULTIPLICACION`, `DIVISION`, `MODULO`), asignación simple (`ASIGNACION`), delimitadores de agrupación (`()`, `{}`, `[]`), función `IMPRIMIR_LN` (`Println`), identificadores (`ID`), `TIPO_CADENA` y `LITERAL_ENTERO`.<br>**Sintáctico (`src/parser.py`):** Declaración explícita de variables (`var`) y constantes (`const`), tipos primitivos (`p_tipo`), arreglos (`[N]T`), referencias e indexación (`arr[i]`, `obj.campo`), funciones estándar con y sin retorno (`func`), sentencia `return` (con expresión y vacía), condicional `if / else / else if`, salida con salto (`fmt.Println`), operaciones de suma/multiplicación, etiquetado de literales/referencias con línea y recuperación de errores (`p_error`).<br>**Semántico (`src/semantic.py`):** **RS-1** (`identificadores`: declaración previa obligatoria, indexación y acceso a campos de `struct`) y **RS-3** (`asignación de tipo`: compatibilidad estricta sin coerción implícita, inferencia en `var`/`:=`, inmutabilidad de `const`, lectura por consola y literales compuestos/`struct_init`).<br>**GUI y Logs (`src/gui/editor_panel.py`, `src/gui/log_exporter.py`, `src/gui/app.py`):** Panel de edición Go con numeración dinámica sincronizada, resaltado de sintaxis y líneas de error, carga de `.go`, botón `Limpiar` y exportación automatizada de reportes semánticos (`ejecutar_analisis_semantico_codigo()`).<br>**Algoritmos de prueba:** `algoritmos/algoritmo2.go`, `algoritmos/algoritmo2_error.go`, `algoritmos/algoritmo_general_hivor_valido.go`, `algoritmos/algoritmo_hivor_practica_errores.go`, `algoritmo2_sintactico.go`, `algoritmo2_error_sintactico.go`, `algoritmo2_semantico.go`, `algoritmo2_error_semantico.go`. |
| **Josué Pacheco** | `@JosuePach3co` | **Léxico (`src/lexer.py`):** Tipo predefinido `TIPO_BOOLEANO` (`bool`), literales booleanos (`VERDADERO`, `FALSO`), función `IMPRIMIR` (`Print`), operadores relacionales (`IGUAL_IGUAL`, `DIFERENTE`, `MENOR`, `MAYOR`, `MENOR_IGUAL`, `MAYOR_IGUAL`), operadores lógicos (`Y_LOGICO`, `O_LOGICO`, `NEGACION`), delimitadores (`PUNTO`, `COMA`), descarte de espacios (`t_ignore`) y seguimiento de saltos de línea (`t_newline`).<br>**Sintáctico (`src/parser.py`):** Estructura de bloques y sentencias, inferencia `var x = ...`, literales funcionales (`literal_funcion`), *slices*, estructura selectiva `switch / case / default` (con y sin expresión selector booleana), salida estándar sin salto (`fmt.Print`), asignaciones compuestas (`+=`, `-=`, `*=`, `/=`, `%=`), incremento/decremento (`++`, `--`), sentencias de salto (`break`, `continue`, `fallthrough`), operadores lógicos (`\|\|`) y resta (`-`).<br>**Semántico (`src/semantic.py`):** Evaluador recursivo de expresiones `evaluar_expresion()`, **RS-4** (`operaciones permitidas`: coherencia de tipos en operaciones aritméticas, relacionales, lógicas, unarias e incremento/decremento) y **RS-6** (`estructuras de control`: ámbitos de bloque, condiciones `bool`, iteración `for ... range`, `switch` e interrupciones `break`, `continue`, `fallthrough`).<br>**GUI (`src/gui/diagnostics_panel.py`, `src/gui/theme.py`):** Panel derecho con pestañas (`Tabla de Tokens`, `Reglas Sintácticas` y `Tabla de Símbolos` con `poblar_tabla_simbolos()` y `mostrar_resultados_semanticos()`) y consola de diagnóstico con visualización de línea y columna exacta.<br>**Algoritmos de prueba:** `algoritmos/algoritmo3.go`, `algoritmos/algoritmo3_error.go`, `algoritmo3_sintactico.go`, `algoritmo3_error_sintactico.go`, `algoritmo3_semantico.go`, `algoritmo3_error_semantico.go`. |

---

## 📌 Especificaciones e Instrucciones (Avances 1, 2 y 3)

Conforme a las indicaciones oficiales provistas por el docente:

1. **Analizador Léxico (`ply.lex` - `src/lexer.py`):**
   - Definición formal de componentes léxicos con nombres de tokens 100% estandarizados al español, incluyendo reconocimiento dedicado para `fmt` (`PAQUETE_FMT`) y funciones de E/S (`IMPRIMIR_LN`, `IMPRIMIR`, `LEER_LN`, `LEER`).
   - Manejo y recuperación ante errores léxicos (`t_error`), registrando caracteres ilegales y la línea/columna exacta.
2. **Analizador Sintáctico (`ply.yacc` - `src/parser.py`):**
   - Gramática Libre de Contexto LALR(1) libre de conflictos *shift/reduce* y *reduce/reduce* para el subconjunto de Go (declaraciones `var`/`const`/`:=`, funciones con parámetros y retorno simple/sin retorno, estructuras `struct`, arreglos, *slices*, mapas, `if/else`, `for` en sus 4 variantes, `switch/case/default` con y sin selector booleano, E/S con `fmt` y expresiones aritméticas/relacionales/lógicas con precedencia jerárquica).
   - Recuperación de errores en modo pánico a nivel de bloque (`error fin_opc`) y detección de fin de archivo inesperado (`p_error`), registrando las reglas gramaticales reconocidas y diagnosticando errores sintácticos con línea y columna exactas.
3. **Analizador Semántico (`src/semantic.py`):**
   - Construcción de una **Tabla de Símbolos jerárquica** (`TablaSimbolos`) con pila de ámbitos léxicos (`global`, `funcion`, `bloque`) y registro de mutabilidad, categoría, tipo de dato y línea de declaración.
   - Verificación de 6 Reglas Semánticas oficiales clasificadas por categoría:
     - **`identificadores`:** declaración previa obligatoria, indexación válida y acceso a campos de `struct` (**RS-1**), además de unicidad dentro del mismo alcance (**RS-2**).
     - **`asignación de tipo`:** compatibilidad estricta de tipos sin coerción implícita `int`/`float64`, inferencia segura, inmutabilidad de constantes `const` y validación en colecciones/`struct_init` (**RS-3**).
     - **`operaciones permitidas`:** coherencia estricta en operadores aritméticos, relacionales, lógicos, unarios y `++`/`--` (**RS-4**).
     - **`retorno de funciones` y `estructuras de control`:** concordancia de argumentos y tipo/existencia de `return` (**RS-5**), condiciones booleanas, iteración `for ... range`, `switch` y saltos `break`/`continue`/`fallthrough` (**RS-6**).
   - Formato estándar de diagnóstico: `Error Semántico <Categoría> en la línea <N>: <Mensaje descriptivo>.`.
4. **Interfaz Gráfica Interactiva (`CustomTkinter`):**
   - Diseño en modo oscuro (Dark Mode) tipo IDE bajo principios de Interacción Humano-Computador (IHC).
   - Editor de código fuente con numeración dinámica de líneas, carga de archivos `.go`, resaltado de sintaxis y marcado visual de líneas con error.
   - Panel de diagnóstico con botones individuales (`Léxico`, `Sintáctico`, `Semántico`) y ejecución encadenada (`▶ Ejecutar Todo`), Banner de Estado semafórico (`[EN ESPERA]`, `[VÁLIDO]`, `[ERROR LÉXICO]`, `[ERROR SINTÁCTICO]`, `[ERROR SEMÁNTICO]`), pestañas por fase (`Tabla de Tokens`, `Reglas Sintácticas` y `Tabla de Símbolos`) y Consola de Diagnóstico general.
5. **Contribución Individual y Trazabilidad en Git:**
   - Cada integrante contribuye con sus componentes asignados dentro de bloques delimitados por comentarios (`# INICIO APORTE` / `# FIN APORTE`) en `src/lexer.py`, `src/parser.py`, `src/semantic.py` y los módulos de `src/gui/`.
   - Cada integrante registra commits e historial de pruebas bajo su propio usuario Git.
6. **Algoritmos de Validación en Go:**
   - Algoritmos de validación léxica (`algoritmo1.go`, `algoritmo1_error.go`, `algoritmo2.go`, `algoritmo2_error.go`, `algoritmo3.go`, `algoritmo3_error.go`), sintáctica (`algoritmo{1,2,3}_sintactico.go` y `algoritmo{1,2,3}_error_sintactico.go`) y semántica (`algoritmo{1,2,3}_semantico.go` y `algoritmo{1,2,3}_error_semantico.go`).
7. **Generación Automatizada de Logs:**
   - Cada ejecución del analizador (desde la GUI o CLI) genera reportes automáticos en la carpeta `logs/`:
     - Léxico: `lexico-<NombreApellido>-<DD>-<MM>-<YYYY>-<HH>h<MM>.txt`
     - Sintáctico: `sintactico-<usuarioGit>-<DDMMYYYY>-<HH>h<MM>.txt`
     - Semántico: `semantico-<usuarioGit>-<DDMMYYYY>-<HH>h<MM>.txt`

---

## 📂 Arquitectura del Repositorio

La estructura modular del proyecto organiza la separación de responsabilidades para facilitar el trabajo colaborativo en equipo:

```text
LP-Proyecto_Parcial/
│
├── algoritmos/                           # Casos de prueba escritos en el subconjunto de Go (.go)
│   ├── algoritmo1.go                     # Validación léxica válida - Pablo Naranjo
│   ├── algoritmo1_error.go               # Validación con errores léxicos - Pablo Naranjo
│   ├── algoritmo1_sintactico.go          # Validación sintáctica válida - Pablo Naranjo
│   ├── algoritmo1_error_sintactico.go    # Validación con errores sintácticos - Pablo Naranjo
│   ├── algoritmo1_semantico.go           # Validación semántica válida - Pablo Naranjo
│   ├── algoritmo1_error_semantico.go     # Validación con errores semánticos - Pablo Naranjo
│   ├── algoritmo2.go                     # Validación léxica - Hivor Araujo
│   ├── algoritmo2_error.go               # Caso de prueba con error léxico - Hivor Araujo
│   ├── algoritmo_general_hivor_valido.go # Validación general válida - Hivor Araujo
│   ├── algoritmo_hivor_practica_errores.go # Práctica con errores - Hivor Araujo
│   ├── algoritmo2_sintactico.go          # Validación sintáctica válida - Hivor Araujo
│   ├── algoritmo2_error_sintactico.go    # Validación con errores sintácticos - Hivor Araujo
│   ├── algoritmo2_semantico.go           # Validación semántica válida - Hivor Araujo
│   ├── algoritmo2_error_semantico.go     # Validación con errores semánticos - Hivor Araujo
│   ├── algoritmo3.go                     # Validación léxica válida - Josué Pacheco
│   ├── algoritmo3_error.go               # Validación con errores léxicos - Josué Pacheco
│   ├── algoritmo3_sintactico.go          # Validación sintáctica válida - Josué Pacheco
│   ├── algoritmo3_error_sintactico.go    # Validación con errores sintácticos - Josué Pacheco
│   ├── algoritmo3_semantico.go           # Validación semántica válida - Josué Pacheco
│   └── algoritmo3_error_semantico.go     # Validación con errores semánticos - Josué Pacheco
│
├── logs/                                 # Registros de ejecución generados automáticamente (.txt)
│   ├── lexico-NombreApellido-DD-MM-YYYY-HHhMM.txt
│   ├── sintactico-usuarioGit-DDMMYYYY-HHhMM.txt
│   └── semantico-usuarioGit-DDMMYYYY-HHhMM.txt
│
├── src/                                  # Código fuente del compilador y la GUI en Python
│   ├── __init__.py
│   ├── lexer.py                          # Analizador léxico implementado con PLY (ply.lex)
│   ├── parser.py                         # Analizador sintáctico LALR(1) implementado con PLY (ply.yacc)
│   ├── semantic.py                       # Analizador semántico, TablaSimbolos jerárquica y reglas RS-1..RS-6
│   └── gui/                              # Paquete modular de la Interfaz Gráfica (CustomTkinter)
│       ├── __init__.py                   # Exportación de GoAnalyzerApp y launch_gui
│       ├── app.py                        # Ventana principal, barra de herramientas y estado inferior
│       ├── editor_panel.py               # Panel izquierdo: editor Go, números de línea y carga .go
│       ├── diagnostics_panel.py          # Panel derecho: banner de estado, pestañas y consola de diagnóstico
│       ├── log_exporter.py               # Integración con lexer/parser/semantic y exportación de logs
│       └── theme.py                      # Paleta de colores Dark Mode, tipografía y formato de tokens
│
├── README.md                             # Documentación general y arquitectura del proyecto
├── main.py                               # Punto de entrada principal (lanza la GUI o modo --cli)
└── requirements.txt                      # Dependencias externas (ply, customtkinter)
```

---

## ⚙️ Preparación del Entorno de Desarrollo

Se requiere **Python 3.10** o superior instalado en el sistema.

### 1. Clonar el Repositorio
```powershell
git clone https://github.com/PabloNaranjoM/LP-Proyecto_Parcial.git
cd LP-Proyecto_Parcial
```

### 2. Creación y Activación del Entorno Virtual

#### En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*(Si PowerShell bloquea la ejecución de scripts, ejecutar temporalmente: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*.

#### En Linux o macOS (Bash/Zsh):
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalación de Dependencias
Con el entorno virtual activo, instale las librerías requeridas (`ply` y `customtkinter`):
```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución de la Aplicación

### Interfaz Gráfica de Usuario (GUI - Modo Predeterminado)
Para iniciar la interfaz gráfica interactiva en **CustomTkinter**:
```powershell
python main.py
```
Opcionalmente puede indicar qué archivo `.go` cargar inicialmente en el editor:
```powershell
python main.py algoritmos/algoritmo2.go
```

### Modo Consola (CLI Opcional)
Si desea ejecutar los análisis léxico, sintáctico y semántico directamente desde la terminal y generar sus reportes en `logs/` (`--fase todo` por defecto):
```powershell
python main.py algoritmos/algoritmo1_semantico.go PabloNaranjoM --cli
```
También puede especificar una fase individual mediante `--fase {lexico,sintactico,semantico,todo}`:
```powershell
python main.py algoritmos/algoritmo1_semantico.go PabloNaranjoM --cli --fase semantico
```

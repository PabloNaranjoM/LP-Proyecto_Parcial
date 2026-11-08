# Compilador para Subconjunto de Go (ESPOL)

Analizador Léxico, Sintáctico y Semántico para un subconjunto del lenguaje de programación **Go**, desarrollado en **Python 3** mediante la herramienta de análisis léxico y sintáctico **PLY (`ply.lex` y `ply.yacc`)**, complementado con una interfaz gráfica moderna e interactiva implementada en **CustomTkinter**.

Este proyecto corresponde al desarrollo práctico de la materia **Lenguajes de Programación** de la Escuela Superior Politécnica del Litoral (**ESPOL**), bajo la dirección del profesor Ing. Rodrigo Saraguro.

---

## 👥 Equipo de Desarrollo

| Integrante | Rol / Usuario GitHub | Módulos Asignados (Avances 1 y 2 - Léxico, Sintáctico y GUI) |
| :--- | :--- | :--- |
| **Pablo Naranjo** | `@PabloNaranjoM` | **Léxico (`src/lexer.py`):** Palabras reservadas `ESTRUCTURA` (`struct`) y `MAPA` (`map`), paquetes/E/S (`PAQUETE_FMT`, `IMPRIMIR_LN`, `IMPRIMIR`, `LEER_LN`, `LEER`), tipos numéricos (`TIPO_ENTERO`, `TIPO_FLOTANTE`), literales (`LITERAL_FLOTANTE`, `LITERAL_CADENA`), asignación corta (`DOS_PUNTOS_IGUAL`), asignaciones compuestas (`MAS_IGUAL`, `MENOS_IGUAL`, `POR_IGUAL`, `DIV_IGUAL`, `MOD_IGUAL`), incremento/decremento (`INCREMENTO`, `DECREMENTO`), comentarios, delimitadores (`DOS_PUNTOS`, `PUNTO_COMA`, `AMPERSAND`, `ELIPSIS`), manejador `t_error` y `build_lexer()`.<br>**Sintáctico (`src/parser.py`):** Infraestructura del parser LALR(1) y tabla de precedencia, declaraciones cortas (`:=`), estructuras (`type ... struct`) e instanciación compuesta, entrada estándar (`fmt.Scanln`, `fmt.Scan`), bucle `for` en sus 4 variantes (`while`, clásico, infinito y `for ... range`), comparaciones (`>`, `<`, `>=`, `<=`), división/módulo, recuperación de errores (`p_error`) y fachada `analizar_sintaxis()`.<br>**GUI y Logs (`src/gui/app.py`, `src/gui/log_exporter.py`, `src/gui/diagnostics_panel.py`):** Orquestación PLY + CustomTkinter (`Léxico`, `Sintáctico`, `▶ Ejecutar Todo`), Banner de Estado (`VÁLIDO` / `ERROR`) y exportación automatizada de logs.<br>**Algoritmos de prueba:** `algoritmos/algoritmo1.go`, `algoritmo1_sintactico.go`, `algoritmo1_error_sintactico.go`. |
| **Hivor Araujo** | `@AraujoHivor` | **Léxico (`src/lexer.py`):** Palabras reservadas principales de Go en español (`PAQUETE`, `IMPORTAR`, `FUNCION`, `VARIABLE`, `CONSTANTE`, `RETORNAR`, `SI`, `SINO`, `PARA`, `RANGO`, `SEGUN`, `CASO`, `DEFECTO`, `ROMPER`, `CONTINUAR`, `CAIDA`, `TIPO`, `INTERFAZ`, `IR`, `CANAL`, `SELECCIONAR`, `DIFERIR`, `IR_A`), operadores aritméticos (`MAS`, `MENOS`, `MULTIPLICACION`, `DIVISION`, `MODULO`), asignación simple (`ASIGNACION`), delimitadores de agrupación (`()`, `{}`, `[]`), identificadores (`ID`), `TIPO_CADENA` y `LITERAL_ENTERO`.<br>**Sintáctico (`src/parser.py`):** Regla inicial del programa (`package`, `import`, declaraciones globales y `func`), declaración explícita de variables (`var`) y constantes (`const`), tipos compuestos (`[]T`, `[N]T`, `map[K]V`), arreglos e indexación (`arr[i]`), condicional `if / else / else if`, salida con salto (`fmt.Println`), asignación simple (`=`) y operaciones de suma, resta y multiplicación.<br>**GUI (`src/gui/editor_panel.py`, `src/gui/app.py`):** Panel de edición de código Go con numeración dinámica de líneas sincronizada, resaltado de sintaxis y líneas de error, carga de archivos `.go` y botón `Limpiar`.<br>**Algoritmos de prueba:** `algoritmos/algoritmo2.go`, `algoritmo2_error.go`, `algoritmo2_sintactico.go`, `algoritmo2_error_sintactico.go`. |
| **Josué Pacheco** | `@JosuePach3co` | **Léxico (`src/lexer.py`):** Tipo predefinido `TIPO_BOOLEANO` (`bool`), literales booleanos (`VERDADERO`, `FALSO`), operadores relacionales (`IGUAL_IGUAL`, `DIFERENTE`, `MENOR_QUE`, `MAYOR_QUE`, `MENOR_IGUAL`, `MAYOR_IGUAL`), operadores lógicos (`Y_LOGICO`, `O_LOGICO`, `NEGACION`), delimitadores (`PUNTO`, `COMA`), descarte de espacios (`t_ignore`) y seguimiento de saltos de línea (`t_newline`).<br>**Sintáctico (`src/parser.py`):** Definición e invocación de funciones con parámetros y retorno múltiple, estructura selectiva `switch / case / default`, salida estándar sin salto (`fmt.Print`), asignaciones compuestas (`+=`, `-=`, `*=`, `/=`, `%=`), incremento/decremento (`++`, `--`), sentencias de salto (`return`, `break`, `continue`), operadores de igualdad (`==`, `!=`), expresiones lógicas (`&&`, `\|\|`, `!`) y acceso a campos (`.`).<br>**GUI (`src/gui/diagnostics_panel.py`, `src/gui/theme.py`):** Panel derecho con pestañas (`Tabla de Tokens`, `Reglas Sintácticas` y `Tabla de Símbolos`) y consola de diagnóstico con visualización de línea y columna exacta.<br>**Algoritmos de prueba:** `algoritmos/algoritmo3.go`, `algoritmo3_sintactico.go`, `algoritmo3_error_sintactico.go`. |

---

## 📌 Especificaciones e Instrucciones (Avances 1 y 2)

Conforme a las indicaciones oficiales provistas por el docente:

1. **Analizador Léxico (`ply.lex` - `src/lexer.py`):**
   - Definición formal de componentes léxicos con nombres de tokens 100% estandarizados al español, incluyendo reconocimiento dedicado para `fmt` (`PAQUETE_FMT`) y funciones de E/S (`IMPRIMIR_LN`, `IMPRIMIR`, `LEER_LN`, `LEER`).
   - Manejo y recuperación ante errores léxicos (`t_error`), registrando caracteres ilegales y la línea/columna exacta.
2. **Analizador Sintáctico (`ply.yacc` - `src/parser.py`):**
   - Gramática Libre de Contexto LALR(1) libre de conflictos *shift/reduce* y *reduce/reduce* para el subconjunto de Go (declaraciones `var`/`const`/`:=`, funciones con múltiples retornos, estructuras `struct`, arreglos, *slices*, mapas, `if/else`, `for` en sus 4 variantes, `switch/case/default`, E/S con `fmt` y expresiones aritméticas/relacionales/lógicas con precedencia formal).
   - Recuperación de errores en modo pánico a nivel de bloque y tope de archivo (`p_error`), registrando las reglas gramaticales reconocidas y diagnosticando errores sintácticos con línea y columna exactas.
3. **Interfaz Gráfica Interactiva (`CustomTkinter`):**
   - Diseño en modo oscuro (Dark Mode) tipo IDE bajo principios de Interacción Humano-Computador (IHC).
   - Editor de código fuente con numeración dinámica de líneas, carga de archivos `.go`, resaltado de sintaxis y marcado visual de líneas con error.
   - Panel de diagnóstico con Banner de Estado semafórico, pestañas por fase (`Tabla de Tokens`, `Reglas Sintácticas` y `Tabla de Símbolos`) y Consola de Diagnóstico general.
4. **Contribución Individual y Trazabilidad en Git:**
   - Cada integrante contribuye con sus componentes asignados dentro de bloques delimitados por comentarios (`# INICIO APORTE` / `# FIN APORTE`) en `src/lexer.py`, `src/parser.py` y los módulos de `src/gui/`.
   - Cada integrante registra commits e historial de pruebas bajo su propio usuario Git.
5. **Algoritmos de Validación en Go:**
   - Algoritmos de validación léxica (`algoritmo1.go`, `algoritmo2.go`, `algoritmo2_error.go`, `algoritmo3.go`) y validación sintáctica con casos válidos y con errores sintácticos intencionales (`algoritmo{1,2,3}_sintactico.go` y `algoritmo{1,2,3}_error_sintactico.go`).
6. **Generación Automatizada de Logs:**
   - Cada ejecución del analizador (desde la GUI o CLI) genera reportes automáticos en la carpeta `logs/`:
     - Léxico: `lexico-<NombreApellido>-<DD>-<MM>-<YYYY>-<HH>h<MM>.txt`
     - Sintáctico: `sintactico-<usuarioGit>-<DDMMYYYY>-<HH>h<MM>.txt`

---

## 📂 Arquitectura del Repositorio

La estructura modular del proyecto organiza la separación de responsabilidades para facilitar el trabajo colaborativo en equipo:

```text
LP-Proyecto_Parcial/
│
├── algoritmos/                           # Casos de prueba escritos en el subconjunto de Go (.go)
│   ├── algoritmo1.go                     # Validación léxica - Pablo Naranjo
│   ├── algoritmo1_sintactico.go          # Validación sintáctica válida - Pablo Naranjo
│   ├── algoritmo1_error_sintactico.go    # Validación con errores sintácticos - Pablo Naranjo
│   ├── algoritmo2.go                     # Validación léxica - Hivor Araujo
│   ├── algoritmo2_error.go               # Caso de prueba con error léxico - Hivor Araujo
│   ├── algoritmo2_sintactico.go          # Validación sintáctica válida - Hivor Araujo
│   ├── algoritmo2_error_sintactico.go    # Validación con errores sintácticos - Hivor Araujo
│   ├── algoritmo3.go                     # Validación léxica - Josué Pacheco
│   ├── algoritmo3_sintactico.go          # Validación sintáctica válida - Josué Pacheco
│   └── algoritmo3_error_sintactico.go    # Validación con errores sintácticos - Josué Pacheco
│
├── docs/                                 # Documentación técnica y especificaciones de diseño
│   ├── [OBSERVACIONES] Avance 1.txt
│   ├── especificaci_n_de_dise_o_de_la_gui.md
│   ├── Instrucciones avance 1.txt
│   ├── Propuesta primera hoja de ruta.pdf
│   └── Proyecto_LP_Parcial_2026_II (APROBADO-EN REDACCIÓN).pdf
│
├── logs/                                 # Registros de ejecución generados automáticamente (.txt)
│   ├── lexico-NombreApellido-DD-MM-YYYY-HHhMM.txt
│   └── sintactico-usuarioGit-DDMMYYYY-HHhMM.txt
│
├── src/                                  # Código fuente del compilador y la GUI en Python
│   ├── __init__.py
│   ├── lexer.py                          # Analizador léxico implementado con PLY (ply.lex)
│   ├── parser.py                         # Analizador sintáctico LALR(1) implementado con PLY (ply.yacc)
│   └── gui/                              # Paquete modular de la Interfaz Gráfica (CustomTkinter)
│       ├── __init__.py                   # Exportación de GoAnalyzerApp y launch_gui
│       ├── app.py                        # Ventana principal, barra de herramientas y estado inferior
│       ├── editor_panel.py               # Panel izquierdo: editor Go, números de línea y carga .go
│       ├── diagnostics_panel.py          # Panel derecho: banner de estado, pestañas y consola de diagnóstico
│       ├── log_exporter.py               # Integración con lexer/parser y exportación automática de logs
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
Si desea ejecutar tanto el análisis léxico como el sintáctico directamente desde la terminal y generar sus reportes en `logs/` (`--fase todo` por defecto):
```powershell
python main.py algoritmos/algoritmo1_sintactico.go PabloNaranjoM --cli
```
También puede especificar una fase individual mediante `--fase {lexico,sintactico,todo}`:
```powershell
python main.py algoritmos/algoritmo1_sintactico.go PabloNaranjoM --cli --fase sintactico
```

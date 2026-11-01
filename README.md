# Compilador para Subconjunto de Go (ESPOL)

Analizador Léxico, Sintáctico y Semántico para un subconjunto del lenguaje de programación **Go**, desarrollado en **Python 3** mediante la herramienta de análisis léxico y sintáctico **PLY (`ply.lex` y `ply.yacc`)**, complementado con una interfaz gráfica moderna e interactiva implementada en **CustomTkinter**.

Este proyecto corresponde al desarrollo práctico de la materia **Lenguajes de Programación** de la Escuela Superior Politécnica del Litoral (**ESPOL**), bajo la dirección del profesor Ing. Rodrigo Saraguro.

---

## 👥 Equipo de Desarrollo

| Integrante | Rol / Usuario GitHub | Módulos Asignados (Avance 1 - Léxico y GUI) |
| :--- | :--- | :--- |
| **Pablo Naranjo** | `@PabloNaranjoM` | **Léxico (`src/lexer.py`):** Palabras reservadas `struct` y `map`, tipos numéricos (`int`, `float64`), literales flotantes (`LITERAL_FLOAT`), literales de cadena con secuencias de escape (`LITERAL_STRING`), asignación corta (`:=`), asignaciones compuestas (`+=`, `-=`, `*=`, `/=`, `%=`), incremento/decremento (`++`, `--`), comentarios (`//`, `/* */`), delimitadores (`:`, `;`, `&`), manejador de errores léxicos (`t_error`) y función fábrica `build_lexer()`.<br>**GUI y Logs (`src/gui/app.py`, `src/gui/log_exporter.py`, `src/gui/diagnostics_panel.py`):** Integración del motor PLY con CustomTkinter, botones de ejecución (`Léxico`, `Sintáctico`, `Semántico`, `▶ Ejecutar Todo`), selector de desarrollador, Banner de Estado del Sistema (`VÁLIDO` / `ERROR`) y exportación automatizada de logs (`<analisis>-<desarrollador>-<fecha>-<hora>.txt`).<br>**Algoritmo de prueba:** `algoritmos/algoritmo1.go`. |
| **Hivor Araujo** | `@AraujoHivor` | **Léxico (`src/lexer.py`):** Palabras reservadas principales de Go (23 keywords: `package`, `import`, `func`, `var`, `const`, `return`, `if`, `else`, `for`, `range`, `switch`, `case`, `default`, `break`, `continue`, `fallthrough`, `type`, `interface`, `go`, `chan`, `select`, `defer`, `goto`), operadores aritméticos (`+`, `-`, `*`, `/`, `%`), asignación simple (`=`), delimitadores de agrupación (`()`, `{}`, `[]`), identificadores (`ID`), tipo predefinido `string` y literales enteros (`LITERAL_INT`).<br>**GUI (`src/gui/editor_panel.py`, `src/gui/app.py`):** Construcción del panel izquierdo de edición de código Go con numeración dinámica de líneas sincronizada, resaltado básico de sintaxis y líneas de error, carga de archivos `.go` y botón `Limpiar`.<br>**Algoritmo de prueba:** `algoritmos/algoritmo2.go`. |
| **Josué Pacheco** | `@JosuePach3co` | **Léxico (`src/lexer.py`):** Tipo predefinido `bool`, literales booleanos (`true`, `false`), operadores relacionales (`==`, `!=`, `<`, `>`, `<=`, `>=`), operadores lógicos (`&&`, `\|\|`, `!`), delimitadores (`.`, `,`), regla para descartar espacios en blanco y tabulaciones (`t_ignore`) y regla para seguimiento de saltos de línea (`t_newline`).<br>**GUI (`src/gui/diagnostics_panel.py`, `src/gui/theme.py`):** Construcción del panel derecho ordenado mediante pestañas (`Tabla de Tokens`, `Reglas Sintáticas` y `Tabla de Símbolos`) y consola general inferior con visualización de línea y columna exacta.<br>**Algoritmo de prueba:** `algoritmos/algoritmo3.go`. |

---

## 📌 Especificaciones e Instrucciones del Avance 1

Conforme a las indicaciones oficiales provistas por el docente para el primer entregable:

1. **Analizador Léxico (`ply.lex`):**
   - Definición formal de componentes léxicos (tokens, palabras reservadas, operadores, delimitadores y literales) para el subconjunto asignado de Go.
   - Manejo y recuperación ante errores léxicos (`t_error`), registrando caracteres ilegales y la línea/columna de ocurrencia.
2. **Interfaz Gráfica Interactiva (`CustomTkinter`):**
   - Diseño en modo oscuro (Dark Mode) tipo IDE bajo principios de Interacción Humano-Computador (IHC).
   - Editor de código fuente con numeración dinámica de líneas, carga de archivos `.go`, resaltado de sintaxis y marcado visual de líneas con error.
   - Panel de diagnóstico con Banner de Estado semafórico, pestañas por fase (`Tabla de Tokens`, `Reglas Sintáticas` y `Tabla de Símbolos`) y Consola de Diagnóstico general.
3. **Contribución Individual y Trazabilidad en Git:**
   - Cada integrante contribuye con sus componentes asignados dentro de bloques delimitados por comentarios (`# INICIO APORTE` / `# FIN APORTE`) tanto en `src/lexer.py` como en los módulos de `src/gui/`.
   - Cada integrante debe contar con commits registrados bajo su propio usuario Git (requisito indispensable de evaluación).
4. **Algoritmos de Validación en Go:**
   - Cada integrante diseña y sube su propio algoritmo de prueba con extensión `.go` dentro de `algoritmos/` (`algoritmo1.go`, `algoritmo2.go`, `algoritmo3.go`).
   - Los algoritmos incluyen tanto código representativo como errores léxicos intencionales para verificar la captura en el analizador.
5. **Generación Automatizada de Logs:**
   - Cada ejecución del analizador (desde la GUI o CLI) genera reportes automáticos en la carpeta `logs/`.
   - Nomenclatura estricta: `lexico-<NombreApellido>-<DD>-<MM>-<YYYY>-<HH>h<MM>.txt`.
   - Todos los logs generados se versionan en el repositorio como evidencia de prueba.

---

## 📂 Arquitectura del Repositorio

La estructura modular del proyecto organiza la separación de responsabilidades para facilitar el trabajo colaborativo en equipo:

```text
LP-Proyecto_Parcial/
│
├── algoritmos/                  # Casos de prueba escritos en el subconjunto de Go (.go)
│   ├── algoritmo1.go            # Algoritmo de validación - Pablo Naranjo
│   ├── algoritmo2.go            # Algoritmo de validación - Hivor Araujo
│   ├── algoritmo2_error.go      # Caso de prueba con error léxico - Hivor Araujo
│   └── algoritmo3.go            # Algoritmo de validación - Josué Pacheco
│
├── docs/                        # Documentación técnica y especificaciones de diseño
│   ├── especificaci_n_de_dise_o_de_la_gui.md
│   ├── Instrucciones avance 1.txt
│   ├── Propuesta primera hoja de ruta.pdf
│   └── Proyecto_LP_Parcial_2026_II (APROBADO-EN REDACCIÓN).pdf
│
├── logs/                        # Registros de ejecución generados automáticamente (.txt)
│   └── lexico-NombreApellido-DD-MM-YYYY-HHhMM.txt
│
├── src/                         # Código fuente del compilador y la GUI en Python
│   ├── __init__.py
│   ├── lexer.py                 # Analizador léxico implementado con PLY (ply.lex)
│   └── gui/                     # Paquete modular de la Interfaz Gráfica (CustomTkinter)
│       ├── __init__.py          # Exportación de GoAnalyzerApp y launch_gui
│       ├── app.py               # Ventana principal, barra de herramientas y estado inferior
│       ├── editor_panel.py      # Panel izquierdo: editor Go, números de línea y carga .go
│       ├── diagnostics_panel.py # Panel derecho: banner de estado, pestañas y consola de diagnóstico
│       ├── log_exporter.py      # Integración con lexer y exportación automática de logs
│       └── theme.py             # Paleta de colores Dark Mode, tipografía y formato de tokens
│
├── README.md                    # Documentación general y arquitectura del proyecto
├── main.py                      # Punto de entrada principal (lanza la GUI o modo --cli)
└── requirements.txt             # Dependencias externas (ply, customtkinter)
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
Si desea ejecutar el análisis léxico directamente desde la terminal y generar el log en `logs/`:
```powershell
python main.py algoritmos/algoritmo1.go PabloNaranjoM --cli
```

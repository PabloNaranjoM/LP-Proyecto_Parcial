# Guía de Contribución y Normas de Desarrollo

Este documento establece los estándares técnicos, flujos de trabajo colaborativos con Git y el contrato unificado de tokens para el desarrollo del compilador de un subconjunto del lenguaje **Go**, desarrollado en **Python 3** con la librería **PLY (`ply.lex` y `ply.yacc`)**.

El cumplimiento riguroso de estas directrices es indispensable para asegurar una integración fluida entre los integrantes del equipo y garantizar el cumplimiento de la rúbrica de evaluación docente establecida por el Ing. Rodrigo Saraguro.

---

## 1. Configuración Obligatoria de Git Antes del Primer Commit

> [!CAUTION]
> **Regla Crítica de Calificación (Profesor Rodrigo Saraguro):**
> Cada integrante debe contar con commits explícitos registrados bajo su propia cuenta en el historial del repositorio. Si un integrante no figura en los commits individuales de GitHub, **no recibirá calificación (0 puntos)** en el avance correspondiente.

Antes de realizar cualquier commit o modificación en su copia local, cada desarrollador debe verificar y configurar su identidad en Git con el **mismo correo electrónico asociado a su cuenta de GitHub**:

```powershell
# 1. Configurar nombre completo
git config user.name "Tu Nombre y Apellido"

# 2. Configurar correo electrónico exacto de GitHub
git config user.email "tu_correo_asociado_a_github@dominio.com"

# 3. Verificar que la configuración se aplicó correctamente
git config user.name
git config user.email
```

### Cuentas del Equipo de Desarrollo
| Integrante | Usuario de GitHub | Rama Asignada (Avance 1) | Archivo de Prueba |
| :--- | :--- | :--- | :--- |
| **Pablo Naranjo** | `@PabloNaranjoM` | `feat/lexico-pablo` | `algoritmos/algoritmo1.go` |
| **Hivor Araujo** | `@AraujoHivor` | `feat/lexico-hivor` | `algoritmos/algoritmo2.go` |
| **Josué Pacheco** | `@JosuePach3co` | `feat/lexico-josue` | `algoritmos/algoritmo3.go` |

---

## 2. Flujo de Ramas, Commits e Integración

### 2.1 Estrategia de Ramas (Git Feature Branch)
- La rama `main` almacena el código estable y validado. Queda estrictamente prohibido realizar `git push` directo a `main`.
- Para el **Avance 1 (Léxico)**, cada desarrollador debe trabajar exclusivamente sobre su rama designada:
  - `feat/lexico-pablo`
  - `feat/lexico-hivor`
  - `feat/lexico-josue`
- Las ramas se desprenden de `main` actualizado:
  ```powershell
  git checkout main
  git pull origin main
  git checkout -b feat/lexico-[tu-nombre]
  ```

### 2.2 Delimitación Estricta de Aportes en Código Fuente
En los módulos colaborativos, en particular dentro del archivo [`src/lexer.py`](./src/lexer.py), cada integrante debe programar **únicamente** dentro de sus bloques delimitados por comentarios con el formato exacto estandarizado:

```python
# =====================================================================
# INICIO APORTE: Nombre Apellido (@UsuarioGitHub)
# =====================================================================

# [Tokens, definiciones de expresiones regulares y funciones asignadas]

# =====================================================================
# FIN APORTE: Nombre Apellido (@UsuarioGitHub)
# =====================================================================
```

> [!WARNING]
> No altere, mueva ni elimine el código o comentarios ubicados fuera de su bloque de aporte asignado sin previo consenso del equipo.

### 2.3 Convención de Mensajes de Commit
Adoptamos el estándar **Conventional Commits**, redactados en español técnico y utilizando verbos en **modo imperativo** (e.g., *agrega*, *corrige*, *actualiza*, *documenta*):

- **Estructura:** `<tipo>(<alcance>): <descripción imperativa>`
- **Tipos permitidos:**
  - `feat`: Nueva característica o definición de tokens (e.g., `feat(lexico): agrega tokens de operadores relacionales y logicos`).
  - `fix`: Corrección de errores en expresiones regulares o precedencias (e.g., `fix(lexico): corrige patron de literales flotantes`).
  - `docs`: Modificaciones en documentación o comentarios (e.g., `docs: detalla contrato de tokens en CONTRIBUTING.md`).
  - `test`: Incorporación o ajuste de algoritmos de prueba (e.g., `test(lexico): agrega algoritmo1.go con casos de prueba y errores deliberados`).
  - `refactor`: Reorganización de código sin alterar su comportamiento léxico.

### 2.4 Regla Crítica en Pull Requests: Prohibido Squash and Merge
Al momento de integrar los cambios de una rama de característica hacia `main` mediante Pull Request en GitHub:

> [!CAUTION]
> **USAR EXCLUSIVAMENTE "Create a merge commit" (`--no-ff`).**
> **ESTÁ TOTALMENTE PROHIBIDO UTILIZAR "Squash and merge" O "Rebase and merge".**
> 
> *Razón técnica:* El *Squash and merge* colapsa todos los commits individuales de la rama en un único commit cuyo autor visible suele ser solo quien presiona el botón o aprueba el PR. Esto borraría los commits individuales de los integrantes en `main`, arriesgando la pérdida de autoría y la calificación de **0 puntos**.

```powershell
# Simulación local del comportamiento requerido (Merge no fast-forward):
git checkout main
git merge --no-ff feat/lexico-[nombre]
```

### 2.5 Orden Sugerido de Prueba e Integración en `ply.lex`
El archivo [`src/lexer.py`](./src/lexer.py) en la rama `main` parte como un **esqueleto con 0% de lógica implementada** (solo marcadores `TODO` estructurales). En PLY, invocar `lex.lex()` requiere obligatoriamente al menos una regla de token y el manejador de errores `t_error` para compilar sin arrojar excepciones.

Dado que `t_error` y la función fábrica `build_lexer()` están asignados a **Pablo Naranjo** (`feat/lexico-pablo`):

1. **Orden de Integración Recomendado en `main`:**
   - **Paso 1 (`feat/lexico-pablo`):** Integrar primero esta rama, ya que aporta el manejador de errores léxicos `t_error`, el constructor `build_lexer()`, el exportador CLI en `main.py`, los comentarios (`//`, `/* */`) y las reglas complejas de flotantes y cadenas.
   - **Paso 2 (`feat/lexico-hivor`):** Integrar la base de identificadores (`t_ID`), las 23 palabras reservadas, literales enteros y operadores aritméticos sobre la base ya funcional de `main`.
   - **Paso 3 (`feat/lexico-josue`):** Integrar operadores relacionales, conectores lógicos, booleanos, delimitadores y reglas de utilidad (`t_ignore`, `t_newline`).

2. **Pruebas Locales Aisladas en Ramas Paralelas:**
   - Si un integrante necesita ejecutar `lex.lex()` localmente en su rama antes de que `feat/lexico-pablo` haya sido mergeado en `main`, puede definir temporalmente un manejador dummy `def t_error(t): t.lexer.skip(1)` **únicamente para sus pruebas locales**, asegurándose de **remover cualquier código fuera de su bloque delimitado antes de realizar su commit y solicitar el Pull Request**.

---

## 3. Contrato de Nombres de Tokens

Para que el **Avance 2 (Analizador Sintáctico con `ply.yacc`)** encaje directamente sin necesidad de reescribir ni renombrar tokens, todos los nombres deben seguir de forma estricta la nomenclatura en **MAYÚSCULAS** alineada con las reglas gramaticales BNF del documento de propuesta técnica aprobado.

### 3.1 Palabras Reservadas (25 Keywords Oficiales de Go)
Las 25 palabras reservadas se estandarizan con su nombre literal en mayúsculas y son detectadas a través del diccionario `KEYWORDS_MAP` dentro de la regla de identificadores `t_ID`:

| Palabra Reservada (Go) | Nombre del Token | Integrante Responsable | Mapeo en Código |
| :--- | :--- | :--- | :--- |
| `package` | `PACKAGE` | Hivor Araujo | `keywords_hivor` |
| `import` | `IMPORT` | Hivor Araujo | `keywords_hivor` |
| `func` | `FUNC` | Hivor Araujo | `keywords_hivor` |
| `var` | `VAR` | Hivor Araujo | `keywords_hivor` |
| `const` | `CONST` | Hivor Araujo | `keywords_hivor` |
| `return` | `RETURN` | Hivor Araujo | `keywords_hivor` |
| `if` | `IF` | Hivor Araujo | `keywords_hivor` |
| `else` | `ELSE` | Hivor Araujo | `keywords_hivor` |
| `for` | `FOR` | Hivor Araujo | `keywords_hivor` |
| `range` | `RANGE` | Hivor Araujo | `keywords_hivor` |
| `switch` | `SWITCH` | Hivor Araujo | `keywords_hivor` |
| `case` | `CASE` | Hivor Araujo | `keywords_hivor` |
| `default` | `DEFAULT` | Hivor Araujo | `keywords_hivor` |
| `break` | `BREAK` | Hivor Araujo | `keywords_hivor` |
| `continue` | `CONTINUE` | Hivor Araujo | `keywords_hivor` |
| `fallthrough` | `FALLTHROUGH` | Hivor Araujo | `keywords_hivor` |
| `type` | `TYPE` | Hivor Araujo | `keywords_hivor` |
| `interface` | `INTERFACE` | Hivor Araujo | `keywords_hivor` |
| `go` | `GO` | Hivor Araujo | `keywords_hivor` |
| `chan` | `CHAN` | Hivor Araujo | `keywords_hivor` |
| `select` | `SELECT` | Hivor Araujo | `keywords_hivor` |
| `defer` | `DEFER` | Hivor Araujo | `keywords_hivor` |
| `goto` | `GOTO` | Hivor Araujo | `keywords_hivor` |
| `struct` | `STRUCT` | Pablo Naranjo | `keywords_pablo` |
| `map` | `MAP` | Pablo Naranjo | `keywords_pablo` |

### 3.2 Tipos de Datos Básicos Predefinidos (Mapeados en `KEYWORDS_MAP`)
Para evitar colisiones de nombres con los literales y facilitar la construcción sintáctica en `ply.yacc`, los tipos de datos primitivos se registran como tokens diferenciados mediante prefijo `TIPO_`:

| Tipo en Go | Token Estandarizado | Integrante Responsable | Mapeo en Código |
| :--- | :--- | :--- | :--- |
| `int` | `TIPO_INT` | Pablo Naranjo | `keywords_pablo` |
| `float64` | `TIPO_FLOAT64` | Pablo Naranjo | `keywords_pablo` |
| `string` | `TIPO_STRING` | Hivor Araujo | `keywords_hivor` |
| `bool` | `TIPO_BOOL` | Josué Pacheco | `keywords_josue` |

### 3.3 Literales e Identificadores
| Categoría / Lexema | Token Estandarizado | Integrante Responsable | Implementación | Ejemplos |
| :--- | :--- | :--- | :--- | :--- |
| Identificador | `ID` | Hivor Araujo | Regla `def t_ID(t)` con consulta a `KEYWORDS_MAP` | `contador`, `calcularSuma`, `total_items` |
| Literal Entero | `LITERAL_INT` | Hivor Araujo | Regla de función o regex numérico decimal | `0`, `42`, `1000` |
| Literal Flotante | `LITERAL_FLOAT` | Pablo Naranjo | Regla `def t_LITERAL_FLOAT(t)` con mayor precedencia | `3.1416`, `0.75`, `1.0e-3` |
| Literal Cadena | `LITERAL_STRING` | Pablo Naranjo | Regla para cadenas delimitadas por comillas dobles | `"Hola ESPOL"`, `"Resultado: %d\n"` |
| Booleano Verdadero | `TRUE` | Josué Pacheco | Palabra reservada en `keywords_josue` (`true`) | `true` |
| Booleano Falso | `FALSE` | Josué Pacheco | Palabra reservada en `keywords_josue` (`false`) | `false` |

### 3.4 Operadores
| Operador | Token Estandarizado | Integrante Responsable | Descripción |
| :---: | :--- | :--- | :--- |
| `+` | `SUMA` | Hivor Araujo | Operador aritmético de suma |
| `-` | `RESTA` | Hivor Araujo | Operador aritmético de resta / unario negativo |
| `*` | `MULT` | Hivor Araujo | Operador aritmético de multiplicación / dereferencia |
| `/` | `DIV` | Hivor Araujo | Operador aritmético de división entera o flotante |
| `%` | `MOD` | Hivor Araujo | Operador aritmético de módulo (resto) |
| `=` | `ASIGNACION` | Hivor Araujo | Operador de asignación simple |
| `:=` | `ASIGNACION_CORTA` | Pablo Naranjo | Declaración y asignación corta de Go |
| `+=` | `MAS_IGUAL` | Pablo Naranjo | Asignación con suma compuesta |
| `-=` | `MENOS_IGUAL` | Pablo Naranjo | Asignación con resta compuesta |
| `*=` | `MULT_IGUAL` | Pablo Naranjo | Asignación con producto compuesto |
| `/=` | `DIV_IGUAL` | Pablo Naranjo | Asignación con división compuesta |
| `%=` | `MOD_IGUAL` | Pablo Naranjo | Asignación con módulo compuesto |
| `++` | `INCREMENTO` | Pablo Naranjo | Operador post-incremento |
| `--` | `DECREMENTO` | Pablo Naranjo | Operador post-decremento |
| `==` | `IGUAL_IGUAL` | Josué Pacheco | Comparación relacional de igualdad |
| `!=` | `DIFERENTE` | Josué Pacheco | Comparación relacional de desigualdad |
| `<` | `MENOR` | Josué Pacheco | Comparación menor que |
| `>` | `MAYOR` | Josué Pacheco | Comparación mayor que |
| `<=` | `MENOR_IGUAL` | Josué Pacheco | Comparación menor o igual que |
| `>=` | `MAYOR_IGUAL` | Josué Pacheco | Comparación mayor o igual que |
| `&&` | `AND` | Josué Pacheco | Operador lógico de conjunción (Y lógico) |
| `\|\|` | `OR` | Josué Pacheco | Operador lógico de disyunción (O lógico) |
| `!` | `NOT` | Josué Pacheco | Operador unario de negación lógica |

### 3.5 Delimitadores y Puntuadores
| Símbolo | Token Estandarizado | Integrante Responsable | Descripción |
| :---: | :--- | :--- | :--- |
| `(` | `PAR_IZQ` | Hivor Araujo | Paréntesis de apertura |
| `)` | `PAR_DER` | Hivor Araujo | Paréntesis de cierre |
| `{` | `LLAVE_IZQ` | Hivor Araujo | Llave de apertura (bloques de código) |
| `}` | `LLAVE_DER` | Hivor Araujo | Llave de cierre |
| `[` | `CORCHETE_IZQ` | Hivor Araujo | Corchete de apertura (arreglos e indexación) |
| `]` | `CORCHETE_DER` | Hivor Araujo | Corchete de cierre |
| `,` | `COMA` | Josué Pacheco | Separador de elementos y parámetros |
| `.` | `PUNTO` | Josué Pacheco | Acceso a miembros de estructuras o paquetes |
| `:` | `DOS_PUNTOS` | Pablo Naranjo | Separador en `case`, `slice` o pares de mapa |
| `;` | `PUNTO_COMA` | Pablo Naranjo | Terminador de sentencia explícito |
| `&` | `AMPERSAND` | Pablo Naranjo | Operador de dirección de memoria / bitwise AND |

---

## 4. Reglas Técnicas de `ply.lex` para Prevenir Errores Comunes

### 4.1 Prioridad de Funciones frente a Cadenas Simples
En PLY, las reglas léxicas definidas mediante funciones (`def t_TOKEN(t):`) son evaluadas **antes** que las definidas mediante cadenas simples de expresiones regulares (`t_TOKEN = r'...'`), y respetan estrictamente el orden en que aparecen en el código fuente.
- **Caso Crítico:** La regla `t_LITERAL_FLOAT` debe definirse mediante una función `def t_LITERAL_FLOAT(t):` y ubicarse **antes** de `t_LITERAL_INT`. De lo contrario, una entrada como `3.14` sería leída erróneamente como un token `LITERAL_INT` con valor `3`, seguido de `PUNTO` (`.`) y otro `LITERAL_INT` con valor `14`.

### 4.2 Prohibido Definir Palabras Clave como Cadenas `t_... = r'...'`
No defina palabras reservadas como tokens directos independientes (por ejemplo, evitar `t_VAR = r'var'`). Si se hiciera esto, cualquier identificador que inicie con esa subcadena (e.g., `variable`, `varianza`, `formato`) se rompería en tokens no deseados.
- **Forma correcta (Estándar PLY):**
  Definir la regla de identificadores `t_ID` con la expresión regular `r'[a-zA-Z_][a-zA-Z0-9_]*'`. Dentro de `t_ID`, consultar el diccionario unificado `KEYWORDS_MAP`:
  ```python
  def t_ID(t):
      r'[a-zA-Z_][a-zA-Z0-9_]*'
      t.type = KEYWORDS_MAP.get(t.value, 'ID')
      return t
  ```

### 4.3 Arreglos (`[n]T`) y Slices (`[]T`) son Estructuras Sintácticas
En la gramática de Go, las construcciones como `[5]int` o `[]string` corresponden a producciones sintácticas del parser (`ply.yacc`), compuestas por la secuencia:
- `CORCHETE_IZQ` (`[`), opcionalmente `LITERAL_INT`, `CORCHETE_DER` (`]`), seguido de un tipo (`TIPO_INT`, `TIPO_STRING`, etc.).
- **Regla estricta:** No cree expresiones regulares en el analizador léxico que intenten capturar arreglos completos como un solo token (e.g., no crear `r'\[\d*\]\w+'`). Cada componente léxico debe tokenizarse individualmente.

### 4.4 Sincronización del Contador de Líneas (`lineno`) y Espacios Ignorados
A cargo de **Josué Pacheco** (`feat/lexico-josue`):
- Los caracteres en blanco y tabuladores deben descartarse con la directiva:
  ```python
  t_ignore = ' \t'
  ```
- Para que los reportes de error y logs reflejen fielmente la posición de los tokens en los archivos de entrada, se mantiene una regla unificada para el conteo de saltos de línea:
  ```python
  def t_newline(t):
      r'\n+'
      t.lexer.lineno += len(t.value)
  ```
- En caso de reconocer comentarios multilínea (`/* ... */`) o cadenas con saltos de línea (gestionados por Pablo Naranjo), se debe incrementar explícitamente `t.lexer.lineno += t.value.count('\n')`.

### 4.5 Manejo de Caracteres No Reconocidos (`t_error`)
A cargo de **Pablo Naranjo** (`feat/lexico-pablo`):
La función de error no debe detener bruscamente la ejecución (`no hacer sys.exit()`), sino registrar el carácter ilegal en la estructura de errores léxicos, reportar la línea y avanzar el lexer con `t.lexer.skip(1)` para permitir la recuperación léxica completa.

---

## 5. Algoritmos de Prueba y Formato Obligatorio de Logs (Avance 1)

### 5.1 Creación de Algoritmos de Prueba
Cada integrante del equipo debe crear desde cero, probar y confirmar desde su propia cuenta de Git un algoritmo en el sublenguaje Go, ubicándolo en el directorio [algoritmos/](./algoritmos/):

- `algoritmos/algoritmo1.go` &rarr; **Pablo Naranjo** (`@PabloNaranjoM`)
  - Enfoque: Estructuras (`struct`), mapas (`map`), tipos primitivos (`int`, `float64`), asignaciones compuestas y literales decimales.
- `algoritmos/algoritmo2.go` &rarr; **Hivor Araujo** (`@AraujoHivor`)
  - Enfoque: Flujo de control principal (`if`, `for`, `switch`), funciones (`func`), palabras clave de paquete/importación (`package`, `import`), operaciones aritméticas e identificadores.
- `algoritmos/algoritmo3.go` &rarr; **Josué Pacheco** (`@JosuePach3co`)
  - Enfoque: Evaluaciones booleanas (`true`, `false`), operadores relacionales (`==`, `!=`, `<`, `>=`, etc.), conectores lógicos (`&&`, `||`, `!`) y tipo `bool`.

> [!IMPORTANT]
> Cada archivo `.go` debe contener tanto código sintácticamente coherente como **errores léxicos deliberados** (e.g., caracteres ilegales como `@`, `$`, `~`, o comillas mal cerradas) para evidenciar el correcto funcionamiento y recuperación de la regla `t_error`.

### 5.2 Nomenclatura Oficial de Archivos de Log
El analizador léxico debe generar automáticamente un archivo de texto con el detalle de todos los tokens identificados y errores capturados.

- **Directorio de salida:** Todos los archivos de log deben almacenarse en [logs/](./logs/).
- **Formato de nombre exigido:**
  ```text
  lexico-NombreApellido-DD-MM-YYYY-HHhMM.txt
  ```
- **Ejemplos válidos:**
  - `lexico-PabloNaranjo-30-10-2026-15h30.txt`
  - `lexico-HivorAraujo-30-10-2026-16h15.txt`
  - `lexico-JosuePacheco-30-10-2026-17h45.txt`

> [!NOTE]
> Se utiliza el carácter `h` para separar las horas de los minutos en lugar de dos puntos (`:`). Esto asegura plena compatibilidad con los sistemas de archivos de Windows (donde `:` es un carácter reservado no permitido en nombres de archivo) y cumple de forma exacta con la muestra provista por el profesor Rodrigo Saraguro en las instrucciones de la asignatura.

### 5.3 Estructura Interna del Log Léxico
Cada archivo de log debe estructurarse con claridad técnica:
```text
================================================================================
REPORTE DE ANÁLISIS LÉXICO - COMPILADOR GO (ESPOL)
Archivo analizado: algoritmos/algoritmo1.go
Fecha y hora     : 30-10-2026 15:30:00
Desarrollador    : Pablo Naranjo (@PabloNaranjoM)
================================================================================

--- TOKENS RECONOCIDOS ---
[Línea   1, Columna   1] TOKEN: PACKAGE              LEXEMA: 'package'
[Línea   1, Columna   9] TOKEN: ID                   LEXEMA: 'main'
[Línea   3, Columna   1] TOKEN: IMPORT               LEXEMA: 'import'
...

--- ERRORES LÉXICOS DETECTADOS ---
[Línea  15, Columna   8] ERROR LÉXICO: Carácter ilegal '@' no reconocido por el lenguaje.
================================================================================
RESUMEN: Total Tokens: 85 | Total Errores Léxicos: 2
================================================================================
```

Los archivos de log resultantes de las pruebas deben agregarse y confirmarse mediante commits individuales en el repositorio para su respectiva evaluación.

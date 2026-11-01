"""
Punto de Entrada Principal - Compilador Subconjunto Go (Lenguajes de Programación)
=================================================================================
Este módulo constituye el punto de entrada principal para el proyecto:
- Avance 1: Interfaz de línea de comandos (CLI) para ejecutar el análisis léxico
  sobre algoritmos de prueba (.go) y generar automáticamente reportes de log
  conforme a la especificación académica:
  logs/lexico-<NombreApellido>-<DD>-<MM>-<YYYY>-<HH>h<MM>.txt.
- Entregas posteriores: Lanzador para la interfaz gráfica de usuario (GUI)
  desarrollada con CustomTkinter para análisis interactivo y visualización
  de tokens y árboles de derivación sintáctica.

Autores:
    - Pablo Naranjo (@PabloNaranjoM)
    - Hivor Araujo (@AraujoHivor)
    - Josué Pacheco (@JosuePach3co)
"""


# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
# TODO: Implementar runner CLI que acepte la ruta de un archivo fuente Go (*.go)
#       y el nombre del integrante evaluador.
# TODO: Invocar la función constructora build_lexer() de src.lexer para inicializar
#       el analizador léxico con PLY.
# TODO: Procesar el código fuente, extrayendo secuencialmente los tokens reconocidos
#       y recolectando los errores léxicos detectados.
# TODO: Formatear y exportar automáticamente el reporte de log en la carpeta:
#       logs/lexico-<NombreApellido>-<DD>-<MM>-<YYYY>-<HH>h<MM>.txt
#       asegurando la creación de la carpeta 'logs/' en caso de no existir.

import os
import sys
from datetime import datetime
from src.lexer import build_lexer


def obtener_desarrollador(ruta_archivo: str) -> tuple[str, str]:
    """Mapea el archivo de prueba con su respectivo autor según CONTRIBUTING.md."""
    archivo = os.path.basename(ruta_archivo).lower()
    if "algoritmo1" in archivo:
        return "Pablo Naranjo", "PabloNaranjo" 
    elif "algoritmo2" in archivo:
        return "Hivor Araujo", "HivorAraujo"
    elif "algoritmo3" in archivo:
        return "Josue Pacheco", "JosuePacheco"


def main() -> None:
    """Punto de entrada principal para la ejecución del analisis lexico por CLI."""
    if len(sys.argv) < 2:
        print("Uso: python main.py <ruta_archivo_go>")
        print("Ejemplos:")
        print("  python main.py algoritmos/algoritmo1.go")
        print("  python main.py algoritmos/algoritmo2.go")
        print("  python main.py algoritmos/algoritmo3.go")
        sys.exit(1)

    archivo_fuente = sys.argv[1]

    if not os.path.exists(archivo_fuente):
        print(f"Error: El archivo fuente '{archivo_fuente}' no existe.")
        sys.exit(1)

    with open(archivo_fuente, "r", encoding="utf-8") as f:
        codigo_fuente = f.read()

    # Construir el lexer
    lexer = build_lexer()
    lexer.input(codigo_fuente)

    tokens_encontrados = []

    # Procesar tokens y capturar errores léxicos
    while True:
        try:
            tok = lexer.token()
            if not tok:
                break
            tokens_encontrados.append(tok)
        except Exception as e:
            break

    # Asegurar la existencia de la carpeta 'logs/'
    os.makedirs("logs", exist_ok=True)

    # Identificar autor de forma dinámica
    nombre_completo, apellido_slug = obtener_desarrollador(archivo_fuente)

    # Generar marca de tiempo conforme a la regla: DD-MM-YYYY-HHhMM[cite: 1, 2]
    ahora = datetime.now()
    fecha_hora_str = ahora.strftime("%d-%m-%Y-%Hh%M")
    nombre_log = f"lexico-{apellido_slug}-{fecha_hora_str}.txt"
    ruta_log = os.path.join("logs", nombre_log)

    # Formatear el contenido del reporte de log
    lineas_reporte = [
        "=" * 80,
        "REPORTE DE ANALISIS LEXICO - COMPILADOR GO (ESPOL)",
        f"Archivo analizado: {archivo_fuente}",
        f"Fecha y hora     : {ahora.strftime('%d-%m-%Y %H:%M:%S')}",
        f"Desarrollador    : {nombre_completo}",
        "=" * 80,
        "",
        "--- TOKENS RECONOCIDOS ---"
    ]

    for tok in tokens_encontrados:
        lineas_reporte.append(
            f"[Linea {tok.lineno:3d}, Columna {tok.lexpos:3d}] TOKEN: {tok.type:20} LEXEMA: '{tok.value}'"
        )

    lineas_reporte.extend([
        "",
        "=" * 80,
        f"RESUMEN: Total Tokens Reconocidos: {len(tokens_encontrados)}",
        "=" * 80
    ])

    # Guardar el archivo de log en la carpeta correspondiente
    with open(ruta_log, "w", encoding="utf-8") as f_log:
        f_log.write("\n".join(lineas_reporte))

    print(f"[OK] Analisis lexico completado exitosamente.")
    print(f"[OK] Reporte de log generado en: {ruta_log}")
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================



#def main() -> None:
 #   """Punto de entrada principal para la ejecución de la aplicación."""
 #   pass


if __name__ == "__main__":
    main()

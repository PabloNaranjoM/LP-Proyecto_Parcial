"""
Punto de entrada principal: lanza la GUI en CustomTkinter o el modo `--cli`.

Autores:
    - Pablo Naranjo (@PabloNaranjoM)
    - Hivor Araujo (@AraujoHivor)
    - Josué Pacheco (@JosuePach3co)
"""

import argparse
from pathlib import Path
import sys

from src.gui import launch_gui
from src.gui.log_exporter import (
    ejecutar_analisis_completo_codigo,
    ejecutar_analisis_lexico_codigo,
    ejecutar_analisis_sintactico_codigo,
)


# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def ejecutar_modo_cli(ruta_archivo: str, autor: str, fase: str = "todo") -> None:
    """Ejecuta el análisis indicado (`lexico`, `sintactico` o `todo`) desde consola."""
    path = Path(ruta_archivo)
    if not path.exists():
        print(f"Error: No se encontró el archivo '{ruta_archivo}'.", file=sys.stderr)
        sys.exit(1)

    codigo = path.read_text(encoding="utf-8")
    nombre = path.as_posix()

    if fase == "lexico":
        res = ejecutar_analisis_lexico_codigo(codigo, autor, nombre)
        print(
            f"[LÉXICO] Tokens: {len(res['tokens'])} | "
            f"Errores: {len(res['errores'])} | Log: {res['ruta_log'].as_posix()}"
        )
    elif fase == "sintactico":
        res = ejecutar_analisis_sintactico_codigo(codigo, autor, nombre)
        print(
            f"[SINTÁCTICO] Reglas: {len(res['reglas'])} | "
            f"Errores: {len(res['errores'])} | Log: {res['ruta_log'].as_posix()}"
        )
    # TODO (Avance 3 - Paso 4.3 | Pablo Naranjo @PabloNaranjoM):
    #       - Agregar rama `elif fase == "semantico":` ejecutando
    #         `ejecutar_analisis_semantico_codigo(codigo, autor, nombre)` y mostrando
    #         símbolos, reglas validadas, errores semánticos y ruta del log.
    #       - Actualizar la rama `else:` (modo `todo`) para imprimir también el resumen
    #         de `completo["semantico"]`.
    else:
        completo = ejecutar_analisis_completo_codigo(codigo, autor, nombre)
        r_lex = completo["lexico"]
        r_sin = completo["sintactico"]
        print(
            f"[LÉXICO] Tokens: {len(r_lex['tokens'])} | "
            f"Errores: {len(r_lex['errores'])} | Log: {r_lex['ruta_log'].as_posix()}"
        )
        print(
            f"[SINTÁCTICO] Reglas: {len(r_sin['reglas'])} | "
            f"Errores: {len(r_sin['errores'])} | Log: {r_sin['ruta_log'].as_posix()}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analizador Léxico, Sintáctico y Semántico en Go — PLY & CustomTkinter"
    )
    parser.add_argument("archivo", nargs="?", default="algoritmos/algoritmo1.go")
    parser.add_argument("autor", nargs="?", default="PabloNaranjoM")
    parser.add_argument("--cli", action="store_true", help="Ejecutar en modo consola")
    # TODO (Avance 3 - Paso 4.3 | Pablo Naranjo @PabloNaranjoM):
    #       Agregar `"semantico"` a `choices` en `--fase` (`["lexico", "sintactico", "semantico", "todo"]`).
    parser.add_argument(
        "--fase",
        choices=["lexico", "sintactico", "todo"],
        default="todo",
        help="Fase de análisis a ejecutar en modo CLI (por defecto: todo)",
    )
    args = parser.parse_args()

    if args.cli:
        ejecutar_modo_cli(args.archivo, args.autor, args.fase)
    else:
        launch_gui(archivo_inicial=args.archivo)
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


if __name__ == "__main__":
    main()

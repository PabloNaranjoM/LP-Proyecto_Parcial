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
    ejecutar_analisis_semantico_codigo,
    ejecutar_analisis_sintactico_codigo,
)


# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def _imprimir_resumen_cli(fase: str, res: dict) -> None:
    ruta = res["ruta_log"].as_posix()
    if fase == "lexico":
        print(
            f"[LÉXICO] Tokens: {len(res['tokens'])} | "
            f"Errores: {len(res['errores'])} | Log: {ruta}"
        )
    elif fase == "sintactico":
        print(
            f"[SINTÁCTICO] Reglas: {len(res['reglas'])} | "
            f"Errores: {len(res['errores'])} | Log: {ruta}"
        )
    elif fase == "semantico":
        print(
            f"[SEMÁNTICO] Símbolos: {len(res['simbolos'])} | "
            f"Reglas: {len(res['reglas_semanticas'])} | "
            f"Errores: {len(res['errores'])} | Log: {ruta}"
        )


def ejecutar_modo_cli(ruta_archivo: str, autor: str, fase: str = "todo") -> None:
    """Ejecuta el análisis indicado (`lexico`, `sintactico`, `semantico` o `todo`) desde consola."""
    path = Path(ruta_archivo)
    if not path.exists():
        print(f"Error: No se encontró el archivo '{ruta_archivo}'.", file=sys.stderr)
        sys.exit(1)

    codigo = path.read_text(encoding="utf-8")
    nombre = path.as_posix()

    ejecutores = {
        "lexico": ejecutar_analisis_lexico_codigo,
        "sintactico": ejecutar_analisis_sintactico_codigo,
        "semantico": ejecutar_analisis_semantico_codigo,
    }
    if fase in ejecutores:
        _imprimir_resumen_cli(fase, ejecutores[fase](codigo, autor, nombre))
    else:
        completo = ejecutar_analisis_completo_codigo(codigo, autor, nombre)
        for etapa in ("lexico", "sintactico", "semantico"):
            _imprimir_resumen_cli(etapa, completo[etapa])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analizador Léxico, Sintáctico y Semántico en Go — PLY & CustomTkinter"
    )
    parser.add_argument("archivo", nargs="?", default="algoritmos/algoritmo1.go")
    parser.add_argument("autor", nargs="?", default="PabloNaranjoM")
    parser.add_argument("--cli", action="store_true", help="Ejecutar en modo consola")
    parser.add_argument(
        "--fase",
        choices=["lexico", "sintactico", "semantico", "todo"],
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

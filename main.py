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
from src.gui.log_exporter import ejecutar_analisis_lexico_codigo


# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
def ejecutar_modo_cli(ruta_archivo: str, autor: str) -> None:
    """Ejecuta el análisis léxico desde consola y genera el reporte en `logs/`."""
    path = Path(ruta_archivo)
    if not path.exists():
        print(f"Error: No se encontró el archivo '{ruta_archivo}'.", file=sys.stderr)
        sys.exit(1)

    resultado = ejecutar_analisis_lexico_codigo(
        codigo_fuente=path.read_text(encoding="utf-8"),
        desarrollador=autor,
        nombre_archivo=path.as_posix(),
    )
    print(
        f"Análisis finalizado | Tokens: {len(resultado['tokens'])} | "
        f"Errores: {len(resultado['errores'])} | Log: {resultado['ruta_log'].as_posix()}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analizador Léxico, Sintáctico y Semántico en Go — PLY & CustomTkinter"
    )
    parser.add_argument("archivo", nargs="?", default="algoritmos/algoritmo1.go")
    parser.add_argument("autor", nargs="?", default="PabloNaranjoM")
    parser.add_argument("--cli", action="store_true", help="Ejecutar en modo consola")
    args = parser.parse_args()

    if args.cli:
        ejecutar_modo_cli(args.archivo, args.autor)
    else:
        launch_gui(archivo_inicial=args.archivo)
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


if __name__ == "__main__":
    main()

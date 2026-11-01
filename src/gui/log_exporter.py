"""
Ejecución léxica y exportación automatizada de registros en `logs/`.

Responsable:
    - Pablo Naranjo (@PabloNaranjoM)
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from src.lexer import analizar

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
MAPA_DESARROLLADORES = {
    "PabloNaranjoM": "PabloNaranjo",
    "AraujoHivor": "HivorAraujo",
    "JosuePach3co": "JosuePacheco",
}


def normalizar_nombre_desarrollador(desarrollador: str) -> str:
    limpio = desarrollador.strip().lstrip("@")
    return MAPA_DESARROLLADORES.get(limpio, limpio.replace(" ", "") or "Desarrollador")


def _detalle_error_log(err: dict[str, Any]) -> str:
    ch = err["caracter"]
    if ch == "/*":
        return "Comentario multilínea no cerrado al fin de archivo."
    return f"Carácter ilegal {repr(ch)} no reconocido por el lenguaje."


def ejecutar_analisis_lexico_codigo(
    codigo_fuente: str,
    desarrollador: str,
    nombre_archivo: str = "editor_interactivo.go",
    tipo_analisis: str = "lexico",
) -> dict[str, Any]:
    """Ejecuta el análisis léxico sobre `codigo_fuente` y guarda el reporte en `logs/`."""
    tokens, errores = analizar(codigo_fuente)

    carpeta_logs = Path("logs")
    carpeta_logs.mkdir(parents=True, exist_ok=True)

    ahora = datetime.now()
    nombre_dev = normalizar_nombre_desarrollador(desarrollador)
    nombre_log = f"{tipo_analisis}-{nombre_dev}-{ahora.strftime('%d-%m-%Y-%Hh%M')}.txt"
    ruta_log = carpeta_logs / nombre_log

    lineas = [
        "=" * 80,
        "REPORTE DE ANÁLISIS LÉXICO - COMPILADOR GO (ESPOL)",
        f"Archivo analizado: {nombre_archivo}",
        f"Fecha y hora     : {ahora.strftime('%d-%m-%Y %H:%M:%S')}",
        f"Desarrollador    : {desarrollador}",
        "=" * 80,
        "",
        "--- TOKENS RECONOCIDOS ---",
    ]
    if tokens:
        lineas.extend(
            f"[Línea {t['linea']:>3}, Columna {t['columna']:>3}] "
            f"TOKEN: {t['tipo']:<20} LEXEMA: {repr(str(t['valor']))}"
            for t in tokens
        )
    else:
        lineas.append("No se reconocieron tokens válidos.")

    lineas.extend(["", "--- ERRORES LÉXICOS DETECTADOS ---"])
    if errores:
        lineas.extend(
            f"[Línea {e['linea']:>3}, Columna {e['columna']:>3}] "
            f"ERROR LÉXICO: {_detalle_error_log(e)}"
            for e in errores
        )
    else:
        lineas.append("No se detectaron errores léxicos.")

    lineas.extend([
        "=" * 80,
        f"RESUMEN: Total Tokens: {len(tokens)} | Total Errores Léxicos: {len(errores)}",
        "=" * 80,
    ])
    ruta_log.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    return {
        "tokens": tokens,
        "errores": errores,
        "ruta_log": ruta_log,
        "nombre_log": nombre_log,
        "valido": not errores,
    }
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

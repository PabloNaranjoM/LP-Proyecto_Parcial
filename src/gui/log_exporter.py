"""
Ejecución léxica, sintáctica y exportación automatizada de registros en `logs/`.

Responsable:
    - Pablo Naranjo (@PabloNaranjoM)
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from src.lexer import analizar
from src.parser import analizar_sintaxis

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


def normalizar_usuario_git(desarrollador: str) -> str:
    limpio = desarrollador.strip().lstrip("@")
    MAPA_INVERSO = {v: k for k, v in MAPA_DESARROLLADORES.items()}
    return MAPA_INVERSO.get(limpio, limpio.replace(" ", "") or "Desarrollador")


def ejecutar_analisis_sintactico_codigo(
    codigo_fuente: str,
    desarrollador: str,
    nombre_archivo: str = "editor_interactivo.go",
) -> dict[str, Any]:
    """Ejecuta el análisis sintáctico sobre `codigo_fuente` y guarda el reporte en `logs/`."""
    resultado = analizar_sintaxis(codigo_fuente)
    reglas = resultado["reglas"]
    errores_sin = resultado["errores"]
    errores_lex = resultado["errores_lexicos"]

    carpeta_logs = Path("logs")
    carpeta_logs.mkdir(parents=True, exist_ok=True)

    ahora = datetime.now()
    usuario_git = normalizar_usuario_git(desarrollador)
    nombre_log = f"sintactico-{usuario_git}-{ahora.strftime('%d%m%Y-%Hh%M')}.txt"
    ruta_log = carpeta_logs / nombre_log

    lineas = [
        "=" * 80,
        "REPORTE DE ANÁLISIS SINTÁCTICO - COMPILADOR GO (ESPOL)",
        f"Archivo analizado: {nombre_archivo}",
        f"Fecha y hora     : {ahora.strftime('%d-%m-%Y %H:%M:%S')}",
        f"Desarrollador    : {usuario_git}",
        "=" * 80,
        "",
        "--- REGLAS GRAMATICALES VALIDADAS ---",
    ]
    if reglas:
        lineas.extend(
            f"[Línea {r['linea']:>3}] REGLA VALIDADA: {r['regla']}"
            for r in sorted(reglas, key=lambda x: x["linea"])
        )
    else:
        lineas.append("No se validaron reglas gramaticales.")

    lineas.extend(["", "--- ERRORES SINTÁCTICOS DETECTADOS ---"])
    if errores_sin:
        for e in errores_sin:
            lineas.append(f"[Línea {e['linea']:>3}, Columna {e['columna']:>3}] {e['mensaje']}")
    else:
        lineas.append("No se detectaron errores sintácticos.")

    if errores_lex:
        lineas.extend(["", "--- ALERTAS LÉXICAS PREVIAS ---"])
        lineas.extend(
            f"[Línea {e['linea']:>3}, Columna {e['columna']:>3}] ERROR LÉXICO: {_detalle_error_log(e)}"
            for e in errores_lex
        )

    estado_str = "VÁLIDO" if resultado["valido"] else "INVÁLIDO"
    lineas.extend([
        "=" * 80,
        f"RESUMEN: Reglas Validadas: {len(reglas)} | Errores Sintácticos: {len(errores_sin)} | Estado: {estado_str}",
        "=" * 80,
    ])
    ruta_log.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    return {
        **resultado,
        "ruta_log": ruta_log,
        "nombre_log": nombre_log,
    }


def ejecutar_analisis_completo_codigo(
    codigo_fuente: str,
    desarrollador: str,
    nombre_archivo: str = "editor_interactivo.go",
) -> dict[str, Any]:
    """Ejecuta las fases léxica y sintáctica en secuencia y exporta ambos registros."""
    res_lexico = ejecutar_analisis_lexico_codigo(
        codigo_fuente=codigo_fuente,
        desarrollador=desarrollador,
        nombre_archivo=nombre_archivo,
    )
    res_sintactico = ejecutar_analisis_sintactico_codigo(
        codigo_fuente=codigo_fuente,
        desarrollador=desarrollador,
        nombre_archivo=nombre_archivo,
    )
    return {
        "lexico": res_lexico,
        "sintactico": res_sintactico,
        "valido": res_lexico["valido"] and res_sintactico["valido"],
    }
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

"""
Tema visual (modo oscuro tipo IDE), constantes de la GUI y formato de tokens.

Autores:
    - Pablo Naranjo (@PabloNaranjoM)
    - Josué Pacheco (@JosuePach3co)
    - Hivor Araujo (@AraujoHivor)
"""

# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
APP_TITLE = "Analizador Léxico, Sintáctico y Semántico en Go — PLY & CustomTkinter"
WINDOW_SIZE = (1280, 760)
WINDOW_MIN_SIZE = (1024, 640)

DEVELOPERS_LIST = ["PabloNaranjoM", "AraujoHivor", "JosuePach3co"]

BG_MAIN = "#121417"
BG_PANEL = "#1A1D24"
BG_EDITOR = "#0E1015"
BG_LINE_NUMBERS = "#14171F"
BG_ROW_ALT = "#131720"
BG_BADGE = "#161B22"
BORDER_PANEL = "#2A2E39"
BORDER_SOFT = "#30363D"

TEXT_PRIMARY = "#E6EDF3"
TEXT_SECONDARY = "#8B949E"
TEXT_MUTED = "#6E7681"
ACCENT = "#58A6FF"

BTN_PRIMARY = ("#1F6FEB", "#388BFD")
BTN_SUCCESS = ("#238636", "#2EA043")
BTN_SECONDARY = ("#21262D", "#30363D")
BTN_DANGER = ("#3D1D22", "#54242B")
BTN_DANGER_TEXT = "#F85149"
BTN_DANGER_BORDER = "#6E2B33"

_OK = {"bg": "#0F291E", "border": "#238636", "fg": "#3FB950", "badge_bg": "#123524"}
_ERROR = {"bg": "#2D1418", "border": "#F85149", "fg": "#FF7B72", "badge_bg": "#3D1D22"}
_IDLE = {"bg": BG_BADGE, "border": BORDER_SOFT, "fg": ACCENT, "badge_bg": "#1F2937"}

OK_FG = _OK["fg"]
ERROR_FG = _ERROR["fg"]
ERROR_ROW_BG = _ERROR["badge_bg"]
ERROR_LINE_BG = "#491C21"

ESTADOS_BANNER = {
    "IDLE": {
        **_IDLE,
        "mensaje": "ESTADO DEL SISTEMA: Listo para analizar código fuente en Go.",
        "badge": "[EN ESPERA]",
    },
    "VALIDO": {
        **_OK,
        "mensaje": "ESTADO DEL SISTEMA: Análisis léxico completado sin errores.",
        "badge": "[VÁLIDO]",
    },
    "ERROR_LEXICO": {
        **_ERROR,
        "mensaje": "ALERTA LÉXICA: Se detectaron caracteres no reconocidos en el código fuente.",
        "badge": "[ERROR LÉXICO]",
    },
    "ERROR_SINTACTICO": {
        **_ERROR,
        "mensaje": "ALERTA SINTÁCTICA: La secuencia de tokens incumple las reglas gramaticales de Go.",
        "badge": "[ERROR SINTÁCTICO]",
    },
    "ERROR_SEMANTICO": {
        **_ERROR,
        "mensaje": "ALERTA SEMÁNTICA: Incompatibilidad de tipos y reglas de alcance detectada.",
        "badge": "[ERROR SEMÁNTICO]",
    },
}

SYNTAX_COLORS = {
    "keyword": "#FF7B72",
    "type_bool": "#79C0FF",
    "string": "#A5D6FF",
    "number": "#D2A8FF",
    "comment": "#8B949E",
}


def fuente_ui(tam: int = 12, negrita: bool = True) -> tuple[str, int, str]:
    return ("Segoe UI", tam, "bold" if negrita else "normal")


def fuente_mono(tam: int = 12, negrita: bool = False) -> tuple[str, int, str]:
    return ("Consolas", tam, "bold" if negrita else "normal")
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================


# =====================================================================
# INICIO APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================
from src.lexer import formatear_categoria_token

__all__ = ["formatear_categoria_token"]
# =====================================================================
# FIN APORTE: Josué Pacheco (@JosuePach3co)
# =====================================================================

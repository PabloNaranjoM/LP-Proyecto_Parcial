"""
Panel izquierdo de la GUI: editor de código Go con numeración de líneas,
resaltado básico de sintaxis, resaltado de errores y carga de archivos `.go`.

Responsable:
    - Hivor Araujo (@AraujoHivor)
"""

# =====================================================================
# INICIO APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================
from __future__ import annotations

from pathlib import Path
import re
import tkinter as tk
from tkinter import filedialog
from typing import Callable

import customtkinter as ctk

from src.lexer import KEYWORDS_MAP
from .theme import (
    ACCENT,
    BG_EDITOR,
    BG_LINE_NUMBERS,
    BG_PANEL,
    BORDER_PANEL,
    ERROR_FG,
    ERROR_LINE_BG,
    SYNTAX_COLORS,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    fuente_mono,
    fuente_ui,
)

# Expresiones regulares derivadas del propio lexer para evitar duplicar listas de palabras
_TIPOS_Y_BOOLS = {k for k, v in KEYWORDS_MAP.items() if v.startswith("TIPO_") or v in ("VERDADERO", "FALSO")}
_RESERVADAS = set(KEYWORDS_MAP) - _TIPOS_Y_BOOLS

_PATRONES_SINTAXIS: list[tuple[str, re.Pattern[str]]] = [
    ("keyword", re.compile(rf"\b(?:{'|'.join(sorted(_RESERVADAS))})\b")),
    ("type_bool", re.compile(rf"\b(?:{'|'.join(sorted(_TIPOS_Y_BOOLS))})\b")),
    ("number", re.compile(r"\b\d+(?:\.\d+)?\b")),
    ("string", re.compile(r'"(?:[^"\\\n]|\\.)*"')),
    ("comment", re.compile(r"//[^\n]*|/\*[\s\S]*?(?:\*/|$)")),
]


class CodeEditorPanel(ctk.CTkFrame):
    """Editor de código fuente en Go con numeración de líneas sincronizada."""

    def __init__(
        self,
        master: tk.Misc,
        nombre_archivo_inicial: str = "sin_titulo.go",
        on_change: Callable[[], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            fg_color=BG_PANEL,
            border_color=BORDER_PANEL,
            corner_radius=8,
            border_width=1,
            **kwargs,
        )
        self._nombre_archivo = nombre_archivo_inicial
        self._on_change = on_change
        self._lineas_error: set[int] = set()

        self._construir_interfaz()
        self._configurar_tags()
        self._vincular_eventos()
        self._actualizar_numeros_linea()

    def _construir_interfaz(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="EDITOR DE CÓDIGO FUENTE (GO)",
            font=fuente_ui(12),
            text_color=TEXT_SECONDARY,
        ).grid(row=0, column=0, sticky="w")

        self.file_badge = ctk.CTkLabel(
            header,
            text=self._nombre_archivo,
            fg_color="#1F2937",
            text_color=ACCENT,
            corner_radius=6,
            padx=10,
            pady=2,
            font=fuente_mono(11),
        )
        self.file_badge.grid(row=0, column=1, sticky="e")

        body = ctk.CTkFrame(
            self,
            fg_color=BG_EDITOR,
            border_color=BORDER_PANEL,
            border_width=1,
            corner_radius=6,
        )
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(2, weight=1)

        self.textbox = ctk.CTkTextbox(
            body,
            fg_color=BG_EDITOR,
            text_color=TEXT_PRIMARY,
            font=fuente_mono(13),
            wrap="none",
            corner_radius=0,
            border_width=0,
            undo=True,
        )
        self.textbox.grid(row=0, column=2, sticky="nsew", padx=(0, 2), pady=2)

        self._text: tk.Text = self.textbox._textbox
        self._text.configure(
            insertbackground=TEXT_PRIMARY,
            selectbackground="#264F78",
            selectforeground=TEXT_PRIMARY,
            padx=8,
            pady=6,
        )

        self.line_numbers = tk.Text(
            body,
            width=4,
            padx=8,
            pady=6,
            takefocus=0,
            bd=0,
            highlightthickness=0,
            background=BG_LINE_NUMBERS,
            foreground=TEXT_SECONDARY,
            font=self._text.cget("font"),
            state="disabled",
            wrap="none",
            cursor="arrow",
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns", padx=(2, 0), pady=2)

        ctk.CTkFrame(body, width=1, fg_color=BORDER_PANEL, corner_radius=0).grid(
            row=0, column=1, sticky="ns", pady=2
        )

        self._text.configure(yscrollcommand=self._on_text_yscroll)
        if getattr(self.textbox, "_y_scrollbar", None) is not None:
            self.textbox._y_scrollbar.configure(command=self._on_scrollbar_yview)

    def _configurar_tags(self) -> None:
        self._text.tag_configure("error_line", background=ERROR_LINE_BG)
        self.line_numbers.tag_configure("align_right", justify="right")
        self.line_numbers.tag_configure(
            "error_line_num", background=ERROR_LINE_BG, foreground=ERROR_FG
        )

        for tag, color in SYNTAX_COLORS.items():
            self._text.tag_configure(tag, foreground=color)

        self._text.tag_lower("error_line")
        if "sel" in self._text.tag_names():
            self._text.tag_raise("sel")

    def _vincular_eventos(self) -> None:
        self._text.bind("<Tab>", self._on_tab)
        self._text.bind("<KeyRelease>", self._on_cambio_texto, add="+")
        for ev in ("<ButtonRelease-1>", "<MouseWheel>", "<Configure>"):
            self._text.bind(ev, lambda _e: self.after_idle(self._sincronizar_scroll), add="+")

        self.line_numbers.bind("<MouseWheel>", self._on_rueda_numeros)
        self.line_numbers.bind("<B1-Motion>", lambda _e: "break")
        self.line_numbers.bind("<Button-1>", lambda _e: "break")

    def _on_tab(self, _event: tk.Event) -> str:
        self._text.insert("insert", "    ")
        self._on_cambio_texto()
        return "break"

    def _on_text_yscroll(self, first: str, last: str) -> None:
        if getattr(self.textbox, "_y_scrollbar", None) is not None:
            self.textbox._y_scrollbar.set(first, last)
        self.line_numbers.yview_moveto(first)

    def _on_scrollbar_yview(self, *args) -> None:
        self._text.yview(*args)
        self.line_numbers.yview(*args)

    def _on_rueda_numeros(self, event: tk.Event) -> str:
        if getattr(event, "delta", 0):
            self._text.yview_scroll(-1 if event.delta > 0 else 1, "units")
        self._sincronizar_scroll()
        return "break"

    def _on_cambio_texto(self, _event: tk.Event | None = None) -> None:
        self._actualizar_numeros_linea()
        self._aplicar_resaltado_sintaxis()
        if self._on_change:
            self._on_change()

    def _sincronizar_scroll(self) -> None:
        self.line_numbers.yview_moveto(self._text.yview()[0])

    def _total_lineas(self) -> int:
        fin = self._text.index("end-1c")
        return max(1, int(fin.split(".")[0])) if fin else 1

    def _actualizar_numeros_linea(self) -> None:
        total = self._total_lineas()
        ancho = max(4, len(str(total)) + 1)
        if int(self.line_numbers.cget("width")) != ancho:
            self.line_numbers.configure(width=ancho)

        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert(
            "1.0", "\n".join(str(i) for i in range(1, total + 1)), "align_right"
        )
        for ln in self._lineas_error:
            if 1 <= ln <= total:
                self.line_numbers.tag_add("error_line_num", f"{ln}.0", f"{ln}.end")
        self.line_numbers.configure(state="disabled")
        self._sincronizar_scroll()

    def _aplicar_resaltado_sintaxis(self) -> None:
        for tag in SYNTAX_COLORS:
            self._text.tag_remove(tag, "1.0", "end")

        codigo = self.obtener_codigo()
        if not codigo:
            return

        for tag, regex in _PATRONES_SINTAXIS:
            for m in regex.finditer(codigo):
                ini, fin = f"1.0+{m.start()}c", f"1.0+{m.end()}c"
                if tag in ("string", "comment"):
                    for previo in ("keyword", "type_bool", "number", "string"):
                        if previo != tag:
                            self._text.tag_remove(previo, ini, fin)
                self._text.tag_add(tag, ini, fin)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def ir_a_linea(self, linea: int) -> None:
        """Desplaza el editor hasta hacer visible `linea`."""
        self._text.see(f"{linea}.0")
        self._sincronizar_scroll()

    def resaltar_lineas_error(self, lineas: list[int]) -> None:
        self.limpiar_resaltado_errores()
        total = self._total_lineas()
        self._lineas_error = {ln for ln in lineas if 1 <= ln <= total}
        for ln in self._lineas_error:
            self._text.tag_add("error_line", f"{ln}.0", f"{ln}.end+1c")
        self._text.tag_lower("error_line")
        self._actualizar_numeros_linea()

    def limpiar_resaltado_errores(self) -> None:
        self._lineas_error.clear()
        self._text.tag_remove("error_line", "1.0", "end")
        self.line_numbers.configure(state="normal")
        self.line_numbers.tag_remove("error_line_num", "1.0", "end")
        self.line_numbers.configure(state="disabled")

    def obtener_codigo(self) -> str:
        return self._text.get("1.0", "end-1c")

    def obtener_nombre_archivo(self) -> str:
        return self._nombre_archivo

    def establecer_codigo(
        self, codigo: str, nombre_archivo: str = "editor_interactivo.go"
    ) -> None:
        self.limpiar_resaltado_errores()
        self._nombre_archivo = nombre_archivo
        self.file_badge.configure(text=nombre_archivo)

        self._text.delete("1.0", "end")
        if codigo:
            self._text.insert("1.0", codigo)
        self._text.edit_reset()
        self._text.yview_moveto(0.0)
        self._actualizar_numeros_linea()
        self._aplicar_resaltado_sintaxis()

    def cargar_archivo_dialogo(
        self, directorio_inicial: str = "algoritmos"
    ) -> tuple[str, str] | None:
        carpeta = Path(directorio_inicial).resolve()
        if not carpeta.is_dir():
            carpeta = Path.cwd()

        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo fuente Go (.go)",
            initialdir=str(carpeta),
            filetypes=[("Archivos Go", "*.go"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return None

        path = Path(ruta)
        contenido = path.read_text(encoding="utf-8")
        self.establecer_codigo(contenido, nombre_archivo=path.name)
        return str(path), contenido

    def limpiar_editor(self) -> None:
        self.establecer_codigo("", nombre_archivo="sin_titulo.go")
# =====================================================================
# FIN APORTE: Hivor Araujo (@AraujoHivor)
# =====================================================================

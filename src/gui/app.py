"""
Ventana principal (`GoAnalyzerApp`) en CustomTkinter.

Estructura en 3 zonas:
1. Barra de herramientas superior (archivo, desarrollador y botones de ejecución).
2. Área central dividida (Editor de código Go y Panel de diagnóstico).
3. Barra de estado inferior (confirmación del archivo de log en `logs/`).

Autores:
    - Pablo Naranjo (@PabloNaranjoM)
    - Hivor Araujo (@AraujoHivor)
    - Josué Pacheco (@JosuePach3co)
"""

from __future__ import annotations

from pathlib import Path
import customtkinter as ctk

from .diagnostics_panel import DiagnosticsPanel
from .editor_panel import CodeEditorPanel
from .log_exporter import ejecutar_analisis_lexico_codigo
from .theme import (
    ACCENT,
    APP_TITLE,
    BG_BADGE,
    BG_MAIN,
    BG_PANEL,
    BORDER_PANEL,
    BORDER_SOFT,
    BTN_DANGER,
    BTN_DANGER_BORDER,
    BTN_DANGER_TEXT,
    BTN_PRIMARY,
    BTN_SECONDARY,
    BTN_SUCCESS,
    DEVELOPERS_LIST,
    OK_FG,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    WINDOW_MIN_SIZE,
    WINDOW_SIZE,
    fuente_mono,
    fuente_ui,
)


# =====================================================================
# INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================
class GoAnalyzerApp(ctk.CTk):
    """Ventana principal del Analizador Léxico, Sintáctico y Semántico en Go."""

    def __init__(self, archivo_inicial: str | None = "algoritmos/algoritmo1.go") -> None:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.minsize(*WINDOW_MIN_SIZE)
        self.configure(fg_color=BG_MAIN)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.desarrollador_var = ctk.StringVar(value=DEVELOPERS_LIST[0])

        self._construir_barra_herramientas()
        self._construir_area_central()
        self._construir_barra_estado_inferior()

        if archivo_inicial:
            path = Path(archivo_inicial)
            if path.is_file():
                self.editor_panel.establecer_codigo(
                    path.read_text(encoding="utf-8"), nombre_archivo=path.name
                )

    def _construir_barra_herramientas(self) -> None:
        toolbar = ctk.CTkFrame(
            self,
            fg_color=BG_PANEL,
            border_color=BORDER_PANEL,
            border_width=1,
            corner_radius=8,
            height=52,
        )
        toolbar.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 8))
        toolbar.grid_columnconfigure(1, weight=1)

        # =====================================================================
        # INICIO APORTE: Hivor Araujo (@AraujoHivor)
        # =====================================================================
        left = ctk.CTkFrame(toolbar, fg_color="transparent")
        left.grid(row=0, column=0, padx=10, pady=8, sticky="w")

        ctk.CTkButton(
            left,
            text="📂 Cargar archivo .go",
            command=self._accion_cargar_archivo,
            fg_color=BTN_SECONDARY[0],
            hover_color=BTN_SECONDARY[1],
            border_color=BORDER_SOFT,
            border_width=1,
            text_color=TEXT_PRIMARY,
            font=fuente_ui(12),
            height=34,
            width=155,
            corner_radius=6,
        ).grid(row=0, column=0, padx=(0, 8))

        ctk.CTkButton(
            left,
            text="🗑 Limpiar",
            command=self._accion_limpiar,
            fg_color=BTN_DANGER[0],
            hover_color=BTN_DANGER[1],
            border_color=BTN_DANGER_BORDER,
            border_width=1,
            text_color=BTN_DANGER_TEXT,
            font=fuente_ui(12),
            height=34,
            width=100,
            corner_radius=6,
        ).grid(row=0, column=1)
        # =====================================================================
        # FIN APORTE: Hivor Araujo (@AraujoHivor)
        # =====================================================================

        center = ctk.CTkFrame(toolbar, fg_color="transparent")
        center.grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(
            center, text="Desarrollador:", font=fuente_ui(12), text_color=TEXT_SECONDARY
        ).grid(row=0, column=0, padx=(0, 8))

        ctk.CTkOptionMenu(
            center,
            variable=self.desarrollador_var,
            values=DEVELOPERS_LIST,
            fg_color=BTN_SECONDARY[0],
            button_color=BORDER_SOFT,
            button_hover_color="#3B4252",
            dropdown_fg_color=BG_PANEL,
            dropdown_hover_color=BTN_PRIMARY[0],
            text_color=TEXT_PRIMARY,
            font=fuente_mono(12, negrita=True),
            height=34,
            width=175,
            corner_radius=6,
        ).grid(row=0, column=1)

        right = ctk.CTkFrame(toolbar, fg_color="transparent")
        right.grid(row=0, column=2, padx=10, pady=8, sticky="e")

        botones = [
            ("Léxico", lambda: self._ejecutar_lexico(False), BTN_PRIMARY, 90, 6),
            ("Sintáctico", None, BTN_PRIMARY, 95, 6),
            ("Semántico", None, BTN_PRIMARY, 95, 8),
            ("▶ Ejecutar Todo", lambda: self._ejecutar_lexico(True), BTN_SUCCESS, 130, 0),
        ]
        for col, (texto, cmd, colores, ancho, pad_der) in enumerate(botones):
            ctk.CTkButton(
                right,
                text=texto,
                command=cmd,
                fg_color=colores[0],
                hover_color=colores[1],
                text_color="#FFFFFF",
                font=fuente_ui(12),
                height=34,
                width=ancho,
                corner_radius=6,
            ).grid(row=0, column=col, padx=(0, pad_der))

    def _construir_area_central(self) -> None:
        workspace = ctk.CTkFrame(self, fg_color="transparent")
        workspace.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 8))
        workspace.grid_rowconfigure(0, weight=1)
        workspace.grid_columnconfigure(0, weight=45, uniform="split")
        workspace.grid_columnconfigure(1, weight=55, uniform="split")

        self.editor_panel = CodeEditorPanel(
            workspace, nombre_archivo_inicial="algoritmo1.go"
        )
        self.editor_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        self.diagnostics_panel = DiagnosticsPanel(
            workspace, on_line_select=self.editor_panel.ir_a_linea
        )
        self.diagnostics_panel.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

    def _construir_barra_estado_inferior(self) -> None:
        footer = ctk.CTkFrame(
            self,
            fg_color=BG_PANEL,
            border_color=BORDER_PANEL,
            border_width=1,
            corner_radius=8,
            height=38,
        )
        footer.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 10))
        footer.grid_columnconfigure(2, weight=1)

        ctk.CTkLabel(
            footer,
            text="📄 Registro generado automáticamente:",
            font=fuente_ui(11),
            text_color=TEXT_SECONDARY,
        ).grid(row=0, column=0, padx=(12, 8), pady=6, sticky="w")

        self.lbl_log_badge = ctk.CTkLabel(
            footer,
            text="Sin registros generados en esta sesión",
            fg_color=BG_BADGE,
            text_color=ACCENT,
            corner_radius=6,
            padx=10,
            pady=2,
            font=fuente_mono(11, negrita=True),
        )
        self.lbl_log_badge.grid(row=0, column=1, pady=6, sticky="w")

        ctk.CTkLabel(
            footer,
            text="Codificación: UTF-8 • ✓ Guardado en /logs",
            font=fuente_ui(11, negrita=False),
            text_color=OK_FG,
        ).grid(row=0, column=2, padx=12, pady=6, sticky="e")

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------
    def _accion_cargar_archivo(self) -> None:
        if self.editor_panel.cargar_archivo_dialogo() is not None:
            self.diagnostics_panel.limpiar_panel()

    def _accion_limpiar(self) -> None:
        self.editor_panel.limpiar_editor()
        self.diagnostics_panel.limpiar_panel()
        self.lbl_log_badge.configure(
            text="Sin registros generados en esta sesión", text_color=TEXT_MUTED
        )

    def _ejecutar_lexico(self, modo_todo: bool = False) -> None:
        resultado = ejecutar_analisis_lexico_codigo(
            codigo_fuente=self.editor_panel.obtener_codigo(),
            desarrollador=self.desarrollador_var.get(),
            nombre_archivo=self.editor_panel.obtener_nombre_archivo(),
        )

        lineas_err = [e["linea"] for e in resultado["errores"]]
        if lineas_err:
            self.editor_panel.resaltar_lineas_error(lineas_err)
        else:
            self.editor_panel.limpiar_resaltado_errores()

        self.diagnostics_panel.mostrar_resultados_lexicos(
            resultado, modo_ejecucion_todo=modo_todo
        )
        self.lbl_log_badge.configure(text=resultado["nombre_log"], text_color=ACCENT)


def launch_gui(archivo_inicial: str | None = "algoritmos/algoritmo1.go") -> None:
    """Inicia el bucle principal de la interfaz gráfica CustomTkinter."""
    GoAnalyzerApp(archivo_inicial=archivo_inicial).mainloop()
# =====================================================================
# FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
# =====================================================================

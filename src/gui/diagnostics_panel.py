"""
Panel derecho de la GUI:
1. Banner de Estado del Sistema (Superior).
2. Vista de Pestañas por fase (Tabla de Tokens, Reglas Sintáticas, Tabla de Símbolos).
3. Consola de Diagnóstico General (Inferior).

Autores:
    - Pablo Naranjo (@PabloNaranjoM)
    - Josué Pacheco (@JosuePach3co)
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable

import customtkinter as ctk

from .theme import (
    BG_BADGE,
    BG_EDITOR,
    BG_MAIN,
    BG_PANEL,
    BG_ROW_ALT,
    BORDER_PANEL,
    BORDER_SOFT,
    BTN_PRIMARY,
    BTN_SECONDARY,
    ERROR_FG,
    ERROR_ROW_BG,
    ESTADOS_BANNER,
    OK_FG,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    fuente_mono,
    fuente_ui,
)


class DiagnosticsPanel(ctk.CTkFrame):
    """Panel derecho de diagnóstico y resultados (55 % del ancho de trabajo)."""

    TAB_TOKENS = "Tabla de Tokens"
    TAB_SINTACTICO = "Reglas Sintácticas"
    TAB_SIMBOLOS = "Tabla de Símbolos"

    def __init__(
        self,
        master: Any,
        on_line_select: Callable[[int], None] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_line_select = on_line_select

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=2)

        self._construir_banner_estado()
        self._construir_vista_pestanas()
        self._construir_consola_inferior()
        self.limpiar_panel()

    # =====================================================================
    # INICIO APORTE: Pablo Naranjo (@PabloNaranjoM)
    # =====================================================================
    def _construir_banner_estado(self) -> None:
        self.banner_frame = ctk.CTkFrame(
            self,
            fg_color=BG_BADGE,
            border_color=BORDER_SOFT,
            border_width=1,
            corner_radius=8,
            height=46,
        )
        self.banner_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.banner_frame.grid_columnconfigure(1, weight=1)

        self.banner_dot = ctk.CTkLabel(
            self.banner_frame, text="●", font=fuente_ui(15)
        )
        self.banner_dot.grid(row=0, column=0, padx=(14, 8), pady=10, sticky="w")

        self.banner_msg = ctk.CTkLabel(
            self.banner_frame, text="", font=fuente_ui(12), anchor="w", justify="left"
        )
        self.banner_msg.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

        self.banner_badge_frame = ctk.CTkFrame(
            self.banner_frame, border_width=1, corner_radius=6
        )
        self.banner_badge_frame.grid(row=0, column=2, padx=(4, 12), pady=8, sticky="e")

        self.banner_badge = ctk.CTkLabel(
            self.banner_badge_frame, text="", font=fuente_mono(11, negrita=True)
        )
        self.banner_badge.pack(padx=10, pady=3)

    def actualizar_estado_banner(
        self, estado: str, mensaje_custom: str | None = None
    ) -> None:
        cfg = ESTADOS_BANNER.get(estado.upper(), ESTADOS_BANNER["IDLE"])
        self.banner_frame.configure(fg_color=cfg["bg"], border_color=cfg["border"])
        self.banner_dot.configure(text_color=cfg["fg"])
        self.banner_msg.configure(
            text=mensaje_custom or cfg["mensaje"], text_color=cfg["fg"]
        )
        self.banner_badge_frame.configure(
            fg_color=cfg["badge_bg"], border_color=cfg["border"]
        )
        self.banner_badge.configure(text=cfg["badge"], text_color=cfg["fg"])
    # =====================================================================
    # FIN APORTE: Pablo Naranjo (@PabloNaranjoM)
    # =====================================================================

    # =====================================================================
    # INICIO APORTE: Josué Pacheco (@JosuePach3co)
    # =====================================================================
    def _construir_vista_pestanas(self) -> None:
        container = ctk.CTkFrame(
            self,
            fg_color=BG_PANEL,
            border_color=BORDER_PANEL,
            border_width=1,
            corner_radius=8,
        )
        container.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(
            container,
            fg_color=BG_PANEL,
            segmented_button_fg_color=BG_MAIN,
            segmented_button_selected_color=BTN_PRIMARY[0],
            segmented_button_selected_hover_color=BTN_PRIMARY[1],
            segmented_button_unselected_color=BG_BADGE,
            segmented_button_unselected_hover_color=BTN_SECONDARY[0],
            text_color=TEXT_PRIMARY,
            corner_radius=8,
            border_width=0,
        )
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=8, pady=(4, 8))

        self.tab_tokens = self.tabview.add(self.TAB_TOKENS)
        self.tab_sintactico = self.tabview.add(self.TAB_SINTACTICO)
        self.tab_simbolos = self.tabview.add(self.TAB_SIMBOLOS)
        self.tabview._segmented_button.configure(font=fuente_ui(12))

        self._construir_tab_tokens()
        self._construir_tab_sintactico()
        self._construir_tab_simbolos()

    def _construir_tab_tokens(self) -> None:
        self.tab_tokens.grid_columnconfigure(0, weight=1)
        self.tab_tokens.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            self.tab_tokens, fg_color=BG_MAIN, corner_radius=6, height=28
        )
        header.grid(row=0, column=0, sticky="ew", padx=2, pady=(0, 6))
        header.grid_columnconfigure(0, weight=1)

        self.lbl_contador_tokens = ctk.CTkLabel(
            header,
            text="Tabla de Tokens (0)",
            font=fuente_ui(11),
            text_color=TEXT_SECONDARY,
        )
        self.lbl_contador_tokens.grid(row=0, column=0, padx=10, pady=3, sticky="w")

        self.lbl_resumen_tokens = ctk.CTkLabel(
            header,
            text="0 válidos • 0 errores léxicos",
            font=fuente_mono(11),
            text_color=TEXT_SECONDARY,
        )
        self.lbl_resumen_tokens.grid(row=0, column=1, padx=10, pady=3, sticky="e")

        tree_frame = ctk.CTkFrame(
            self.tab_tokens,
            fg_color=BG_EDITOR,
            border_color=BORDER_PANEL,
            border_width=1,
            corner_radius=6,
        )
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=2)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Tokens.Treeview",
            background=BG_EDITOR,
            foreground=TEXT_PRIMARY,
            fieldbackground=BG_EDITOR,
            borderwidth=0,
            relief="flat",
            font=fuente_mono(11),
            rowheight=26,
        )
        style.map(
            "Tokens.Treeview",
            background=[("selected", BTN_PRIMARY[0])],
            foreground=[("selected", "#FFFFFF")],
        )
        style.configure(
            "Tokens.Treeview.Heading",
            background=BG_PANEL,
            foreground=TEXT_SECONDARY,
            bordercolor=BORDER_PANEL,
            borderwidth=1,
            relief="flat",
            font=fuente_ui(10),
            padding=(8, 6),
        )
        style.map(
            "Tokens.Treeview.Heading",
            background=[("active", BTN_SECONDARY[0])],
            foreground=[("active", TEXT_PRIMARY)],
        )

        definicion_columnas = [
            ("indice", "#", 48, 40, False, "center"),
            ("categoria", "Categoría / Token", 210, 150, True, "w"),
            ("lexema", "Lexema", 180, 110, True, "w"),
            ("linea", "Línea", 70, 55, False, "center"),
            ("columna", "Columna", 80, 65, False, "center"),
        ]
        self.tree_tokens = ttk.Treeview(
            tree_frame,
            columns=[c[0] for c in definicion_columnas],
            show="headings",
            style="Tokens.Treeview",
            selectmode="browse",
        )
        for col, titulo, width, minw, stretch, anchor in definicion_columnas:
            self.tree_tokens.heading(col, text=titulo, anchor=anchor)
            self.tree_tokens.column(
                col, width=width, minwidth=minw, stretch=stretch, anchor=anchor
            )

        self.tree_tokens.tag_configure("even", background=BG_EDITOR, foreground=TEXT_PRIMARY)
        self.tree_tokens.tag_configure("odd", background=BG_ROW_ALT, foreground=TEXT_PRIMARY)
        self.tree_tokens.tag_configure("error", background=ERROR_ROW_BG, foreground=ERROR_FG)
        self.tree_tokens.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=2)

        scrollbar = ctk.CTkScrollbar(
            tree_frame,
            orientation="vertical",
            command=self.tree_tokens.yview,
            fg_color=BG_EDITOR,
            button_color=BORDER_PANEL,
            button_hover_color="#3B4252",
        )
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 2), pady=2)
        self.tree_tokens.configure(yscrollcommand=scrollbar.set)
        self.tree_tokens.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

    def _al_seleccionar_fila(self, _event: Any = None) -> None:
        if not self._on_line_select:
            return
        sel = self.tree_tokens.selection()
        if sel:
            valores = self.tree_tokens.item(sel[0], "values")
            if len(valores) >= 4:
                self._on_line_select(int(valores[3]))

    def _construir_tab_sintactico(self) -> None:
        self.tab_sintactico.grid_columnconfigure(0, weight=1)
        self.tab_sintactico.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            self.tab_sintactico, fg_color=BG_MAIN, corner_radius=6, height=28
        )
        header.grid(row=0, column=0, sticky="ew", padx=2, pady=(0, 6))
        header.grid_columnconfigure(0, weight=1)

        self.lbl_contador_sintactico = ctk.CTkLabel(
            header,
            text="Reglas Sintácticas (0)",
            font=fuente_ui(11),
            text_color=TEXT_SECONDARY,
        )
        self.lbl_contador_sintactico.grid(row=0, column=0, padx=10, pady=3, sticky="w")

        self.lbl_resumen_sintactico = ctk.CTkLabel(
            header,
            text="0 reglas validadas • 0 errores sintácticos",
            font=fuente_mono(11),
            text_color=TEXT_SECONDARY,
        )
        self.lbl_resumen_sintactico.grid(row=0, column=1, padx=10, pady=3, sticky="e")

        tree_frame = ctk.CTkFrame(
            self.tab_sintactico,
            fg_color=BG_EDITOR,
            border_color=BORDER_PANEL,
            border_width=1,
            corner_radius=6,
        )
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=2)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        columnas_sin = [
            ("estado", "Estado", 85, 70, False, "center"),
            ("linea", "Línea", 70, 55, False, "center"),
            ("regla", "Regla Gramatical", 185, 140, False, "w"),
            ("detalle", "Detalle de Validación LALR(1)", 360, 220, True, "w"),
        ]
        self.tree_sintactico = ttk.Treeview(
            tree_frame,
            columns=[c[0] for c in columnas_sin],
            show="headings",
            style="Tokens.Treeview",
            selectmode="browse",
        )
        for col, titulo, width, minw, stretch, anchor in columnas_sin:
            self.tree_sintactico.heading(col, text=titulo, anchor=anchor)
            self.tree_sintactico.column(
                col, width=width, minwidth=minw, stretch=stretch, anchor=anchor
            )

        self.tree_sintactico.tag_configure("even", background=BG_EDITOR, foreground=OK_FG)
        self.tree_sintactico.tag_configure("odd", background=BG_ROW_ALT, foreground=OK_FG)
        self.tree_sintactico.tag_configure("error", background=ERROR_ROW_BG, foreground=ERROR_FG)
        self.tree_sintactico.grid(row=0, column=0, sticky="nsew", padx=(2, 0), pady=2)

        scrollbar = ctk.CTkScrollbar(
            tree_frame,
            orientation="vertical",
            command=self.tree_sintactico.yview,
            fg_color=BG_EDITOR,
            button_color=BORDER_PANEL,
            button_hover_color="#3B4252",
        )
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 2), pady=2)
        self.tree_sintactico.configure(yscrollcommand=scrollbar.set)
        self.tree_sintactico.bind("<<TreeviewSelect>>", self._al_seleccionar_fila_sintactico)

    def _al_seleccionar_fila_sintactico(self, _event: Any = None) -> None:
        if not self._on_line_select:
            return
        sel = self.tree_sintactico.selection()
        if sel:
            valores = self.tree_sintactico.item(sel[0], "values")
            if len(valores) >= 2:
                self._on_line_select(int(valores[1]))

    def _construir_tab_simbolos(self) -> None:
        self.tab_simbolos.grid_columnconfigure(0, weight=1)
        self.tab_simbolos.grid_rowconfigure(0, weight=1)
        ctk.CTkLabel(
            self.tab_simbolos,
            text="Tabla de Símbolos y Análisis Semántico — Pendiente para el Avance 3",
            font=fuente_ui(12, negrita=False),
            text_color=TEXT_SECONDARY,
        ).grid(row=0, column=0, padx=20, pady=20)

    def _construir_consola_inferior(self) -> None:
        frame = ctk.CTkFrame(
            self,
            fg_color=BG_PANEL,
            border_color=BORDER_PANEL,
            border_width=1,
            corner_radius=8,
        )
        frame.grid(row=2, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(frame, fg_color="transparent", height=30)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(8, 4))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="CONSOLA DE DIAGNÓSTICO (LÉXICO / SINTÁCTICO / SEMÁNTICO)",
            font=fuente_ui(11),
            text_color=TEXT_SECONDARY,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header,
            text="Motor: PLY (Python Lex-Yacc)",
            font=fuente_mono(11),
            text_color=TEXT_SECONDARY,
        ).grid(row=0, column=1, sticky="e")

        self.consola_textbox = ctk.CTkTextbox(
            frame,
            fg_color=BG_EDITOR,
            text_color=TEXT_PRIMARY,
            border_color=BORDER_PANEL,
            border_width=1,
            corner_radius=6,
            font=fuente_mono(12),
            wrap="word",
            height=135,
        )
        self.consola_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        inner = self.consola_textbox._textbox
        inner.tag_config("ok", foreground=OK_FG)
        inner.tag_config("error", foreground=ERROR_FG)
        inner.tag_config("info", foreground=TEXT_SECONDARY)
        self.consola_textbox.configure(state="disabled")

    def _actualizar_contador_tokens(self, total_filas: int) -> None:
        txt_tokens = f"Tabla de Tokens ({total_filas})"
        self.lbl_contador_tokens.configure(text=txt_tokens)
        botones = self.tabview._segmented_button._buttons_dict
        if self.TAB_TOKENS in botones:
            botones[self.TAB_TOKENS].configure(text=txt_tokens)

    def _actualizar_contador_sintactico(self, total_filas: int) -> None:
        txt_sin = f"Reglas Sintácticas ({total_filas})"
        self.lbl_contador_sintactico.configure(text=txt_sin)
        botones = self.tabview._segmented_button._buttons_dict
        if self.TAB_SINTACTICO in botones:
            botones[self.TAB_SINTACTICO].configure(text=txt_sin)

    def _escribir_consola(self, segmentos: list[tuple[str, str]]) -> None:
        self.consola_textbox.configure(state="normal")
        self.consola_textbox.delete("1.0", "end")
        inner = self.consola_textbox._textbox
        for texto, tag in segmentos:
            inner.insert("end", texto, tag)
        self.consola_textbox.configure(state="disabled")

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def mostrar_resultados_lexicos(
        self, resultado: dict[str, Any], modo_ejecucion_todo: bool = False
    ) -> None:
        tokens: list[dict[str, Any]] = resultado["tokens"]
        errores: list[dict[str, Any]] = resultado["errores"]
        tiene_errores = bool(errores)

        if tiene_errores:
            self.actualizar_estado_banner("ERROR_LEXICO")
        else:
            msg = (
                "ESTADO DEL SISTEMA: Análisis léxico, sintáctico y semántico completado sin errores."
                if modo_ejecucion_todo
                else None
            )
            self.actualizar_estado_banner("VALIDO", mensaje_custom=msg)

        self.tree_tokens.delete(*self.tree_tokens.get_children())
        filas = [
            (t["linea"], t["columna"], False, str(t["indice"]), t["categoria"], str(t["valor"]))
            for t in tokens
        ] + [
            (e["linea"], e["columna"], True, "-", "ERROR_LEXICO", str(e["caracter"]))
            for e in errores
        ]
        filas.sort(key=lambda r: (r[0], r[1]))

        for pos, (linea, col, es_err, idx, cat, lexema) in enumerate(filas):
            tag = "error" if es_err else ("even" if pos % 2 == 0 else "odd")
            self.tree_tokens.insert(
                "", "end", values=(idx, cat, lexema, linea, col), tags=(tag,)
            )

        self.lbl_resumen_tokens.configure(
            text=f"{len(tokens)} válidos • {len(errores)} errores léxicos",
            text_color=ERROR_FG if tiene_errores else OK_FG,
        )
        self._actualizar_contador_tokens(len(filas))

        if not tiene_errores:
            segmentos = [
                (f"[OK] Análisis Léxico: {len(tokens)} tokens reconocidos correctamente.\n", "ok")
            ]
            if modo_ejecucion_todo:
                segmentos.append((
                    "[INFO] Ejecutando fase de Análisis Sintáctico LALR(1)...\n",
                    "info",
                ))
        else:
            segmentos = [(f"{e['mensaje'].rstrip('.')}.\n", "error") for e in errores]
        self._escribir_consola(segmentos)

    def mostrar_resultados_sintacticos(
        self, resultado: dict[str, Any], modo_ejecucion_todo: bool = False
    ) -> None:
        reglas: list[dict[str, Any]] = resultado["reglas"]
        errores_sin: list[dict[str, Any]] = resultado["errores"]
        errores_lex: list[dict[str, Any]] = resultado.get("errores_lexicos", [])
        tokens: list[dict[str, Any]] = resultado.get("tokens", [])

        if errores_lex:
            self.actualizar_estado_banner("ERROR_LEXICO")
        elif errores_sin:
            self.actualizar_estado_banner("ERROR_SINTACTICO")
        else:
            msg = (
                "ESTADO DEL SISTEMA: Análisis léxico y sintáctico completado sin errores."
                if modo_ejecucion_todo
                else "ESTADO DEL SISTEMA: Análisis sintáctico LALR(1) completado sin errores."
            )
            self.actualizar_estado_banner("VALIDO", mensaje_custom=msg)

        self.tree_sintactico.delete(*self.tree_sintactico.get_children())
        filas = [
            (
                r["linea"],
                0,
                False,
                "✓ VÁLIDA",
                r["regla"],
                f"✓ [Línea {r['linea']}] Regla '{r['regla']}' validada.",
            )
            for r in reglas
        ] + [
            (
                e["linea"],
                1,
                True,
                "✕ ERROR",
                "p_error (LALR)",
                f"✕ [Línea {e['linea']}, Col {e['columna']}] Token inesperado '{e['token']}'",
            )
            for e in errores_sin
        ]
        filas.sort(key=lambda r: (r[0], r[1]))

        for pos, (linea, _prio, es_err, estado_txt, regla_txt, detalle_txt) in enumerate(filas):
            tag = "error" if es_err else ("even" if pos % 2 == 0 else "odd")
            self.tree_sintactico.insert(
                "", "end", values=(estado_txt, linea, regla_txt, detalle_txt), tags=(tag,)
            )

        tiene_err_sin = bool(errores_sin)
        self.lbl_resumen_sintactico.configure(
            text=f"{len(reglas)} reglas validadas • {len(errores_sin)} errores sintácticos",
            text_color=ERROR_FG if tiene_err_sin else OK_FG,
        )
        self._actualizar_contador_sintactico(len(filas))

        segmentos: list[tuple[str, str]] = []
        if modo_ejecucion_todo:
            if not errores_lex:
                segmentos.append(
                    (f"[OK] Análisis Léxico: {len(tokens)} tokens reconocidos correctamente.\n", "ok")
                )
            else:
                for el in errores_lex:
                    segmentos.append((f"{el['mensaje'].rstrip('.')}.\n", "error"))

        if not errores_sin and not errores_lex:
            segmentos.append((
                f"[OK] Análisis Sintáctico: Estructura gramatical LALR(1) válida ({len(reglas)} reglas verificadas).\n",
                "ok",
            ))
            if modo_ejecucion_todo:
                segmentos.append((
                    "[INFO] Análisis Semántico: Pendiente de integración (Avance 3).\n",
                    "info",
                ))
        else:
            for es in errores_sin:
                segmentos.append((f"{es['mensaje']}\n", "error"))

        self._escribir_consola(segmentos)
        if not modo_ejecucion_todo or tiene_err_sin:
            self.tabview.set(self.TAB_SINTACTICO)

    def limpiar_panel(self) -> None:
        self.actualizar_estado_banner("IDLE")
        self.tree_tokens.delete(*self.tree_tokens.get_children())
        self.tree_sintactico.delete(*self.tree_sintactico.get_children())
        self.lbl_resumen_tokens.configure(
            text="0 válidos • 0 errores léxicos", text_color=TEXT_SECONDARY
        )
        self.lbl_resumen_sintactico.configure(
            text="0 reglas validadas • 0 errores sintácticos", text_color=TEXT_SECONDARY
        )
        self._actualizar_contador_tokens(0)
        self._actualizar_contador_sintactico(0)
        self._escribir_consola([(
            "Consola lista. Cargue un archivo .go o escriba código en el editor y presione 'Léxico', 'Sintáctico' o '▶ Ejecutar Todo'.\n",
            "info",
        )])
        self.tabview.set(self.TAB_TOKENS)
    # =====================================================================
    # FIN APORTE: Josué Pacheco (@JosuePach3co)
    # =====================================================================

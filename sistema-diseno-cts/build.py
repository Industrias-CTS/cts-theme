#!/usr/bin/env python3
"""Genera las hojas del Sistema de Diseño CTS (base: cts-manager / W-Flow).

Uso: `python3 build.py` → escribe `artboards/*.dc.html` y `canvas.json`.
Todos los valores son literales copiados de cts-manager
(frontend/src/theme/ctsTheme.ts y componentes; se cita la fuente en cada hoja).
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / "artboards"

# ── Tokens (ctsTheme.ts, modo claro salvo indicación) ─────────────────────
BLUE = "#0065BB"; BLUE_L = "#29ABE2"; BLUE_D = "#004696"
NAVY = "#1a2236"; MUTED = "#5a6a80"; BORDER = "#dde3ec"; INPUT_BD = "#d0d8e4"
SOFT = "#f0f4f9"; PAPER = "#ffffff"
RED = "#e2445c"; ORANGE = "#fdab3d"; GREEN = "#00c875"
DATA8 = ["#0065BB", "#29ABE2", "#00c875", "#fdab3d", "#e2445c", "#a25ddc", "#ff642e", "#579bfc"]
W = 1440

HELMET = f"""<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700;900&amp;display=swap">
  <style>
    body {{ margin: 0; font-family: 'Titillium Web', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: {NAVY}; background: {SOFT}; -webkit-font-smoothing: antialiased; }}
    a {{ color: {BLUE}; }} a:hover {{ color: {BLUE_D}; }}
    * {{ box-sizing: border-box; }}
  </style>
</helmet>"""

def page(body, h):
    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
{HELMET}
<div style="width: {W}px; height: {h}px; background: {SOFT}; padding: 40px 48px; display: flex; flex-direction: column; gap: 24px; overflow: hidden;">
{body}
</div>
</x-dc>
</body>
</html>
"""

def header(title, subtitle, source):
    return f"""<div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 24px;">
  <div style="display: flex; flex-direction: column; gap: 4px;">
    <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.32em; text-transform: uppercase; color: {BLUE};">Sistema de Diseño CTS</span>
    <h1 style="margin: 0; font-size: 30px; font-weight: 700; letter-spacing: -0.5px; color: {NAVY};">{title}</h1>
    <span style="font-size: 14px; color: {MUTED};">{subtitle}</span>
  </div>
  <span style="font-size: 11px; color: {MUTED}; font-family: monospace; padding-bottom: 6px;">{source}</span>
</div>"""

def card(title, inner, grow=False):
    g = "flex-grow: 1; " if grow else ""
    return (f'<section style="{g}background: {PAPER}; border: 1px solid {BORDER}; border-radius: 12px; padding: 20px 24px; display: flex; flex-direction: column; gap: 14px;">'
            f'<span style="font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {MUTED};">{title}</span>{inner}</section>')

def row(gap=16, wrap=False):
    return f'display: flex; gap: {gap}px; align-items: flex-start;' + (' flex-wrap: wrap;' if wrap else '')

def swatch(hex_, name, note="", w=150, light_text=False):
    fg = "#ffffff" if not light_text else NAVY
    return f"""<div style="width: {w}px; border: 1px solid {BORDER}; border-radius: 10px; overflow: hidden; background: {PAPER};">
  <div style="height: 52px; background: {hex_}; display: flex; align-items: flex-end; padding: 6px 10px;"><span style="font-size: 11px; font-weight: 700; color: {fg}; font-family: monospace;">{hex_}</span></div>
  <div style="padding: 8px 10px; display: flex; flex-direction: column; gap: 1px;">
    <span style="font-size: 12.5px; font-weight: 700; color: {NAVY};">{name}</span>
    <span style="font-size: 11px; color: {MUTED};">{note}</span>
  </div>
</div>"""

def spec(label, value):
    return (f'<div style="display: flex; flex-direction: column; gap: 1px; min-width: 0;">'
            f'<span style="font-size: 11px; font-weight: 600; color: {MUTED};">{label}</span>'
            f'<span style="font-size: 13px; font-weight: 600; color: {NAVY}; font-family: monospace;">{value}</span></div>')

def table(headers, rows_, widths=None):
    ths = "".join(f'<div style="padding: 9px 12px; font-size: 11px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: #ffffff; border-right: 1px solid rgba(255,255,255,0.12);">{h}</div>' for h in headers)
    cols = widths or f"repeat({len(headers)}, minmax(0, 1fr))"
    trs = ""
    for r in rows_:
        tds = "".join(f'<div style="padding: 8px 12px; font-size: 13px; color: {NAVY}; border-right: 1px solid {BORDER}; border-bottom: 1px solid {BORDER}; display: flex; align-items: center; min-height: 38px;">{c}</div>' for c in r)
        trs += f'<div style="display: grid; grid-template-columns: {cols};">{tds}</div>'
    return (f'<div style="border: 1px solid {BORDER}; border-radius: 10px; overflow: hidden; background: {PAPER};">'
            f'<div style="display: grid; grid-template-columns: {cols}; background: {BLUE};">{ths}</div>{trs}</div>')

def mono(t):
    return f'<span style="font-family: monospace; font-size: 12px; background: {SOFT}; border: 1px solid {BORDER}; border-radius: 4px; padding: 1px 6px;">{t}</span>'

# ═══ 1. Portada ═══════════════════════════════════════════════════════════
def v_portada():
    principios = [
        ("Riel azul como identidad", f"El sidebar es una losa {BLUE} de 256 px sobre contenido claro. Es el identificador visual más fuerte del sistema."),
        ("Bordes estructuran, no sombras", f"Hairlines 1px {BORDER} en todo; la elevación se reserva para capas flotantes (menús, diálogos). Las cards son planas."),
        ("Sombras azuladas en lo flotante", "En claro, menús, diálogos y el botón contained llevan sombra con tinte de marca rgba(0,101,187,…); las elevaciones base del tema son negras suaves."),
        ("Color funcional, no decorativo", "El chrome es azul + gris. La paleta de 8 colores queda para datos del usuario (estados, grupos, gráficos)."),
        ("Densidad de hoja de cálculo", "Filas 38–40 px, texto 13 px, cabeceras 11 px uppercase, controles 32 px. El gutter de página es 24 px."),
        ("Una sola voz tipográfica", "Titillium Web en todo, pesos 300–900; etiquetas en 600/700. Tamaños fraccionales (9.5, 12.5, 13.5) son intencionales."),
    ]
    ps = "".join(f'<div style="display: flex; flex-direction: column; gap: 4px; width: 400px;"><span style="font-size: 14.5px; font-weight: 700; color: {NAVY};">{t}</span><span style="font-size: 13px; line-height: 1.5; color: {MUTED};">{d}</span></div>' for t, d in principios)
    hojas = ["Colores", "Modo oscuro", "Tipografía", "Forma y espacio", "Controles", "Tablas y listas", "Navegación"]
    idx = "".join(f'<div style="display: flex; align-items: center; gap: 10px; font-size: 13.5px; font-weight: 600; color: {NAVY};"><span style="width: 22px; height: 22px; border-radius: 6px; background: {BLUE}; color: #fff; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center;">{i+1}</span>{n}</div>' for i, n in enumerate(hojas))
    body = f"""<div style="background: {BLUE}; border-radius: 16px; padding: 40px 48px; display: flex; align-items: center; gap: 32px;">
  <img src="logo-cts-blanco.png" alt="CTS" style="width: 84px; height: auto;">
  <div style="display: flex; flex-direction: column; gap: 6px;">
    <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.32em; text-transform: uppercase; color: rgba(255,255,255,0.7);">Industrias CTS</span>
    <span style="font-size: 34px; font-weight: 900; letter-spacing: 2px; color: #ffffff; line-height: 1.1;">Sistema de Diseño</span>
    <span style="font-size: 14px; color: rgba(255,255,255,0.75);">Base común para todas las aplicaciones (W-Flow, E-Panel y siguientes). Fuente de verdad: cts-manager · frontend/src/theme/ctsTheme.ts</span>
  </div>
</div>
{card("Principios", f'<div style="{row(28)} flex-wrap: wrap; row-gap: 20px;">{ps}</div>')}
<div style="{row(24)}">
  {card("Hojas de esta guía", f'<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px 32px;">{idx}</div>', grow=True)}
  {card("Stack de referencia", f'<div style="display: flex; flex-direction: column; gap: 10px;">{spec("UI", "React 19 + MUI v7 (createTheme + sx)")}{spec("Fuente", "Titillium Web · Google Fonts · 300/400/600/700/900")}{spec("Modo por defecto", "claro · oscuro implementado y conmutable")}{spec("Radio base", "shape.borderRadius: 10")}{spec("Espaciado", "múltiplos de 8 px (MUI spacing)")}</div>', grow=True)}
</div>"""
    return page(f'{header("Portada", "Qué es y cómo usar esta guía", "cts-manager@main")}{body}', 900)

# ═══ 2. Colores ═══════════════════════════════════════════════════════════
def v_colores():
    marca = "".join([
        swatch(BLUE, "primary.main", "azul CTS — acciones, rail, énfasis"),
        swatch(BLUE_D, "primary.dark", "hover de contained"),
        swatch(BLUE_L, "primary.light / secondary", "acentos fríos, info"),
        swatch("#1a8ab8", "secondary.dark", "hover de secondary"),
        swatch("#003B8E", "blueGrad1", "declarado, sin uso — no usar"),
    ])
    superficie = "".join([
        swatch(SOFT, "background.default", "fondo de aplicación", light_text=True),
        swatch(PAPER, "background.paper", "cards, menús, diálogos", light_text=True),
        swatch(BORDER, "divider", "hairline universal", light_text=True),
        swatch(INPUT_BD, "borde de inputs", "fieldset 1.5px", light_text=True),
        swatch(NAVY, "text.primary", "texto principal"),
        swatch(MUTED, "text.secondary", "etiquetas, texto de apoyo"),
    ])
    sem = "".join([
        swatch(RED, "error.main", "errores, eliminar"),
        swatch(ORANGE, "warning.main", "avisos, badges beta"),
        swatch(GREEN, "success.main", "éxito, aprobar"),
        swatch(BLUE_L, "info.main", "informativo"),
    ])
    datos = "".join(swatch(c, f"data-{i+1}", "", w=118) for i, c in enumerate(DATA8))
    states = table(["Token", "Valor (claro)", "Uso"], [
        ["action.hover", mono("rgba(0,101,187,0.05)"), "hover de filas y superficies"],
        ["action.selected", mono("rgba(0,101,187,0.1)"), "selección, chips activos"],
        ["hover de fila de tabla", mono("#f7fafd"), "sólido a propósito (celdas sticky)"],
        ["celda de solo lectura", mono("rgba(15,23,42,0.035)"), "tinte de bloqueo"],
        ["fallback de estado", mono("#c4c4c4"), "status sin valor"],
    ], "220px 320px 1fr")
    body = f"""{card("Marca", f'<div style="{row(16, wrap=True)}">{marca}</div>')}
{card("Superficie y texto (modo claro)", f'<div style="{row(16, wrap=True)}">{superficie}</div>')}
<div style="{row(24)}">
  {card("Semánticos", f'<div style="{row(16, wrap=True)}">{sem}</div>', grow=True)}
</div>
{card("Paleta de datos — reservada para contenido del usuario (estados, grupos, tableros, gráficos), nunca para chrome", f'<div style="{row(12, wrap=True)}">{datos}</div>')}
{card("Estados de interacción", states)}"""
    return page(f'{header("Colores", "Marca, superficie, semánticos, datos y estados", "ctsTheme.ts:4-49")}{body}', 1280)

# ═══ 3. Modo oscuro ═══════════════════════════════════════════════════════
def v_oscuro():
    dk = "".join([
        swatch("#2A3547", "background.default", "fondo de aplicación"),
        swatch("#253662", "background.paper", "cards — MÁS CLARO que el fondo"),
        swatch("#2d3c53", "cabecera de tabla / grupo", "superficies de grid"),
        swatch("#e8edf4", "text.primary", "", light_text=True),
        swatch("#a6b4c8", "text.secondary", "", light_text=True),
        swatch("#253662", "sidebar (rail)", "sustituye al azul de marca"),
    ])
    sem = "".join([
        swatch("#ef4444", "error.main", ""),
        swatch("#f59e0b", "warning.main", ""),
        swatch("#22c55e", "success.main", ""),
        swatch("#06b6d4", "info.main", ""),
    ])
    reglas = table(["Regla", "Valor"], [
        ["primary.main NO cambia", mono("#0065BB") + " en ambos modos"],
        ["divider / bordes", mono("rgba(74,144,226,0.12)") + " — azul translúcido, no gris"],
        ["borde de inputs", mono("rgba(74,144,226,0.25)") + " · hover " + mono("rgba(41,171,226,0.5)")],
        ["action.hover / selected", mono("rgba(74,144,226,0.08)") + " / " + mono("rgba(74,144,226,0.16)")],
        ["hover de fila", mono("#2f435e") + " · selección " + mono("#2f476d")],
        ["sombras", "negras, más profundas: elev1 " + mono("0 1px 4px rgba(0,0,0,0.4)")],
        ["backgroundImage", mono("none") + " en Paper/Card/Dialog (MUI añade gradiente por defecto)"],
        ["scrollbars", mono("#3d4f6f") + " sobre " + mono("#253662")],
    ], "300px 1fr")
    body = f"""{card("Superficie y texto (modo oscuro)", f'<div style="{row(16, wrap=True)}">{dk}</div>')}
{card("Semánticos (oscuro)", f'<div style="{row(16, wrap=True)}">{sem}</div>')}
{card("Reglas del modo oscuro", reglas)}"""
    return page(f'{header("Modo oscuro", "Equivalencias y reglas — el papel es más claro que el fondo (elevación invertida)", "ctsTheme.ts:17-49")}{body}', 1100)

# ═══ 4. Tipografía ════════════════════════════════════════════════════════
def v_tipografia():
    pesos = "".join(f'<div style="display: flex; flex-direction: column; gap: 2px; width: 150px;"><span style="font-size: 26px; font-weight: {wgt}; color: {NAVY};">Aa 123</span><span style="font-size: 11px; color: {MUTED};">{wgt} · {name}</span></div>'
                    for wgt, name in [(300, "Light"), (400, "Regular"), (600, "SemiBold"), (700, "Bold"), (900, "Black — wordmark")])
    escala = table(["Variante", "Tamaño / interlineado", "Peso", "Uso"], [
        ["h1–h5", "MUI por defecto", "700", "títulos; h1 tracking -0.5px, h2 -0.25px"],
        ["h6", "MUI por defecto", "600", "subtítulos de sección"],
        ["subtitle1", "1rem / 1.4", "600", "encabezados de grupo"],
        ["subtitle2", "13px", "600", "títulos menores"],
        ["body1", "15px / 1.6", "400", "texto base"],
        ["body2", "13px / 1.5", "400", "texto denso (tablas, filas)"],
        ["button", "heredado", "600", "tracking 0.01em, sin uppercase"],
        ["caption", "12px", "400", "tracking 0.01em"],
        ["overline", "11px", "600", "tracking 0.08em, uppercase"],
    ], "140px 220px 90px 1fr")
    micro = table(["Contexto", "Especificación"], [
        ["Cabecera de tabla", "11px · 600 · uppercase · tracking 0.06em · blanco sobre azul"],
        ["Título de sección del sidebar", "10px · 700 · uppercase · tracking 0.1em · opacity 0.45"],
        ["Eyebrow / micro-etiqueta", "11px · 700 · uppercase · tracking 0.32em · color acento"],
        ["Etiqueta de nav", "13.5px · 600"],
        ["Fila de datos", "13px · 400–600"],
        ["Tamaños fraccionales", "9.5 · 10.5 · 12.5 · 13.5 · 15.5 px — intencionales, no redondear"],
    ], "300px 1fr")
    body = f"""{card("Familia única — Titillium Web", f'<div style="display: flex; flex-direction: column; gap: 14px;"><span style="font-size: 22px; color: {NAVY};">Gestión de flujos de trabajo — 0123456789</span><div style="{row(24, wrap=True)}">{pesos}</div><div style="{row(24)}">{spec("Carga", "Google Fonts · wght 300;400;600;700;900")}{spec("Fallback", "-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif")}{spec("Suavizado", "-webkit-font-smoothing: antialiased")}</div></div>')}
{card("Escala tipográfica (MUI typography)", escala)}
{card("Micro-tipografía", micro)}"""
    return page(f'{header("Tipografía", "Una sola familia, pesos amplios, etiquetas anchas y en mayúsculas", "ctsTheme.ts:51-71")}{body}', 1240)

# ═══ 5. Forma y espacio ═══════════════════════════════════════════════════
def v_forma():
    def rbox(r, label):
        return f'<div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 96px; height: 64px; background: {SOFT}; border: 1.5px solid {BLUE}; border-radius: {r}px;"></div><span style="font-size: 12px; font-weight: 700; color: {NAVY};">{r}px</span><span style="font-size: 11px; color: {MUTED}; text-align: center;">{label}</span></div>'
    radios = "".join([rbox(6, "chips, menu-item, tooltip"), rbox(8, "botones, inputs, list-item"), rbox(10, "menús, tablas (base)"), rbox(12, "cards, paper"), rbox(14, "diálogos"), rbox(30, "diálogos destacados (borderRadius: 3)"),
                      f'<div style="display: flex; flex-direction: column; align-items: center; gap: 6px;"><div style="width: 96px; height: 40px; margin-top: 12px; background: {SOFT}; border: 1.5px solid {BLUE}; border-radius: 99px;"></div><span style="font-size: 12px; font-weight: 700; color: {NAVY};">99px</span><span style="font-size: 11px; color: {MUTED};">píldoras y badges</span></div>'])
    bordes = table(["Grosor", "Uso"], [
        ["1px", f"hairline universal — divisores, cards, tablas ({mono(BORDER)})"],
        ["1.5px", "énfasis: fieldset de inputs, botones outlined, cards seleccionables"],
        ["2px", "subrayado de tabs, avatar del rail"],
        ["3px", "nav activo (borde izq.), indicadores de drop, acento de tipo de columna"],
        ["4px", "riel de color de grupo / tablero"],
    ], "110px 1fr")
    def shbox(sh, label, note):
        return f'<div style="display: flex; flex-direction: column; align-items: center; gap: 8px; width: 180px;"><div style="width: 150px; height: 64px; background: {PAPER}; border: 1px solid {BORDER}; border-radius: 12px; box-shadow: {sh};"></div><span style="font-size: 12px; font-weight: 700; color: {NAVY};">{label}</span><span style="font-size: 10.5px; color: {MUTED}; text-align: center; font-family: monospace;">{note}</span></div>'
    sombras = "".join([
        shbox("none", "card (defecto)", "borde, sin sombra"),
        shbox("0 1px 4px rgba(0,0,0,0.06)", "elevación 1", "0 1px 4px rgba(0,0,0,0.06)"),
        shbox("0 2px 8px rgba(0,101,187,0.3)", "botón contained", "0 2px 8px rgba(0,101,187,0.3)"),
        shbox("0 8px 24px rgba(0,101,187,0.15)", "menú", "0 8px 24px rgba(0,101,187,0.15)"),
        shbox("0 24px 64px rgba(0,101,187,0.18)", "diálogo", "0 24px 64px rgba(0,101,187,0.18)"),
        shbox("4px 0 20px rgba(0,0,0,0.2)", "sidebar", "4px 0 20px rgba(0,0,0,0.2)"),
    ])
    dens = table(["Elemento", "Alto"], [
        ["Fila de tabla / celda", "38px (texto 13px, padding 0)"],
        ["Fila de grid / cabecera de columna", "40px"],
        ["Cabecera de grupo", "44px · resumen 36px"],
        ["Control de toolbar (TextField, botón)", "32px"],
        ["Ítem de navegación", "34px"],
        ["Selector de workspace / búsqueda del rail", "42px / 34px"],
        ["Chip", "24px (variantes 18–20px)"],
        ["Campo de edición en línea", "26px"],
    ], "380px 1fr")
    anim = table(["Duración", "Uso"], [
        ["0.12s", "micro: opacidad de botones ocultos, swatches"],
        ["0.15s", "nav, list-items, menú (background), hovers de fila"],
        ["0.2s", "botones (all), focus ring de inputs"],
        ["0.25s", "colapso del sidebar, cambio de tema"],
        ["ease global", mono("cubic-bezier(0.32, 0.72, 0, 1)")],
    ], "140px 1fr")
    body = f"""{card("Radios — por nivel de elevación", f'<div style="{row(28, wrap=True)}">{radios}</div>')}
{card("Bordes — los bordes estructuran", bordes)}
{card("Sombras — azuladas en claro, reservadas a capas flotantes", f'<div style="{row(16, wrap=True)}">{sombras}</div>')}
<div style="{row(24)}">
  <div style="flex: 1; display: flex; flex-direction: column; gap: 24px;">{card("Densidad", dens)}</div>
  <div style="flex: 1; display: flex; flex-direction: column; gap: 24px;">{card("Animación", anim)}{card("Espaciado", f'<div style="display: flex; flex-direction: column; gap: 10px;">{spec("Base", "8px (spacing MUI); medios pasos 2/4/6px permitidos")}{spec("Gutter de página", "24px (p: 3)")}{spec("Separación de cards", "16–24px")}</div>')}</div>
</div>"""
    return page(f'{header("Forma y espacio", "Radios, bordes, sombras, densidad y movimiento", "ctsTheme.ts:73-119 · Sidebar.tsx · BoardGridV2.tsx")}{body}', 1460)

# ═══ 6. Controles ═════════════════════════════════════════════════════════
def v_controles():
    def btn(label, bg, fg, sh="", bd="", extra=""):
        return f'<div style="height: 36px; padding: 0 16px; border-radius: 8px; background: {bg}; color: {fg}; font-size: 13.5px; font-weight: 600; display: flex; align-items: center; justify-content: center; {"box-shadow: " + sh + ";" if sh else ""}{"border: " + bd + ";" if bd else ""}{extra}">{label}</div>'
    botones = f"""<div style="{row(14, wrap=True)}">
  {btn("Contained", BLUE, "#fff", "0 2px 8px rgba(0,101,187,0.3)")}
  {btn("Hover", BLUE_D, "#fff", "0 4px 12px rgba(0,101,187,0.4)")}
  {btn("Secondary", BLUE_L, "#fff", "0 2px 8px rgba(41,171,226,0.3)")}
  {btn("Outlined", PAPER, MUTED, "", f"1.5px solid {INPUT_BD}")}
  {btn("Outlined hover", PAPER, BLUE, "", f"1.5px solid {BLUE}")}
  <div style="height: 28px; padding: 0 12px; border-radius: 8px; background: {PAPER}; border: 1.5px solid {INPUT_BD}; color: {MUTED}; font-size: 13px; font-weight: 600; display: flex; align-items: center;">small · 4px 12px</div>
  <div style="height: 34px; padding: 0 16px; border-radius: 99px; background: rgba(0,101,187,0.07); border: 1px solid rgba(0,101,187,0.3); color: {BLUE}; font-size: 13.5px; font-weight: 700; display: flex; align-items: center;">Píldora / enlace</div>
</div>
<span style="font-size: 12px; color: {MUTED};">Siempre {mono("textTransform: none")} · peso 600 · radio 8 · transición {mono("all 0.2s")}. El contained es el único elemento sólido con sombra.</span>"""
    def input_(label, bd, extra=""):
        return f'<div style="width: 210px; display: flex; flex-direction: column; gap: 4px;"><span style="font-size: 11px; font-weight: 600; color: {MUTED};">{label}</span><div style="height: 40px; border: 1.5px solid {bd}; border-radius: 8px; background: {PAPER}; padding: 0 12px; display: flex; align-items: center; font-size: 13px; color: {MUTED}; {extra}">Valor</div></div>'
    inputs = f"""<div style="{row(16, wrap=True)}">
  {input_("Default — 1.5px #d0d8e4", INPUT_BD)}
  {input_("Hover — borde primario", BLUE)}
  {input_("Focus — anillo 3px", BLUE, f"box-shadow: 0 0 0 3px rgba(0,101,187,0.15);")}
  {input_("Toolbar — 32px · 13px", INPUT_BD, "height: 32px;")}
</div>"""
    chips = f"""<div style="{row(10, wrap=True)} align-items: center;">
  <div style="height: 24px; padding: 0 10px; border-radius: 6px; background: rgba(0,101,187,0.1); color: {BLUE}; font-size: 12px; font-weight: 600; display: flex; align-items: center;">Chip 24px</div>
  <div style="height: 20px; padding: 0 8px; border-radius: 6px; background: {GREEN}20; color: {GREEN}; font-size: 11px; font-weight: 700; display: flex; align-items: center;">conteo 20px</div>
  <div style="height: 18px; padding: 0 8px; border-radius: 6px; background: {ORANGE}; color: #fff; font-size: 10.5px; font-weight: 700; display: flex; align-items: center;">BETA</div>
  <div style="height: 20px; padding: 0 9px; border-radius: 99px; background: {RED}; color: #fff; font-size: 10px; font-weight: 800; letter-spacing: 0.4px; display: flex; align-items: center;">NUEVO</div>
  <span style="font-size: 12px; color: {MUTED};">tinte = color + sufijo 20/18 hex · texto en el color pleno</span>
</div>"""
    tabs = f"""<div style="display: flex; border-bottom: 2px solid {BORDER};">
  <div style="padding: 8px 12px; margin-bottom: -2px; font-size: 13px; font-weight: 700; color: {BLUE}; border-bottom: 2px solid {BLUE};">Activa</div>
  <div style="padding: 8px 12px; margin-bottom: -2px; font-size: 13px; font-weight: 500; color: {MUTED};">Inactiva</div>
  <div style="padding: 8px 12px; margin-bottom: -2px; font-size: 13px; font-weight: 500; color: {MUTED}; background: rgba(0,101,187,0.05); border-radius: 4px 4px 0 0;">Hover</div>
</div>"""
    menu = f"""<div style="width: 220px; background: {PAPER}; border: 1px solid {BORDER}; border-radius: 10px; box-shadow: 0 8px 24px rgba(0,101,187,0.15); padding: 4px 0;">
  <div style="margin: 2px 6px; padding: 7px 10px; border-radius: 6px; font-size: 13px; color: {NAVY};">Elemento de menú</div>
  <div style="margin: 2px 6px; padding: 7px 10px; border-radius: 6px; font-size: 13px; color: {NAVY}; background: rgba(0,101,187,0.05);">Hover</div>
  <div style="margin: 2px 6px; padding: 7px 10px; border-radius: 6px; font-size: 13px; color: {RED};">Destructivo</div>
</div>"""
    tooltip = f"""<div style="display: flex; flex-direction: column; gap: 10px; align-items: flex-start;">
  <div style="background: {NAVY}; color: #fff; font-size: 12px; font-weight: 500; border-radius: 6px; padding: 5px 10px;">Tooltip — fondo #1a2236, flecha</div>
  <div style="background: {PAPER}; color: {NAVY}; font-size: 13px; line-height: 1.55; border: 1px solid #e0e7ef; border-left: 3px solid {BLUE}; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,101,187,0.12); padding: 10px 14px; max-width: 300px;">Variante rica: superficie clara con riel de marca a la izquierda, para explicaciones largas.</div>
</div>"""
    dialogo = f"""<div style="width: 340px; background: {PAPER}; border-radius: 14px; box-shadow: 0 24px 64px rgba(0,101,187,0.18); overflow: hidden;">
  <div style="padding: 16px 20px 8px 20px; font-size: 16px; font-weight: 700; color: {NAVY};">Título del diálogo</div>
  <div style="padding: 4px 20px 16px 20px; font-size: 14px; color: {MUTED};">Cuerpo 14px. Radio 14 (24 en diálogos destacados).</div>
  <div style="display: flex; justify-content: flex-end; gap: 8px; padding: 0 20px 18px 20px;">
    <div style="height: 32px; padding: 0 14px; border-radius: 8px; color: {MUTED}; font-size: 13px; font-weight: 600; display: flex; align-items: center;">Cancelar</div>
    {btn("Confirmar", BLUE, "#fff", "0 2px 8px rgba(0,101,187,0.3)", extra=" height: 32px;")}
  </div>
</div>"""
    body = f"""{card("Botones", botones)}
{card("Inputs (outlined, el único variant)", inputs)}
<div style="{row(24)}">
  <div style="flex: 1.2; display: flex; flex-direction: column; gap: 24px;">{card("Chips y badges", chips)}{card("Tabs — subrayado 2px sobre línea 2px", tabs)}</div>
  <div style="flex: 1; display: flex; flex-direction: column; gap: 24px;">{card("Menú contextual", menu)}</div>
  <div style="flex: 1; display: flex; flex-direction: column; gap: 24px;">{card("Tooltips", tooltip)}</div>
</div>
{card("Diálogo", dialogo)}"""
    return page(f'{header("Controles", "Botones, inputs, chips, tabs, menús, tooltips y diálogos", "ctsTheme.ts:123-368")}{body}', 1080)

# ═══ 7. Tablas y listas ═══════════════════════════════════════════════════
def v_tablas():
    head = "".join(f'<div style="padding: 9px 12px; font-size: 11px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: #fff; border-right: 1px solid rgba(255,255,255,0.12);">{h}</div>' for h in ["Tarea", "Estado", "Responsable", "Fecha"])
    def cell(t, extra=""):
        return f'<div style="height: 38px; padding: 0 12px; font-size: 13px; color: {NAVY}; border-right: 1px solid {BORDER}; border-bottom: 1px solid {BORDER}; display: flex; align-items: center; {extra}">{t}</div>'
    def status(t, c):
        return f'<div style="height: 38px; border-right: 1px solid {BORDER}; border-bottom: 1px solid {BORDER}; background: {c}; color: #fff; font-size: 11px; font-weight: 600; display: flex; align-items: center; justify-content: center;">{t}</div>'
    rows_ = (
        f'<div style="display: grid; grid-template-columns: 1.4fr 150px 1fr 1fr;">{cell("Revisión de planos")}{status("En curso", ORANGE)}{cell("L. García")}{cell("13 Ago 2026")}</div>'
        f'<div style="display: grid; grid-template-columns: 1.4fr 150px 1fr 1fr; background: #f7fafd;">{cell("Compra de barrajes — fila hover #f7fafd")}{status("Hecho", GREEN)}{cell("C. Rodríguez")}{cell("20 Ago 2026")}</div>'
        f'<div style="display: grid; grid-template-columns: 1.4fr 150px 1fr 1fr;">{cell("Celda de solo lectura", f"background: rgba(15,23,42,0.035);")}{status("Bloqueado", RED)}{cell("—")}{cell("—")}</div>'
    )
    tabla = f'<div style="border: 1px solid {BORDER}; border-radius: 10px; overflow: hidden; background: {PAPER};"><div style="display: grid; grid-template-columns: 1.4fr 150px 1fr 1fr; background: {BLUE};">{head}</div>{rows_}</div>'
    grupo = f"""<div style="border: 1px solid {BORDER}; border-radius: 10px; overflow: hidden; background: {PAPER};">
  <div style="display: flex; align-items: center; gap: 8px; padding: 8px 10px; background: #f5f7fa; border-left: 4px solid {GREEN};">
    <span style="width: 12px; height: 12px; border-radius: 3px; background: {GREEN};"></span>
    <span style="font-size: 15px; font-weight: 700; color: {GREEN};">Producción</span>
    <span style="height: 20px; padding: 0 8px; border-radius: 6px; background: {GREEN}20; color: {GREEN}; font-size: 11px; font-weight: 700; display: flex; align-items: center;">12</span>
  </div>
  <div style="border-left: 4px solid {GREEN};">
    <div style="height: 40px; display: flex; align-items: center; padding: 0 12px; font-size: 13px; color: {NAVY}; border-bottom: 1px solid {BORDER};">Fila de grid — 40px</div>
    <div style="height: 36px; display: flex; align-items: center; padding: 0 12px; font-size: 12px; color: {MUTED};">Fila de resumen — 36px</div>
  </div>
</div>
<span style="font-size: 12px; color: {MUTED};">Cabecera de grupo 44px, sticky, riel izquierdo 4px del color del grupo; el color viene de la paleta de datos.</span>"""
    reglas = table(["Regla", "Valor"], [
        ["Cabecera", f"bg {mono(BLUE)} · texto blanco 11px uppercase 0.06em · pad 9px 12px"],
        ["Celda", "38px · 13px · padding 0 (el contenido interno se alinea) · bordes " + mono(BORDER)],
        ["Hover de fila", mono("#f7fafd") + " sólido — no rgba (hay celdas sticky encima)"],
        ["Contenedor", "radio 10 + borde; sin sombra"],
        ["Celda de estado", "color pleno a sangre completa, texto blanco 11px 600; hover " + mono("filter: brightness(0.88)")],
        ["Columna fija", "sticky izquierda con fondo de papel y borde derecho"],
        ["Ancho de columna", "150px por defecto · mínimo 60px · tarea 220–260px"],
    ], "220px 1fr")
    body = f"""{card("Tabla estándar", tabla)}
{card("Grupos (patrón W-Flow)", grupo)}
{card("Reglas", reglas)}"""
    return page(f'{header("Tablas y listas", "Cabecera azul, filas 38–40 px, estados a sangre completa", "ctsTheme.ts:204-250 · GroupSection.tsx · StatusCell.tsx")}{body}', 1220)

# ═══ 8. Navegación ════════════════════════════════════════════════════════
def v_navegacion():
    def nav(label, state):
        if state == "active":
            st = f'background: rgba(255,255,255,0.18); border-left: 3px solid rgba(255,255,255,0.9); color: #fff;'
        elif state == "hover":
            st = f'background: rgba(255,255,255,0.1); border-left: 3px solid transparent; color: #fff;'
        else:
            st = f'background: transparent; border-left: 3px solid transparent; color: rgba(255,255,255,0.65);'
        return f'<div style="display: flex; align-items: center; gap: 10px; height: 34px; margin: 0 12px 2px 12px; padding: 0 12px; border-radius: 8px; font-size: 13.5px; font-weight: 600; {st}"><span style="width: 18px; height: 18px; border: 1.6px solid currentColor; border-radius: 4px; flex-shrink: 0;"></span>{label}</div>'
    rail = f"""<div style="width: 256px; background: {BLUE}; border-radius: 12px; box-shadow: 4px 0 20px rgba(0,0,0,0.2); overflow: hidden; display: flex; flex-direction: column;">
  <div style="display: flex; align-items: center; gap: 12px; padding: 24px 24px 16px 24px; border-bottom: 1px solid rgba(255,255,255,0.1);">
    <img src="logo-cts-blanco.png" alt="CTS" style="width: 34px; height: auto;">
    <div style="display: flex; flex-direction: column; line-height: 1.1;">
      <span style="font-size: 17px; font-weight: 900; letter-spacing: 2px; color: #fff;">APLICACIÓN</span>
      <span style="font-size: 9.5px; color: rgba(255,255,255,0.55);">Descriptor del producto</span>
    </div>
  </div>
  <div style="padding: 12px 16px 6px 16px;">
    <div style="height: 34px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; display: flex; align-items: center; padding: 0 10px; font-size: 12.5px; color: rgba(255,255,255,0.4);">Buscar…</div>
  </div>
  <div style="padding: 10px 20px 4px 20px; font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(255,255,255,0.45);">Sección</div>
  {nav("Ítem activo", "active")}{nav("Ítem hover", "hover")}{nav("Ítem inactivo", "idle")}
  <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 10px 16px;"></div>
  <div style="display: flex; align-items: center; gap: 12px; padding: 12px 16px; border-top: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.15); margin-top: 8px;">
    <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.2); border: 2px solid rgba(255,255,255,0.35); color: #fff; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center;">MB</div>
    <div style="display: flex; flex-direction: column; line-height: 1.3; color: #fff;">
      <span style="font-size: 12.5px; font-weight: 700;">Nombre Usuario</span>
      <span style="font-size: 10.5px; opacity: 0.5;">Rol</span>
    </div>
  </div>
</div>"""
    tokens = table(["Token", "Valor"], [
        ["Ancho", "256px (colapsado: 0 con FAB de reapertura, o 64px)"],
        ["Fondo", mono("#0065BB") + " claro · " + mono("#253662") + " oscuro · texto siempre blanco"],
        ["Sombra / borde", mono("4px 0 20px rgba(0,0,0,0.2)") + " · sin borde"],
        ["Ítem activo", mono("rgba(255,255,255,0.18)") + " + borde izq. 3px " + mono("rgba(255,255,255,0.9)")],
        ["Ítem idle / hover", mono("rgba(255,255,255,0.65)") + " / fondo " + mono("rgba(255,255,255,0.1)")],
        ["Divisores", mono("rgba(255,255,255,0.1)")],
        ["Footer de usuario", mono("rgba(0,0,0,0.15)") + " · avatar 32px borde 2px " + mono("rgba(255,255,255,0.35)")],
        ["Logout hover", mono("rgba(255,100,100,0.2)") + " + texto " + mono("rgba(255,180,180,1)")],
    ], "200px 1fr")
    flotantes = f"""<div style="display: flex; flex-direction: column; gap: 14px;">
  <div style="{row(10)} align-items: center;">
    <div style="width: 38px; height: 38px; border-radius: 50%; background: {PAPER}; border: 1px solid {BORDER}; box-shadow: 0 1px 4px rgba(0,0,0,0.06); display: flex; align-items: center; justify-content: center; position: relative;">
      <span style="width: 16px; height: 16px; border: 1.7px solid {MUTED}; border-radius: 4px;"></span>
      <span style="position: absolute; top: -4px; right: -4px; min-width: 16px; height: 16px; border-radius: 8px; background: {RED}; color: #fff; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center;">5</span>
    </div>
    <span style="font-size: 13px; color: {MUTED};">Sin barra superior persistente: acciones en círculos de papel, fijos arriba a la derecha (top 16, right 16).</span>
  </div>
  <div style="display: flex; align-items: center; gap: 6px; font-size: 13px;">
    <span style="color: {MUTED}; font-weight: 500;">Proyectos</span><span style="color: {MUTED};">/</span>
    <span style="color: {MUTED}; font-weight: 500;">Data Center</span><span style="color: {MUTED};">/</span>
    <span style="color: {NAVY}; font-weight: 700;">Esquema</span>
  </div>
  <span style="font-size: 12px; color: {MUTED};">Migas dentro del contenido (mb 8px sobre el título): enlaces 13px 500 en text.secondary con subrayado al hover; la última en text.primary 700.</span>
</div>"""
    body = f"""<div style="{row(24)}">
  <div style="flex-shrink: 0;">{rail}</div>
  <div style="flex: 1; display: flex; flex-direction: column; gap: 24px;">
    {card("Tokens del rail", tokens)}
    {card("Acciones flotantes y migas", flotantes)}
  </div>
</div>"""
    return page(f'{header("Navegación", "El rail azul es la identidad; el contenido queda limpio", "Sidebar.tsx · NotificationBell.tsx · BoardBreadcrumb.tsx")}{body}', 900)


# ═══ 9. Estructura (wireframe numerado) ═══════════════════════════════════
def v_estructura():
    def num(n, abs_=None):
        pos = f'position: absolute; {abs_};' if abs_ else ''
        return (f'<span style="{pos} width: 24px; height: 24px; border-radius: 50%; background: {BLUE}; color: #fff; '
                f'font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,101,187,0.3); flex-shrink: 0;">{n}</span>')
    def zone(label, extra="", dashed=True):
        bd = f'1.5px dashed {INPUT_BD}' if dashed else f'1px solid {BORDER}'
        return (f'<div style="border: {bd}; border-radius: 8px; background: {SOFT}; display: flex; align-items: center; '
                f'justify-content: center; font-size: 11.5px; font-weight: 600; color: {MUTED}; position: relative; {extra}">{label}</div>')

    # ── Shell general (escala 1:2 de 1440×900) ──
    shell = f"""<div style="width: 720px; height: 470px; border: 1px solid {BORDER}; border-radius: 10px; background: {PAPER}; display: flex; overflow: hidden; position: relative; flex-shrink: 0;">
  <div style="width: 128px; background: {BLUE}; display: flex; flex-direction: column; position: relative; flex-shrink: 0;">
    {num(1, "top: 6px; left: 8px;")}
    <div style="margin: 34px 10px 8px 10px; height: 34px; border: 1.5px dashed rgba(255,255,255,0.5); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.85); position: relative;">Logo + descriptor{num(2, "top: -10px; right: -10px;")}</div>
    <div style="margin: 0 10px 8px 10px; height: 24px; border: 1.5px dashed rgba(255,255,255,0.5); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 9.5px; font-weight: 600; color: rgba(255,255,255,0.85); position: relative;">Búsqueda / workspace{num(3, "top: -10px; right: -10px;")}</div>
    <div style="margin: 0 10px; flex-grow: 1; border: 1.5px dashed rgba(255,255,255,0.5); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; color: rgba(255,255,255,0.85); position: relative;">Navegación{num(4, "top: -10px; right: -10px;")}</div>
    <div style="margin: 8px 10px 10px 10px; height: 30px; border: 1.5px dashed rgba(255,255,255,0.5); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 600; color: rgba(255,255,255,0.85); position: relative;">Usuario + rol{num(5, "top: -10px; right: -10px;")}</div>
  </div>
  <div style="flex-grow: 1; display: flex; flex-direction: column; padding: 12px 16px; gap: 8px; position: relative; background: {SOFT};">
    <div style="position: absolute; top: 8px; right: 8px; display: flex; gap: 4px; align-items: center;">
      <span style="width: 20px; height: 20px; border-radius: 50%; background: {PAPER}; border: 1px solid {BORDER};"></span>
      <span style="width: 20px; height: 20px; border-radius: 50%; background: {PAPER}; border: 1px solid {BORDER};"></span>
      {num(6)}
    </div>
    {zone("Migas de pan", "height: 20px; width: 220px;")}
    <div style="display: flex; align-items: center; gap: 8px;">{zone("Título de vista + acciones", "height: 34px; flex-grow: 1;")}{num(7)}</div>
    <div style="display: flex; align-items: center; gap: 8px;">{zone("Toolbar: búsqueda · filtros · orden · CTA", "height: 28px; flex-grow: 1;")}{num(8)}</div>
    <div style="display: flex; gap: 8px; flex-grow: 1;">
      <div style="flex-grow: 1; position: relative;">{zone("Contenido (tabla · cards · lienzo)", "position: absolute; inset: 0;")}<span style="position: absolute; bottom: 8px; right: 8px;">{num(9)}</span></div>
      <div style="width: 150px; position: relative;">{zone("Panel lateral (opcional)", "position: absolute; inset: 0;")}<span style="position: absolute; bottom: 8px; right: 8px;">{num(10)}</span></div>
    </div>
  </div>
</div>"""

    leyenda = table(["N°", "Sección", "Especificación"], [
        ["1", "Rail de navegación", "256px fijo · #0065BB claro / #253662 oscuro · sombra 4px 0 20px · colapsable a 0 con FAB"],
        ["2", "Cabecera del rail", "logo 34px + wordmark 900/17px tracking 2 + descriptor 9.5px · borde inf. rgba(255,255,255,0.1)"],
        ["3", "Búsqueda / workspace", "34px / 42px · fondo rgba(255,255,255,0.08) · radio 10 · opcional según app"],
        ["4", "Navegación", "secciones con título 10px uppercase 0.1em · ítems 34px radio 8 · estados de la hoja Navegación"],
        ["5", "Footer de usuario", "avatar 32px + nombre 12.5/700 + rol 10.5 · fondo rgba(0,0,0,0.15) · fijo abajo"],
        ["6", "Acciones flotantes", "fixed top 16 right 16 · círculos 38px en papel, borde divisor, sombra 1 · campana + tema + perfil"],
        ["7", "Cabecera de vista", "migas 13px arriba (mb 8) · título h5 700 + chip de conteo + acciones · borde inf. divisor · mb 24"],
        ["8", "Toolbar de vista", "controles 32px · búsqueda 200px · selects 135–185px · CTA contained a la derecha"],
        ["9", "Contenido", "gutter 24px (p: 3) · tabla radio 10 / cards radio 12 separadas 16–24px / lienzo a sangre"],
        ["10", "Panel lateral", "300–360px · borde izq. divisor · para detalle, catálogo o inspector · opcional"],
    ], "56px 220px 1fr")

    # ── Variantes ──
    def mini(title, inner):
        return (f'<div style="display: flex; flex-direction: column; gap: 8px;"><span style="font-size: 12px; font-weight: 700; color: {NAVY};">{title}</span>'
                f'<div style="width: 380px; height: 240px; border: 1px solid {BORDER}; border-radius: 8px; background: {PAPER}; display: flex; overflow: hidden;">{inner}</div></div>')
    rail_mini = f'<div style="width: 56px; background: {BLUE}; flex-shrink: 0; display: flex; align-items: flex-start; justify-content: center; padding-top: 6px;"><span style="color: rgba(255,255,255,0.85); font-size: 9px; font-weight: 700;">1</span></div>'
    def z(label, extra=""):
        return zone(label, extra)
    v_listado = mini("A · Listado (Inicio, Proyectos, Catálogo)", f"""{rail_mini}
<div style="flex-grow: 1; background: {SOFT}; padding: 8px; display: flex; flex-direction: column; gap: 6px;">
  {z("7 · cabecera", "height: 24px;")}{z("8 · toolbar", "height: 20px;")}
  {z("9 · fila / card", "height: 34px;")}{z("9 · fila / card", "height: 34px;")}{z("9 · fila / card", "height: 34px;")}
</div>""")
    v_detalle = mini("B · Detalle con panel (Editar proyecto, Esquema)", f"""{rail_mini}
<div style="flex-grow: 1; background: {SOFT}; padding: 8px; display: flex; flex-direction: column; gap: 6px;">
  {z("7 · cabecera", "height: 24px;")}
  <div style="display: flex; gap: 6px; flex-grow: 1;">
    <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 6px;">{z("9 · contenido", "flex-grow: 1;")}</div>
    {z("10 · panel", "width: 96px;")}
  </div>
</div>""")
    v_editor = mini("C · Editor de lienzo (Layout, Diseñar cuadro)", f"""{rail_mini}
<div style="flex-grow: 1; background: {SOFT}; padding: 8px; display: flex; flex-direction: column; gap: 6px;">
  {z("7 · cabecera", "height: 24px;")}
  <div style="display: flex; gap: 6px; flex-grow: 1;">
    {z("10 · equipos", "width: 66px;")}
    <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 6px;">{z("8 · herramientas", "height: 16px;")}{z("9 · lienzo", "flex-grow: 1;")}{z("pestañas de vista", "height: 18px;")}</div>
    {z("10 · inspector", "width: 66px;")}
  </div>
</div>""")

    reglas = f"""<div style="display: flex; flex-direction: column; gap: 10px;">
  {spec("Orden vertical fijo", "6 flotantes → 7 cabecera → 8 toolbar → 9 contenido")}
  {spec("Sin barra superior", "nunca AppBar persistente; el rail y las acciones flotantes son el chrome")}
  {spec("Un solo CTA primario", "el contained vive en la toolbar (8), a la derecha")}
  {spec("Paneles", "derecha para detalle/inspector; el rail (1) nunca duplica contenido de (10)")}
  {spec("Modales", "centrados, radio 14; menús contextuales anclados al disparador")}
</div>"""

    body = f"""<div style="{row(24)}">
  <div style="flex-shrink: 0; display: flex; flex-direction: column; gap: 24px;">{card("Shell de aplicación — zonas numeradas", shell)}{card("Reglas de composición", reglas)}</div>
  <div style="flex-grow: 1;">{card("Leyenda", leyenda)}</div>
</div>
{card("Variantes de vista", f'<div style="{row(24, wrap=True)}">{v_listado}{v_detalle}{v_editor}</div>')}
"""
    return page(f'{header("Estructura", "Wireframe numerado: dónde va cada cosa en toda aplicación CTS", "AppLayout.tsx · Sidebar.tsx · BoardToolbar.tsx")}{body}', 1560)

# ═══ Salida ═══════════════════════════════════════════════════════════════
FILES = {
    "Main.dc.html": (v_portada(), 900),
    "Colores.dc.html": (v_colores(), 1280),
    "ModoOscuro.dc.html": (v_oscuro(), 1100),
    "Tipografia.dc.html": (v_tipografia(), 1240),
    "FormaEspacio.dc.html": (v_forma(), 1460),
    "Controles.dc.html": (v_controles(), 1080),
    "TablasListas.dc.html": (v_tablas(), 1220),
    "Navegacion.dc.html": (v_navegacion(), 900),
    "Estructura.dc.html": (v_estructura(), 1560),
}
OUT.mkdir(exist_ok=True)
for name, (html, _) in FILES.items():
    (OUT / name).write_text(html)

titles = {"Main.dc.html": "Portada", "Colores.dc.html": "1 · Colores", "ModoOscuro.dc.html": "2 · Modo oscuro",
          "Tipografia.dc.html": "3 · Tipografía", "FormaEspacio.dc.html": "4 · Forma y espacio",
          "Controles.dc.html": "5 · Controles", "TablasListas.dc.html": "6 · Tablas y listas", "Navegacion.dc.html": "7 · Navegación", "Estructura.dc.html": "8 · Estructura (wireframe)"}
order = [["Main.dc.html", "Colores.dc.html", "ModoOscuro.dc.html"],
         ["Tipografia.dc.html", "FormaEspacio.dc.html", "Controles.dc.html"],
         ["TablasListas.dc.html", "Navegacion.dc.html", "Estructura.dc.html"]]
GAP_X, GAP_Y = 120, 160
arts, y = [], 0
for r in order:
    row_h = max(FILES[f][1] for f in r)
    for c, f in enumerate(r):
        arts.append({"file": f, "title": titles[f], "x": c * (W + GAP_X), "y": y, "w": W, "h": FILES[f][1]})
    y += row_h + GAP_Y
canvas = {
    "artboards": arts,
    "annotations": [
        {"id": "uso", "x": 0, "y": -150, "w": 560, "text": "Sistema de Diseño CTS — fuente de verdad: cts-manager (frontend/src/theme/ctsTheme.ts).\nToda aplicación nueva copia estos valores literales; no redondear ni aproximar.\nCada hoja cita el archivo de origen arriba a la derecha."},
    ],
    "launch": {"view": "canvas"},
}
(OUT / "canvas.json").write_text(json.dumps(canvas, ensure_ascii=False, indent=2))
print("ok", len(FILES), "hojas →", OUT)

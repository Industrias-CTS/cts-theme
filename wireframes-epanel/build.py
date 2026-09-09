#!/usr/bin/env python3
"""Wireframes numerados de E-Panel (base: Sistema de Diseño CTS, hoja 8 · Estructura).

Uso: `python3 build.py` → escribe `artboards/*.dc.html` y `canvas.json`.
Reutiliza la numeración fija 1-10 del shell de aplicación; cada vista añade
sub-zonas letradas (9a, 9b, 10a...) solo donde su contenido lo requiere.
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / "artboards"

BLUE = "#0065BB"; BLUE_D = "#004696"
NAVY = "#1a2236"; MUTED = "#5a6a80"; BORDER = "#dde3ec"; INPUT_BD = "#d0d8e4"
SOFT = "#f0f4f9"; PAPER = "#ffffff"
RED = "#e2445c"; GREEN = "#00c875"
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
    <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.32em; text-transform: uppercase; color: {BLUE};">Wireframes E-Panel</span>
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

# ── Vocabulario de wireframe (reutiliza el lenguaje de la hoja "Estructura") ──
def badge(n, size=22, dark=False):
    bg = "#ffffff" if dark else BLUE
    fg = BLUE if dark else "#ffffff"
    bd = f"border: 1.5px solid {BLUE};" if dark else ""
    return (f'<span style="width: {size}px; height: {size}px; border-radius: 50%; background: {bg}; color: {fg}; {bd} '
            f'font-size: {round(size*0.5)}px; font-weight: 700; display: flex; align-items: center; justify-content: center; '
            f'box-shadow: 0 2px 6px rgba(0,101,187,0.3); flex-shrink: 0;">{n}</span>')

def zone(n, label, extra="", on_dark=False, align="center"):
    """Caja punteada de wireframe con su número. `extra` trae flex/width/height."""
    dash = f'1.5px dashed {"rgba(255,255,255,0.5)" if on_dark else INPUT_BD}'
    bg = "transparent" if on_dark else SOFT
    fg = "rgba(255,255,255,0.9)" if on_dark else MUTED
    just = {"center": "center", "start": "flex-start", "end": "flex-end"}[align]
    pad = "padding: 8px 12px;" if align != "center" else ""
    return (f'<div style="border: {dash}; border-radius: 8px; background: {bg}; display: flex; align-items: center; '
            f'justify-content: {just}; {pad} gap: 8px; font-size: 12px; font-weight: 600; color: {fg}; position: relative; {extra}">'
            f'{badge(n, 20, dark=on_dark)}<span>{label}</span></div>')

def zone_row(items, gap=8, extra=""):
    inner = "".join(f'<div style="{it[1]}">{it[0]}</div>' for it in items)
    return f'<div style="display: flex; gap: {gap}px; {extra}">{inner}</div>'

RAIL_W = 210

def rail(items4, extra_top="", extra_bottom=""):
    """Rail wireframe (columnas 1-5) a escala, para anteponer a cada vista."""
    return f"""<div style="width: {RAIL_W}px; background: {BLUE}; border-radius: 10px 0 0 10px; display: flex; flex-direction: column; padding: 10px; gap: 8px; flex-shrink: 0; position: relative;">
  {zone(2, "Logo + descriptor", "height: 40px;", on_dark=True)}
  {extra_top}
  {zone(4, "Navegación" + (f" — {items4}" if items4 else ""), "flex-grow: 1;", on_dark=True)}
  {extra_bottom}
  {zone(5, "Usuario + rol", "height: 34px;", on_dark=True)}
</div>"""

def floating():
    return f'<div style="position: absolute; top: 10px; right: 10px;">{badge(6)}</div>'

def shell(rail_html, main_zones, h=560):
    return f"""<div style="border: 1px solid {BORDER}; border-radius: 10px; background: {PAPER}; display: flex; overflow: hidden; position: relative; height: {h}px;">
  {rail_html}
  <div style="flex-grow: 1; display: flex; flex-direction: column; padding: 14px 16px; gap: 8px; position: relative; background: {SOFT};">
    {floating()}
    {main_zones}
  </div>
</div>"""

def legend_common(extra_rows, cols="52px 190px 1fr"):
    base = [
        ["1", "Rail de navegación", "256 px · #0065BB · ver hoja 8 (Estructura) del Sistema de Diseño CTS"],
    ]
    return table(["N°", "Sección", "Contenido específico de esta vista"], base + extra_rows, cols)

# ═══ 1. Login (sin shell) ═════════════════════════════════════════════════
def v_login():
    def n(i, label, extra=""):
        return f'<div style="border: 1.5px dashed {INPUT_BD}; border-radius: 8px; background: {SOFT}; display: flex; align-items: center; gap: 8px; padding: 10px 14px; font-size: 13px; font-weight: 600; color: {MUTED}; {extra}">{badge(i, 22)}<span>{label}</span></div>'
    wire = f"""<div style="border: 1px solid {BORDER}; border-radius: 10px; overflow: hidden; display: flex; height: 520px;">
  <div style="width: 42%; background: {BLUE}; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 16px; padding: 32px; position: relative;">
    {badge(1, 26, dark=True)}<span style="position: absolute; top: 16px; left: 16px; color: #fff; font-size: 11px; font-weight: 700;">1 · Panel de marca</span>
    <div style="width: 72px; height: 72px; border: 1.5px dashed rgba(255,255,255,0.6); border-radius: 12px;"></div>
    <div style="width: 70%; height: 14px; border: 1.5px dashed rgba(255,255,255,0.6); border-radius: 4px;"></div>
    <div style="width: 50%; height: 10px; border: 1.5px dashed rgba(255,255,255,0.4); border-radius: 4px;"></div>
  </div>
  <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; gap: 16px; padding: 48px 64px;">
    {n(2, "Título — Iniciar sesión", "height: 40px; width: 60%;")}
    {n(3, "Campo — Correo electrónico", "height: 44px;")}
    {n(4, "Campo — Contraseña", "height: 44px;")}
    <div style="display: flex; justify-content: space-between;">{n(5, "Recordarme", "height: 30px; width: 45%;")}{n(5, "¿Olvidó su contraseña?", "height: 30px; width: 45%;")}</div>
    {n(6, "Botón — Ingresar (CTA primario)", "height: 44px; background: rgba(0,101,187,0.08); border-color: {BLUE};".replace("{BLUE}", BLUE))}
    {n(7, "Pie — versión / © Industrias CTS", "height: 22px; width: 60%;")}
  </div>
</div>"""
    leyenda = table(["N°", "Sección", "Contenido"], [
        ["1", "Panel de marca", "mitad izquierda, fondo #0065BB · logo E-Panel + wordmark + descriptor · oculto en móvil"],
        ["2", "Título", "\"Iniciar sesión\" · h4/700"],
        ["3", "Campo correo", "input outlined 44px, icono usuario"],
        ["4", "Campo contraseña", "input outlined 44px, icono candado, alternar visibilidad"],
        ["5", "Acciones secundarias", "checkbox \"Recordarme\" (izq.) + enlace \"¿Olvidó su contraseña?\" (der.)"],
        ["6", "CTA primario", "botón contained ancho completo, 44px — \"Ingresar\""],
        ["7", "Pie", "número de versión y crédito, 12px, color muted"],
    ], "56px 180px 1fr")
    body = f"""{card("Wireframe", wire)}
{card("Qué va en cada sección", leyenda)}"""
    return page(f'{header("Login", "Pantalla de acceso — sin rail ni acciones flotantes (fuera del shell de aplicación)", "pages/Login")}{body}', 1220)

# ═══ 2. Inicio ═════════════════════════════════════════════════════════════
def v_inicio():
    r = rail("Inicio")
    main = f"""{zone(7, "Cabecera — saludo \"Buenos días, {Usuario}\"", "height: 32px; align-self: flex-start;", align="start")}
{zone("9a", "Tarjetas \"Visitado recientemente\" (5)", "height: 90px;")}
{zone("9b", "Buscador + filtros (Fecha, Tipo)", "height: 40px;")}
{zone("9c", "Lista de actividad reciente por OT", "flex-grow: 1;")}"""
    wire = shell(r, main, h=520)
    leyenda = table(["N°", "Sección", "Contenido específico"], [
        ["1", "Rail de navegación", "Inicio activo · grupo Espacio de trabajo: Cuadros / Esquema / Layout / U-Draw"],
        ["6", "Acciones flotantes", "toggle de tema + avatar de perfil (sin campana: sin backend de notificaciones aún)"],
        ["7", "Cabecera", "saludo con nombre del usuario; sin migas (es la raíz)"],
        ["9a", "Recientes", "hasta 5 tarjetas 200×124 (banda con degradado del color + etiqueta); vacías si no hay historial"],
        ["9b", "Buscador y filtros", "input \"Buscar…\" 40px + selects Fecha / Tipo"],
        ["9c", "Actividad", "filas 72px: icono de edición, \"OTxxxx - Nombre\", tiempo relativo (\"Hace 3 horas\")"],
    ], "52px 190px 1fr")
    body = f"""{card("Wireframe", wire)}
{card("Qué va en cada sección", leyenda)}"""
    return page(f'{header("Inicio", "Home / Dashboard", "pages/Dashboard")}{body}', 1200)

# ═══ 3. Proyectos → Tablero ════════════════════════════════════════════════
def v_proyectos_tablero():
    r1 = rail("Proyectos")
    main1 = f"""{zone(7, "Título \"Proyectos\" + contador", "height: 30px; align-self: flex-start;", align="start")}
{zone(8, "Buscador · Filtros (Estado, Ordenar) · CTA \"Nuevo proyecto\"", "height: 36px;")}
{zone("9", "Listado de proyectos (tarjeta / lista, con toggle)", "flex-grow: 1;")}"""
    wire1 = shell(r1, main1, h=460)

    r2 = rail("Proyectos")
    main2 = f"""{zone(7, "Migas + nombre del proyecto (editable) + guardar/cancelar", "height: 34px; align-self: flex-start;", align="start")}
{zone(8, "Buscador por tag · Filtros (Línea, Ordenar) · CTA \"Nuevo tablero\"", "height: 36px;")}
{zone_row([(zone("9", "Tableros del proyecto (tarjeta / lista)", "flex-grow: 1; height: 100%;"), "flex-grow: 1;"),
           (zone("10", "Panel — datos comercial/técnico", "width: 100%; height: 100%;"), "width: 190px; flex-shrink: 0;")], extra="flex-grow: 1;")}"""
    wire2 = shell(r2, main2, h=460)

    arrow = f'<div style="display: flex; align-items: center; justify-content: center; width: 56px; flex-shrink: 0;"><svg width="36" height="24" viewBox="0 0 36 24" fill="none" stroke="{BLUE}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h28M22 4l8 8-8 8"/></svg></div>'
    flow = f"""<div style="display: flex; align-items: center; gap: 0;">
  <div style="flex: 1; display: flex; flex-direction: column; gap: 8px;"><span style="font-size: 12px; font-weight: 700; color: {NAVY};">A · Listado de proyectos</span>{wire1}</div>
  {arrow}
  <div style="flex: 1; display: flex; flex-direction: column; gap: 8px;"><span style="font-size: 12px; font-weight: 700; color: {NAVY};">B · Tablero (detalle del proyecto)</span>{wire2}</div>
</div>"""
    leyenda = table(["Vista", "N°", "Sección", "Contenido específico"], [
        ["A", "8", "Toolbar", "buscador + Estado + Ordenar por + CTA contained \"Nuevo proyecto\""],
        ["A", "9", "Listado", "toggle tarjeta/lista; card = folder con OT, cliente, estado, fecha, creador, botón Abrir"],
        ["B", "7", "Cabecera", "migas \"Proyectos / {Proyecto}\"; título editable en línea + iconos guardar/cancelar"],
        ["B", "8", "Toolbar", "buscar por tag + Línea + Ordenar por + CTA \"Nuevo tablero\""],
        ["B", "9", "Tableros", "cards 300px o lista 9 columnas: Tag, Línea, Icc, IP, Imax, Color, Dimensiones, U"],
        ["B", "10", "Panel lateral", "300px · datos comercial (cliente, OT) y técnico (In, Icc, IP, tensión) del proyecto"],
    ], "56px 44px 130px 1fr")
    body = f"""{card("Wireframe — flujo A → B", flow)}
{card("Qué va en cada sección", leyenda)}"""
    return page(f'{header("Proyectos → Tablero", "Del listado al detalle de un proyecto", "pages/Projects · pages/ProjectDetail")}{body}', 1200)

# ═══ 4. Selección de equipos (Esquema) ═════════════════════════════════════
def v_seleccion_equipos():
    r = rail("Selección Equipos", extra_top=zone(3, "Búsqueda por referencia", "height: 28px;", on_dark=True))
    main = f"""{zone(7, "Migas + título \"Selección de equipos\"", "height: 30px; align-self: flex-start;", align="start")}
{zone_row([
    (zone("9", "Árbol de equipos seleccionados (referencia, polos, familia, corriente, poder de corte, cantidad…)", "flex-grow: 1; height: 100%;"), "flex-grow: 1;"),
    (f'<div style="display: flex; flex-direction: column; gap: 8px; width: 220px; flex-shrink: 0;">{zone("10a", "Catálogo — categorías / familias", "flex-grow: 1;")}{zone("10b", "Detalle del equipo (al agregar)", "flex-grow: 1;")}</div>', "width: 220px; flex-shrink: 0;"),
], extra="flex-grow: 1;")}"""
    wire = shell(r, main, h=520)
    leyenda = table(["N°", "Sección", "Contenido específico"], [
        ["3", "Búsqueda del rail", "input \"Búsqueda por referencia\" — específico de esta vista"],
        ["4", "Navegación contextual", "Selección Equipos (activo) / Diseñar Cuadro / Unifilar"],
        ["7", "Cabecera", "migas \"Proyectos / {Proyecto} / {Tablero}\" + título"],
        ["9", "Contenido", "árbol jerárquico; cada fila: referencia, N° polos, familia, corriente, poder de corte, voltaje, instalación, cantidad, menú ···"],
        ["10a", "Catálogo", "árbol de categorías → familias (MCB, MCCB, ACB…) del fabricante"],
        ["10b", "Detalle del equipo", "aparece al seleccionar/agregar: selector técnico, accesorios, listado de componentes, botón Agregar"],
    ], "52px 190px 1fr")
    body = f"""{card("Wireframe", wire)}
{card("Qué va en cada sección", leyenda)}"""
    return page(f'{header("Selección de equipos", "Configurador de equipos del tablero (\"Esquema\")", "pages/BoardDetail · sección equipos")}{body}', 1200)

# ═══ 5. Diseñar cuadro (Layout) ════════════════════════════════════════════
def v_disenar_cuadro():
    r = rail("Diseñar Cuadro")
    main = f"""{zone(7, "Migas + título \"Diseñar cuadro\"", "height: 30px; align-self: flex-start;", align="start")}
{zone(8, "Herramientas del lienzo: deshacer · zoom · exportar · comentar · filtrar", "height: 28px;")}
{zone_row([
    (zone("10a", "Panel — Equipos", "height: 100%;"), "width: 130px; flex-shrink: 0;"),
    (f'<div style="display: flex; flex-direction: column; gap: 8px; flex-grow: 1;">{zone("9", "Lienzo — gabinete, celdas, barrajes, botón + para nueva celda", "flex-grow: 1;")}{zone("9", "Pestañas de vista: Frontal · Lateral · Posterior · Superior · Inferior", "height: 26px;")}</div>', "flex-grow: 1;"),
    (zone("10b", "Panel — Toppings", "height: 100%;"), "width: 130px; flex-shrink: 0;"),
], extra="flex-grow: 1;")}"""
    wire = shell(r, main, h=520)
    leyenda = table(["N°", "Sección", "Contenido específico"], [
        ["4", "Navegación contextual", "Diseñar Cuadro (activo) / Selección Equipos / Unifilar"],
        ["7", "Cabecera", "migas \"Proyectos / {Proyecto} / {Tablero}\" + título \"Diseñar cuadro\""],
        ["8", "Herramientas", "iconos 24px: deshacer, zoom −/+, exportar, comentar, filtrar — alineados a la derecha"],
        ["9", "Lienzo", "vista frontal del gabinete con celdas de barraje y equipos; celda fantasma + botón \"+\" para agregar; anchos disponibles (200/400/720/800/1120 mm)"],
        ["9", "Pestañas de vista", "franja azul inferior: Frontal (activa) · Lateral · Posterior · Superior · Inferior + versión"],
        ["10a", "Panel Equipos", "lista de piezas disponibles para arrastrar al lienzo"],
        ["10b", "Panel Toppings", "barrajes horizontal/vertical, puente, placas lisas"],
    ], "52px 190px 1fr")
    body = f"""{card("Wireframe", wire)}
{card("Qué va en cada sección", leyenda)}"""
    return page(f'{header("Diseñar cuadro", "Armado físico del tablero (\"Layout\")", "pages/BoardDetail · sección cuadro")}{body}', 1260)

# ═══ Portada ════════════════════════════════════════════════════════════════
def v_portada():
    items = [
        ("Login", "Pantalla de acceso, sin shell de aplicación."),
        ("Inicio", "Home con recientes, buscador y actividad."),
        ("Proyectos → Tablero", "Del listado de proyectos al detalle de un proyecto."),
        ("Selección de equipos", "Configurador de equipos del tablero (Esquema)."),
        ("Diseñar cuadro", "Armado físico del tablero (Layout)."),
        ("Configurador (modal)", "Modal de configuración de un equipo del catálogo — patrón nuevo, no cubierto por la hoja Estructura."),
    ]
    idx = "".join(f'<div style="display: flex; align-items: flex-start; gap: 10px;"><span style="width: 22px; height: 22px; border-radius: 6px; background: {BLUE}; color: #fff; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px;">{i+1}</span><div style="display: flex; flex-direction: column;"><span style="font-size: 14px; font-weight: 700; color: {NAVY};">{t}</span><span style="font-size: 12.5px; color: {MUTED};">{d}</span></div></div>' for i, (t, d) in enumerate(items))
    convencion = table(["N°", "Significa siempre"], [
        ["1–6", "Chrome fijo del shell — igual en toda la app (rail, cabecera del rail, búsqueda/workspace, navegación, footer de usuario, acciones flotantes)"],
        ["7", "Cabecera de la vista — migas + título + acciones"],
        ["8", "Toolbar — búsqueda, filtros, orden, CTA principal"],
        ["9", "Contenido — lo específico de cada vista (sufijos a/b/c cuando hay más de un bloque)"],
        ["10", "Panel lateral — opcional; detalle, catálogo o inspector (sufijos a/b si hay más de uno)"],
    ], "80px 1fr")
    body = f"""<div style="background: {BLUE}; border-radius: 16px; padding: 40px 48px; display: flex; align-items: center; gap: 32px;">
  <img src="logo-epanel.png" alt="E-Panel" style="width: 64px; height: 64px;">
  <div style="display: flex; flex-direction: column; gap: 6px;">
    <span style="font-size: 11px; font-weight: 700; letter-spacing: 0.32em; text-transform: uppercase; color: rgba(255,255,255,0.7);">E-Panel</span>
    <span style="font-size: 30px; font-weight: 700; color: #ffffff; line-height: 1.1;">Wireframes de estructura</span>
    <span style="font-size: 14px; color: rgba(255,255,255,0.75);">Numeración de la hoja 8 · Estructura del Sistema de Diseño CTS, aplicada a las vistas reales de E-Panel — para socializar con el equipo dónde va cada cosa.</span>
  </div>
</div>
<div style="{row(24)}">
  {card("Vistas de esta guía", f'<div style="display: flex; flex-direction: column; gap: 14px;">{idx}</div>', grow=True)}
  {card("Convención de numeración (fija en todas las vistas)", convencion, grow=True)}
</div>"""
    return page(f'{header("Portada", "Cómo leer estos wireframes", "cts-theme/sistema-diseno-cts · hoja 8")}{body}', 780)

# ═══ 6. Configurador (modal) ════════════════════════════════════════════════
# La hoja "Estructura" del Sistema de Diseño CTS numera VISTAS (shell de
# página); no cubre diálogos. Esta hoja define la convención para modales de
# configuración — el mismo patrón sirve para cualquier equipo (NSX, CVS...) y
# para futuros modales similares (no solo el selector de equipos).
def v_configurador():
    header_bar = zone(1, "Cabecera — nombre del equipo/fabricante + cerrar", "height: 88px; border-radius: 10px 10px 0 0;")

    tabs_col = zone(2, "Pestañas (navegación vertical)", "width: 190px; flex-shrink: 0; border-right: 1px solid " + BORDER + "; border-radius: 0;")
    content_col = zone(3, "Contenido de la pestaña activa — grupos de opciones", "flex-grow: 1; border-radius: 0;")
    side_col = zone(4, "Vista general — imagen técnica + especificaciones", "width: 250px; flex-shrink: 0; border-left: 1px solid " + BORDER + "; border-radius: 0;")
    footer = zone(5, "Pie de acciones — CTA principal", "height: 60px; border-top: 1px solid " + BORDER + "; border-radius: 0 0 10px 10px;")

    modal = f"""<div style="border: 1px solid {BORDER}; border-radius: 10px; overflow: hidden; background: {PAPER}; box-shadow: 0 24px 64px rgba(0,101,187,0.18); display: flex; flex-direction: column;">
  {header_bar}
  <div style="display: flex; min-height: 380px;">{tabs_col}{content_col}{side_col}</div>
  {footer}
</div>"""
    scrim_wrap = f'<div style="background: rgba(15,23,42,0.35); border-radius: 12px; padding: 32px;">{modal}</div>'

    leyenda = table(["N°", "Sección", "Contenido específico"], [
        ["1", "Cabecera", "banda con degradado de marca (patrón cts-manager DialogHeader) · nombre del equipo + fabricante · botón cerrar"],
        ["2", "Pestañas", "navegación vertical: Claves de búsqueda (activa) · Accesorios · Comunicación — varía según el equipo"],
        ["3", "Contenido de la pestaña", "grupos de opciones tipo chip, obligatorios marcados con *: Línea, Corriente nominal, Unidad de disparo"],
        ["4", "Vista general", "imagen técnica del equipo + ficha de especificaciones (Polos, Frame, Icc 220/440/480V)"],
        ["5", "Pie de acciones", "CTA \"Agregar a la lista\" — deshabilitado hasta completar los campos obligatorios de la pestaña activa"],
    ], "52px 170px 1fr")

    convencion = table(["Uso", "Regla"], [
        ["Cuándo aplica", "todo modal de configuración de un equipo/pieza dentro del catálogo (E-Configurator); no es el modal genérico Crear/Editar (ese usa el patrón simple de formulario)"],
        ["Tamaño", "modal grande centrado, ancho fijo ~900–1000px, alto según contenido con scroll interno en 3"],
        ["Pestañas", "1 a N según el equipo; siempre \"Claves de búsqueda\" primero"],
        ["Obligatoriedad", "asterisco rojo en el grupo + borde rojo en sus chips hasta seleccionar uno"],
        ["Cierre", "botón × en la cabecera; sin botón \"Cancelar\" separado — el cierre descarta la selección"],
    ], "150px 1fr")

    body = f"""{card("Wireframe", scrim_wrap)}
{card("Qué va en cada sección", leyenda)}
{card("Convención de modal de configuración (nueva — no estaba en la hoja Estructura)", convencion)}"""
    return page(f'{header("Configurador (modal)", "Modal de configuración de un equipo del catálogo — ej. selector NSX", "BoardDetail · sección equipos · FamilyConfigDialog")}{body}', 1450)

# ═══ Salida ═══════════════════════════════════════════════════════════════
FILES = {
    "Main.dc.html": (v_portada(), 780),
    "Login.dc.html": (v_login(), 1220),
    "Inicio.dc.html": (v_inicio(), 1200),
    "ProyectosTablero.dc.html": (v_proyectos_tablero(), 1200),
    "SeleccionEquipos.dc.html": (v_seleccion_equipos(), 1200),
    "DisenarCuadro.dc.html": (v_disenar_cuadro(), 1260),
    "Configurador.dc.html": (v_configurador(), 1450),
}
OUT.mkdir(exist_ok=True)
for name, (html, _) in FILES.items():
    (OUT / name).write_text(html)

titles = {"Main.dc.html": "Portada", "Login.dc.html": "1 · Login", "Inicio.dc.html": "2 · Inicio",
          "ProyectosTablero.dc.html": "3 · Proyectos → Tablero", "SeleccionEquipos.dc.html": "4 · Selección de equipos",
          "DisenarCuadro.dc.html": "5 · Diseñar cuadro", "Configurador.dc.html": "6 · Configurador (modal)"}
order = [["Main.dc.html", "Login.dc.html", "Inicio.dc.html"],
         ["ProyectosTablero.dc.html", "SeleccionEquipos.dc.html", "DisenarCuadro.dc.html"],
         ["Configurador.dc.html"]]
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
        {"id": "uso", "x": 0, "y": -150, "w": 620, "text": "Wireframes de E-Panel — misma numeración que la hoja 8 (Estructura) del Sistema de Diseño CTS.\n1-6 chrome fijo · 7 cabecera · 8 toolbar · 9 contenido · 10 panel lateral.\nPara socializar dónde va cada cosa antes de maquetar en alta fidelidad."},
    ],
    "launch": {"view": "canvas"},
}
(OUT / "canvas.json").write_text(json.dumps(canvas, ensure_ascii=False, indent=2))
print("ok", len(FILES), "wireframes →", OUT)

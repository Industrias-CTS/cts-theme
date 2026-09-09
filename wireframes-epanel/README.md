# Wireframes E-Panel

Wireframes numerados de las vistas clave de E-Panel, usando la misma
numeración fija de la hoja **8 · Estructura** del
[Sistema de Diseño CTS](../sistema-diseno-cts/) — para socializar con el
equipo dónde va cada cosa antes de maquetar en alta fidelidad.

- **Lienzo publicado (Claude Design):**
  https://claude.ai/code/artifact/b77faf03-ed66-4420-8f40-256fdef58e53

## Vistas

1. **Login** — pantalla de acceso, sin shell de aplicación (numeración propia 1–7)
2. **Inicio** — home con recientes, buscador y actividad
3. **Proyectos → Tablero** — del listado de proyectos al detalle de un proyecto
4. **Selección de equipos** — configurador de equipos del tablero ("Esquema")
5. **Diseñar cuadro** — armado físico del tablero ("Layout")
6. **Configurador (modal)** — modal de configuración de un equipo del catálogo (ej. selector NSX); numeración propia 1–5, no cubierta por la hoja Estructura

## Convención de numeración (fija en toda vista con shell)

| N° | Significa siempre |
|---|---|
| 1–6 | Chrome fijo del shell: rail, cabecera del rail, búsqueda/workspace, navegación, footer de usuario, acciones flotantes |
| 7 | Cabecera de la vista — migas + título + acciones |
| 8 | Toolbar — búsqueda, filtros, orden, CTA principal |
| 9 | Contenido — específico de cada vista (sufijos a/b/c si hay más de un bloque) |
| 10 | Panel lateral — opcional; detalle, catálogo o inspector (sufijos a/b si hay más de uno) |

Login no usa el shell (no hay sesión aún), así que tiene su propia numeración
1–7 documentada en su propia hoja.

## Convención de modal de configuración (hoja 6)

Los modales tampoco entran en la numeración de "Estructura" (esa hoja cubre
vistas, no diálogos). La hoja "Configurador" define el patrón para todo modal
de configuración de un equipo del catálogo — numeración propia 1–5:

| N° | Sección |
|---|---|
| 1 | Cabecera — banda con degradado de marca + nombre del equipo/fabricante + cerrar |
| 2 | Pestañas — navegación vertical (varía según el equipo) |
| 3 | Contenido de la pestaña activa — grupos de opciones |
| 4 | Vista general — imagen técnica + especificaciones |
| 5 | Pie de acciones — CTA principal |

Este patrón es reutilizable para cualquier configurador de equipo (no solo NSX);
el modal genérico Crear/Editar Proyecto sigue el patrón simple de formulario ya
visto en la maquetación de `E-Panel/docs/design/`.

## Estructura

```
wireframes-epanel/
├── build.py               # generador: una función v_* por vista
├── README.md
├── wireframes-epanel.html # lienzo sembrado (se regenera; no editar a mano)
├── logo-epanel.png · logo-cts-blanco.png
└── artboards/              # hojas .dc.html + canvas.json (salida de build.py)
```

## Flujo de actualización

1. Editar `build.py` (zonas por vista definidas cerca del final del archivo).
2. `python3 build.py` regenera `artboards/`.
3. Desde Claude Code con `/design`, re-sembrar y guardar al mismo enlace.

## Notas

- Contenido tomado de las vistas reales de `apps/web` (Dashboard, Projects,
  ProjectDetail, BoardDetail secciones `equipos`/`cuadro`) y de la maquetación
  previa en `E-Panel/docs/design/`.
- Son wireframes de bajo detalle a propósito: cajas punteadas con número, sin
  color ni tipografía final — la idea es acordar la estructura antes de vestirla.

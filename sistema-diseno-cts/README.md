# Sistema de Diseño CTS

Guía visual de tokens y componentes para que todas las aplicaciones de
Industrias CTS (W-Flow, E-Panel y siguientes) compartan la misma base de
estilos. **Fuente de verdad:** `cts-manager/frontend/src/theme/ctsTheme.ts`.

- **Lienzo publicado (Claude Design):**
  https://claude.ai/code/artifact/c6735804-7f9c-4f31-ac8c-090a11b5e0ef
- **Cómo ver / regenerar el diseño:** [COMO-VER-EL-DISENO.md](COMO-VER-EL-DISENO.md)

## Hojas

1. **Portada** — principios y stack de referencia
2. **Colores** — marca, superficie, semánticos, paleta de datos (8), estados
3. **Modo oscuro** — equivalencias y reglas (papel más claro que el fondo)
4. **Tipografía** — Titillium Web 300–900, escala MUI, micro-tipografía
5. **Forma y espacio** — radios 6/8/10/12/14/30/99, bordes 1–4px, sombras azuladas, densidad, animación
6. **Controles** — botones, inputs, chips, tabs, menús, tooltips, diálogos
7. **Tablas y listas** — cabecera azul, filas 38–40px, estados a sangre completa, grupos
8. **Navegación** — rail azul 256px con estados exactos, acciones flotantes, migas
9. **Estructura (wireframe)** — shell numerado 1–10, leyenda y variantes de vista (listado, detalle con panel, editor de lienzo)

## Estructura

```
sistema-diseno-cts/
├── build.py                 # generador: una función v_* por hoja, tokens en cabecera
├── README.md
├── COMO-VER-EL-DISENO.md    # cómo ejecutar y ver el diseño
├── sistema-diseno-cts.html  # lienzo sembrado (se regenera; no editar a mano)
├── logo-cts-azul.png · logo-cts-blanco.png · logo-w-flow.svg
└── artboards/                # hojas .dc.html + canvas.json (salida de build.py)
```

## Flujo de actualización

1. Editar `build.py` (los tokens están al inicio, cada hoja cita su archivo fuente).
2. `python3 build.py` regenera `artboards/`.
3. Desde Claude Code con `/design`, re-sembrar y guardar al mismo enlace.

## Regla de oro

Copiar los valores **literales** — hex, radios, alturas, alfas — sin redondear
ni aproximar. Si un valor no está aquí, buscarlo en el código de cts-manager y
añadirlo a la hoja correspondiente.

# cts-theme

Estándar de diseño de Industrias CTS: tema de colores para JavaScript/TypeScript
(con soporte para `MUI^6`), y punto de reunión de todas las guías/lienzos de
diseño que se vayan haciendo para las aplicaciones del grupo (W-Flow, E-Panel
y siguientes).

**Fuente de verdad de los tokens:** `cts-manager/frontend/src/theme/ctsTheme.ts`.

## Diseños en esta carpeta

Cada diseño vive en su propia subcarpeta, con su generador, sus artboards y su
propio `README.md`:

- **[sistema-diseno-cts/](sistema-diseno-cts/)** — la guía de estilos base:
  colores, tipografía, forma y espacio, controles, tablas, navegación y
  estructura (wireframe numerado). Lienzo publicado:
  https://claude.ai/code/artifact/c6735804-7f9c-4f31-ac8c-090a11b5e0ef

Cuando se agregue un diseño nuevo (una app, una vista, una exploración), crear
una subcarpeta hermana (`nombre-del-diseño/`) con la misma estructura:
`build.py` + `README.md` + `COMO-VER-EL-DISENO.md` + `artboards/`.

## Regla de oro

Copiar los valores **literales** de cts-manager — hex, radios, alturas, alfas
— sin redondear ni aproximar. Cada hoja debe citar el archivo fuente del que
tomó cada valor.

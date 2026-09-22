# cts-theme

Estándar de diseño de Industrias CTS: tema de colores para JavaScript/TypeScript
(con soporte para `MUI ^6 || ^7 || ^9`), y punto de reunión de todas las guías/lienzos de
diseño que se vayan haciendo para las aplicaciones del grupo (W-Flow, E-Panel
y siguientes).

**Fuente de verdad de los tokens:** `cts-manager/frontend/src/theme/ctsTheme.ts`.

## Paquete

- `src/tokens.ts` — radios, bordes, sombras, densidad, animación, layout, rail, tipografía
- `src/colors.ts` — marca, superficie (claro/oscuro), semánticos, paleta de datos (8)
- `src/mui/theme.ts` — `createCtsTheme(mode)`; `augmentation.ts` expone los tokens como `theme.cts` dentro de cualquier `sx`
- [**INSTRUCCIONES-COMPONENTES.md**](docs/INSTRUCCIONES-COMPONENTES.md) — especificación de los 13 componentes de layout (zonas 1–10)
- [**MOBILE-TBD.md**](docs/MOBILE-TBD.md) — lo que el sistema todavía no define para móvil

```bash
pnpm build             # tsc → dist/
pnpm typecheck:matrix  # comprueba src + smoke contra MUI 6.5.0, 7.3.11 y 9.4.0
```

## Diseños en esta carpeta

Cada diseño vive en su propia subcarpeta, con su generador, sus artboards y su
propio `README.md`:

- **[docs/demo/](docs/demo/)** — la guía de estilos base:
  colores, tipografía, forma y espacio, controles, tablas, navegación y
  estructura (wireframe numerado). Lienzo publicado:
  https://claude.ai/code/artifact/c6735804-7f9c-4f31-ac8c-090a11b5e0ef
- **[wireframes-epanel/](wireframes-epanel/)** — wireframes numerados de Login,
  Inicio, Proyectos → Tablero, Selección de equipos y Diseñar cuadro, con la
  numeración de la hoja Estructura aplicada a E-Panel. Lienzo publicado:
  https://claude.ai/code/artifact/b77faf03-ed66-4420-8f40-256fdef58e53

Cuando se agregue un diseño nuevo (una app, una vista, una exploración), crear
una subcarpeta hermana (`nombre-del-diseño/`) con la misma estructura:
`build.py` + `README.md` + `COMO-VER-EL-DISENO.md` + `artboards/`.

## Regla de oro

Copiar los valores **literales** de cts-manager — hex, radios, alturas, alfas
— sin redondear ni aproximar. Cada hoja debe citar el archivo fuente del que
tomó cada valor.

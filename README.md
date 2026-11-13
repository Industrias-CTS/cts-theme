# cts-theme

Sistema de Diseño de Industrias CTS: la fuente única de colores, medidas,
tema MUI, componentes comunes, formato y reglas de estilo para **todas** las
aplicaciones de la organización (cts-manager/W-Flow, E-Panel, t-monitor y las
que vengan). También reúne las guías y lienzos de diseño de cada app.

Soporta React 18/19 y `MUI ^6 || ^7 || ^9`.

**Origen de los valores:** las apps en producción, copiados literalmente
(cts-manager `frontend/src/theme/ctsTheme.ts` como base; ver
[Estandares-Globales.md](docs/Estandares-Globales.md)).

## Empezar

- [**Nueva-App.md**](docs/Nueva-App.md) — cómo usar el paquete en una app nueva o migrar una existente
- [**Filosofia.md**](docs/Filosofia.md) — principios y reglas obligatorias (las marcadas [lint] fallan en CI)
- [**Estandares-Globales.md**](docs/Estandares-Globales.md) — auditoría de las apps y decisiones G1–G12

## Paquete

| Import | Contenido | Fuente |
|---|---|---|
| `@industriascts/cts-theme` | todo lo de abajo salvo `views`, `css` y `eslint` | `src/index.ts` |
| `…/colors` | marca, superficies, semánticos, chrome, acción, **estados** (`status`), `data8` | `src/colors.ts` |
| `…/tokens` | radios, bordes, sombras, elevación, densidad, movimiento, **capas** (`zIndex`), notificaciones, táctil, layout, rail, tipografía | `src/tokens.ts` |
| `…/mui` | `createCtsTheme(mode, { profile })`, `themeOptions`; overrides de componentes; `theme.cts` en cualquier `sx` | `src/mui/` |
| `…/views` | `AppShell`, `LoginShell`, `QueryState`, `DialogHeader`, `NotificationHost` + `useNotify` | `src/views/` |
| `…/format` | fechas, horas, números, moneda, porcentajes y unidades en `es-CO` | `src/format.ts` |
| `…/css` | variables `--cts-*` para lo que no usa MUI | generado desde `src/css.ts` |
| `…/eslint` | preset que aplica las reglas de Filosofia.md | `eslint/index.js` |

```bash
pnpm build             # tsc → dist/ y dist/cts-theme.css
pnpm typecheck:matrix  # src + smoke contra MUI 6.5.0, 7.3.11 y 9.4.0
pnpm lint              # el repo pasa su propio preset
pnpm check             # las tres cosas
pnpm dev               # playground con LoginShell y AppShell
```

## Documentación

- [**App-Shell.md**](docs/App-Shell.md) · [**Login-Shell.md**](docs/Login-Shell.md) — diseño de los dos cascarones
- [**Atomos.md**](docs/Atomos.md) — modelo primitivos → roles → átomos y decisiones D1–D23
- [**Instrucciones-Componentes.md**](docs/Instrucciones-Componentes.md) — especificación de los 13 componentes de layout (zonas 1–10)
- [**Mobile.md**](docs/Mobile.md) — perfil HMI y lo que falta definir para móvil
- [**Estilado-Consumo.md**](docs/Estilado-Consumo.md) — métodos de estilado de MUI y formas de inyectar cts-theme

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

# Átomos del Sistema de Diseño CTS

> **Estado:** borrador para revisión. Paso 1 de 3 de la rama `feat/atoms`.
> No hay código todavía. El paso 2 (código) empieza cuando las decisiones
> abiertas estén resueltas.
>
> **Fuente:** `cts-manager/frontend/src`, rama `main` en `cb1d6b04`
> (2026-10-14). Cada valor está copiado literalmente del código. Los valores
> marcados `[M]` se midieron en un navegador (Chromium sin interfaz, MUI 7.3.9,
> con el `createCtsTheme` real de cts-manager).

## Contenido

1. [Modelo](#modelo) · [La auditoría en cifras](#la-auditoría-en-cifras)
2. [Capa 1 · Primitivos](#capa-1--primitivos) · [Capa 2 · Roles](#capa-2--roles)
3. Capa 3 · Átomos: [Controles](#controles) · [Navegación y capas flotantes](#navegación-y-capas-flotantes) · [Datos y retroalimentación](#datos-y-retroalimentación)
4. [Deriva de cts-theme](#deriva-de-cts-theme-frente-a-cts-manager-d15) · [Decisiones abiertas (D1–D23)](#decisiones-abiertas) · [Fuera de alcance](#fuera-de-alcance) · [Pasos siguientes](#pasos-siguientes)

## Modelo

El sistema tiene tres capas. Cada capa solo lee la capa de abajo.

```
primitivos (hex crudo)   →   roles (significado, claro/oscuro)   →   átomos × micro-estados
#0065BB                       brand.default                          button.contained.reposo.fondo
#004696                       brand.hover                            button.contained.hover.fondo
rgba(0,101,187,0.15)          focus.ring                             input.focus-visible.anillo
#d0d8e4 / rgba(74,…,0.25)     border.control                         input.reposo.borde
```

- **Primitivos** (`src/colors.ts`): valores crudos, sin significado. Un
  primitivo no sabe dónde se usa.
- **Roles** (`src/roles.ts`, paso 2): un nombre por trabajo (`text.disabled`,
  `border.control`), con un valor para claro y otro para oscuro. Cada valor
  apunta a un primitivo.
- **Átomos** (`src/atoms.ts`, paso 2): cada control del sistema con sus
  micro-estados. Cada estado apunta a un rol.
- **Overrides de MUI** (`src/mui/components.ts`, paso 2): leen solo átomos,
  nunca un hex. Esto resuelve la sección 1.10 de
  [`ESTILADO-Y-CONSUMO.md`](ESTILADO-Y-CONSUMO.md) («`theme.components`
  pendiente»). La compatibilidad de los nombres de slot entre MUI 6, 7 y 9 se
  comprueba en el paso 3 con `pnpm typecheck:matrix`.

Micro-estados, en este orden: **reposo · hover · activo · focus-visible ·
seleccionado · deshabilitado · error**. Algunos átomos tienen además
*abierto*, *arrastrando*, *bloqueado*, *cargando* o *vacío*.

### Leyenda

| Marca | Significado |
|---|---|
| `⚠ sin valor → MUI: …` | cts-manager no define ese estado. Hoy se ve el valor por defecto de MUI que se indica. Es un **hueco**: no se rellena sin una decisión. |
| `(D7)` | Remite a la decisión abierta D7 (sección «Decisiones abiertas»). |
| `[M]` | Valor medido en el navegador, no leído del código. |
| `NUEVO: …` | Rol que no estaba en la lista canónica. |
| `T:123` | `theme/ctsTheme.ts`, línea 123. Las demás rutas son relativas a `cts-manager/frontend/src`. |

### Trampa de `borderRadius` numérico

En `sx`, un `borderRadius` **numérico** se multiplica por
`shape.borderRadius` (10). Así, `borderRadius: 2` da 20px, y pasar
`radii.card` (12) como número da 120px. Los átomos siempre usan cadenas con
unidad (`'12px'`), igual que los ejemplos de `ESTILADO-Y-CONSUMO.md`. En
cts-manager hay unos 40 lugares con radios de 15, 20, 25, 30 y 35px que
salen de esta multiplicación (D7).

## La auditoría en cifras

Panel interactivo con todas las cifras y gráficos:
<https://claude.ai/artifact/FKkNFMpKYzz7MNDXfwmjUW> (privado; hay que
compartirlo para que otros lo abran).

| Métrica | Valor |
|---|---|
| Valores de color distintos | 373 (190 hex + 183 rgba/hsl) |
| Usos de color en el código | 1 511, en 132 de 360 archivos (sin pruebas) |
| Usos que ya cubre cts-theme | 774 (51 %), con solo 45 valores distintos |
| Hex que no están en cts-theme | 160 de 190: 60 de datos, 52 candidatos a rol, 47 locales, 1 fuga de MUI |
| Familias de casi-duplicados | 23 |
| Usos de `text.disabled` sin definir | 435 |
| Pares claro/oscuro escritos a mano | 98 pares distintos (144 usos) fuera del tema |
| Pasos de alfa distintos por color base | blanco 31 · negro 25 · azul de marca 24 · celeste 19 |
| Pasos de blanco con alfa en el rail | 24 en uso, 11 con token en `tokens.rail` |
| Usos en páginas con paleta propia | notas de versión 298 · documentos (formato) 136 |
| Tokens de cts-theme revisados | 139: 121 coinciden, 4 con deriva, 2 solo de la página de novedades, 8 solo de las hojas de diseño, 4 ambiguos |
| Estados de átomo sin valor | controles 59 · navegación 70 · datos y retroalimentación 69 (filas `UNDEFINED` en los informes) |

**Colores:** cero deriva. Cada color de `src/colors.ts` y de `palette(mode)`
coincide con cts-manager hoy. La deriva está en espaciado, tipografía y
movimiento (D15).

### Conclusiones del desarrollador

Podemos observar que 'cts-manager' no tiene un sistema de diseño definido y por tanto, las incompatibilidades, contradicciones, las no generalidades que se encuentren, son obra de un desarrollo que ha sido desaforado y sin una estructura de diseño clara.

Es nuestro deber hacer de esta plétora de colores, roles y componentes, una librería estructurada y escalable, de fácil uso y además optimizable en peso. Estas grandilocuentes metas, que por cierto, pueden llegar a ser fantasiosas, son por ahora, la base de la motivación de este proyecto.

Por eso mismo, una falta de consistencia como la vemos en los pares claro/oscuro, las variaciones en el alpha de varios colores, páginas con una paleta de colores propia y valores indefinidos que usan valores por defecto, son los problemas que debemos resolver desde este proyecto.

Utilizaremos un enfonque en reforzar los colores ideales, _la mayoría_ del tiempo.

## Capa 1 · Primitivos

### Existentes

Los de `src/colors.ts` (`palette`, `surface`, `surfaceDark`, `semantic`,
`semanticDark`, `secondary`, `data8`) se quedan como están. Notas:

- `palette.grayLight` `#C9C9C9` y `palette.grayDark` `#5A5A5A` tienen 0 usos
  fuera del tema. La app usa `#c8c8c8` (×15) y `#c4c4c4` (×9) (D9).
- `#29ABE2` es a la vez `palette.blueLight`, `secondary.main`,
  `semantic.info` y `data8[1]`: un primitivo, cuatro roles.

#### Notas del desarrollador

* En caso de `palette.grayLight` y `palette.grayDark` no sean usados, entonces se reemplazan por uso real, apuntando a no usar colores primitivos directamente cuando se instancia un componente o se codifica un estilo.

* Como data8 es un arreglo de colores para estados, podemos derivar un nombre y uso adecuado basado en los componentes, dividos en átomos, que los usan. 

* Queda abierta la pregunta al planteamiento de roles y componentes: _¿es ideal usar distintos roles para el mismo color?


### Nuevos (valores observados, a agregar en el paso 2)

Ninguno es inventado: todos aparecen en cts-manager. Los marcados con una
decisión no entran hasta resolverla.

| Primitivo propuesto | Valor | Usos | Dónde | Decisión |
|---|---|---:|---|---|
| `surface.rowHover` | `#f7fafd` | 2 | `T:260-261` fila de tabla (sólido a propósito, por las celdas sticky) | — |
| `surface.selected` | `#eff5fe` | 1 | `BoardGridV2.tsx:896` fila seleccionada | D12 |
| `surfaceDark.raised` | `#2d3c53` | 18 | cabecera de tabla, celdas de la grilla, banda de grupo | D12 |
| `surfaceDark.rowHover` | `#2f435e` | 1 | `T:260` | D12 |
| `surfaceDark.selected` | `#2f476d` | 1 | `BoardGridV2.tsx:896` | D12 |
| `surfaceDark.inverse` | `#1e2d42` | 2 | fondo y flecha del tooltip (`T:312,319`) | D19 |
| `surfaceDark.authPage` | `#1a1a2e` | 1 | `AuthPage.tsx:65` | D9 |
| `brandOnDark` | `#89AEDC` | 19 | texto de marca y enlaces sobre fondo oscuro | D14 |
| `darkAction` | `#4a90e2` (solo como `rgba(74,144,226,α)`) | 19 | `action.*` oscuro, divisor oscuro, borde de input oscuro | — |
| `scrollbar.*` | `#c0c8d4` `#a0aab8` / `#3d4f6f` `#4a6090` | tema | `T:88-115` | D18 |
| `neutralStatus` | `#c4c4c4` | 9 | color de estado vacío (`StatusCell.tsx:30`) | D9 |
| `successHover` | `#00a65c` | 2 | botón verde (`SharedViewPage.tsx:703`) | D9 |
| `focusRing` | `rgba(0,101,187,0.15)` | tema | anillo de foco del input (`T:191`) | D2 |
| `scrim` | `rgba(15,23,42,0.55)` | 4 | velo del recorrido guiado (`FeatureTour.tsx:212`) | — |

### Sombras

| Nivel | Claro | Oscuro | Fuente |
|---|---|---|---|
| `shadow.e1` | `0 1px 4px rgba(0,0,0,0.06)` | `0 1px 4px rgba(0,0,0,0.4)` | `T:75` |
| `shadow.e2` | `0 2px 8px rgba(0,0,0,0.08)` | `0 2px 8px rgba(0,0,0,0.45)` | `T:76` |
| `shadow.e3` | `0 4px 16px rgba(0,0,0,0.1)` | `0 4px 16px rgba(0,0,0,0.5)` | `T:77` |
| `shadow.e4` | `0 8px 24px rgba(0,0,0,0.12)` | `0 8px 24px rgba(0,0,0,0.55)` | `T:78` |
| `shadow.e5` | `0 12px 32px rgba(0,0,0,0.14)` | `0 12px 32px rgba(0,0,0,0.6)` | `T:79` |
| `shadow.e6` (y 7–24) | `0 16px 40px rgba(0,0,0,0.16)` | `0 16px 40px rgba(0,0,0,0.65)` | `T:80` |
| `shadow.paper` | `0 2px 8px rgba(0,0,0,0.07)` | `0 2px 8px rgba(0,0,0,0.4)` | `T:161-162` (choca con `e1`, D16) |
| `shadow.button` / `buttonHover` | `0 2px 8px rgba(0,101,187,0.3)` / `0 4px 12px rgba(0,101,187,0.4)` | igual | `T:132,135` |
| `shadow.buttonSecondary` / `…Hover` | `0 2px 8px rgba(41,171,226,0.3)` / `0 4px 12px rgba(41,171,226,0.4)` | igual | `T:140,143` (el hover no está en `tokens.shadows`) |
| `shadow.menu` | `0 8px 24px rgba(0,101,187,0.15)` | `0 8px 24px rgba(0,0,0,0.5)` | `T:381` |
| `shadow.dialog` | `0 24px 64px rgba(0,101,187,0.18)` | `0 24px 64px rgba(0,0,0,0.7)` | `T:284-285` |
| `shadow.sidebar` | `4px 0 20px rgba(0,0,0,0.2)` | igual | `Sidebar.tsx:431` |
| `shadow.tooltipRich` | `0 6px 20px rgba(0,101,187,0.12)` | `0 6px 20px rgba(0,0,0,0.45)` | `SharedViewPage.tsx:50-51` (D19) |

### Datos del usuario (swatches)

`data8` sigue siendo la paleta de datos (estados, grupos, gráficos), más el
neutro `#c4c4c4` para «sin color». Estos colores se guardan en la base de
datos de cts-manager como opciones, así que **no se cambian**, aunque fallen
en contraste (D8).

Otras familias existen pero son locales y quedan fuera de los roles: tipos de
archivo (12 colores), conformidad (`#d23b3b` `#15a86b` `#e08a1e` `#9aa3af`),
columnas gestionadas (Material 600–900), avatares (Tailwind 500), acentos del
constructor de formularios (22), roles de cuenta y roles de tablero (dos
paletas distintas para conceptos parecidos).

### Escaleras de alfa

Hoy cada componente elige su propio alfa. Ejemplos:

- **Blanco sobre el rail:** 24 pasos en uso. Activo `0.18` en
  `Sidebar.tsx:68` y `0.15` en `BoardList.tsx:102`. Hover `0.1`, `0.09`, `0.08`
  y `0.06` según el archivo (D10).
- **Tinte de marca:** el mismo «bloque teñido de azul» usa alfas de 0.04 a
  0.09 en claro y de 0.08 a 0.16 en oscuro, sobre **tres bases distintas**
  en oscuro (`0,101,187`, `41,171,226`, `74,144,226`) (D11).
- **Sufijos hex de `tint()`:** hay 17 sufijos en uso (`05` a `66`); `tint()`
  solo acepta `20` y `18`, que cubren 15 de 46 usos (D11).

## Capa 2 · Roles

Estado: **tema** = definido hoy en `ctsTheme.ts` · **nuevo** = observado en la
app, sin token · **MUI** = no definido, se ve el valor por defecto de MUI ·
**deriva** = el código usa varios valores.

| Rol | Claro | Oscuro | Estado | Decisión |
|---|---|---|---|---|
| `bg.canvas` | `#f0f4f9` | `#2A3547` | tema | — |
| `bg.surface` | `#ffffff` | `#253662` | tema | — |
| `bg.raised` | `#ffffff` | `#2d3c53` | nuevo | D12 |
| `bg.groupHeader` | `#f0f4f9` | `#2d3c53` | nuevo | D12 |
| `bg.tableHead` | `#0065BB` | `#2d3c53` | tema | — |
| `bg.rowHover` | `#f7fafd` | `#2f435e` | tema (deriva en 4 tablas) | D12 |
| `bg.selected` | `#eff5fe` | `#2f476d` | nuevo | D1, D12 |
| `bg.sunken` | `rgba(15,23,42,0.035)` | `rgba(255,255,255,0.045)` | nuevo (deriva) | D12 |
| `bg.rail` | `#0065BB` | `#253662` | nuevo (hoy literal en `Sidebar.tsx:428`) | — |
| `bg.inverse` | `#1a2236` | `#1e2d42` | tema | D19 |
| `bg.authPage` | `#f0f4f9` | `#1a1a2e` | nuevo | D9 |
| `text.primary` | `#1a2236` | `#e8edf4` | tema | — |
| `text.secondary` | `#5a6a80` | `#a6b4c8` | tema | — |
| `text.disabled` | `rgba(0, 0, 0, 0.38)` | `rgba(255, 255, 255, 0.5)` | MUI (435 usos) | D4 |
| `text.brand` | `#0065BB` | `#89AEDC` | nuevo | D14 |
| `text.onBrand` | `#ffffff` | `#ffffff` | tema | — |
| `text.onRail` / `text.onRailMuted` | `#ffffff` / `rgba(255,255,255,0.65)` | igual | tema (`tokens.rail`) | D10 |
| `text.onInverse` | `#ffffff` | `#ffffff` | tema (tooltip) | — |
| `border.subtle` | `#dde3ec` | `rgba(74,144,226,0.12)` | tema (oscuro usa también `0.1`) | D9 |
| `border.control` | `#d0d8e4` | `rgba(74,144,226,0.25)` | tema | — |
| `border.controlHover` | `#0065BB` (pedido) · `#1a2236` (renderiza) [M] | `rgba(41,171,226,0.5)` (pedido) · `#e8edf4` (renderiza) [M] | tema, sin efecto | D5 |
| `border.onRail` | `rgba(255,255,255,0.1)` | igual | tema (`tokens.rail`) | D10 |
| `brand.default` | `#0065BB` | `#0065BB` | tema | D14 |
| `brand.hover` | `#004696` | `#004696` | tema (deriva: `#0078d4`, `#2e4275`, `#1278cf`) | D13 |
| `brand.light` | `#29ABE2` | `#29ABE2` | tema | — |
| `brand.subtle` | `rgba(0,101,187,0.05)` | `rgba(41,171,226,0.10)` | nuevo (deriva) | D11 |
| `secondary.default` / `.hover` | `#29ABE2` / `#1a8ab8` | igual | tema | — |
| `focus.ring` | `0 0 0 3px rgba(0,101,187,0.15)` | igual | tema (solo input) | D2 |
| `overlay.hover` | `rgba(0,101,187,0.05)` | `rgba(74,144,226,0.08)` | tema | — |
| `overlay.selected` | `rgba(0,101,187,0.1)` | `rgba(74,144,226,0.16)` | tema (MUI no lo usa en MenuItem) | D1 |
| `overlay.focus` | `rgba(0, 0, 0, 0.12)` | `rgba(74,144,226,0.12)` | claro: MUI | D3 |
| `overlay.active` | `rgba(0, 0, 0, 0.54)` | `rgba(255,255,255,0.6)` | claro: MUI | D3 |
| `overlay.disabled` | `rgba(0, 0, 0, 0.26)` | `rgba(255,255,255,0.28)` | claro: MUI | D3 |
| `overlay.disabledBg` | `rgba(0, 0, 0, 0.12)` | `rgba(255,255,255,0.08)` | claro: MUI | D3 |
| `overlay.scrim` | `rgba(0, 0, 0, 0.5)` (Backdrop) · `rgba(15,23,42,0.55)` (recorrido) | igual | MUI / nuevo | — |
| `onRail.hover` / `onRail.selected` | `rgba(255,255,255,0.1)` / `0.18` | igual | tema (`tokens.rail`) | D10, D23 |
| `onRail.indicator` | `rgba(255,255,255,0.9)` | igual | tema (`tokens.rail`) | D10 |
| `onRail.searchBg` / `onRail.searchBgFocus` | `rgba(255,255,255,0.08)` / `0.12` | igual | tema / nuevo | D10 |
| `feedback.error.default` | `#e2445c` | `#ef4444` | tema | — |
| `feedback.warning.default` | `#fdab3d` | `#f59e0b` | tema | — |
| `feedback.success.default` | `#00c875` | `#22c55e` | tema | — |
| `feedback.info.default` | `#29ABE2` | `#06b6d4` | tema | — |
| `feedback.*.hover` | MUI calcula (`error.dark` `rgb(158, 47, 64)`…) · verde `#00a65c` | MUI calcula | MUI | D21 |
| `feedback.*.subtle` | alfa 0.05–0.08 sobre el color | alfa 0.06–0.12 | nuevo (deriva) | D11, D17 |
| `feedback.*.onColor` | error `#fff` · aviso, éxito, info `rgba(0, 0, 0, 0.87)` | igual | MUI | D21 |
| `scrollbar.track` / `.thumb` / `.thumbHover` | `#f0f4f9` / `#c0c8d4` / `#a0aab8` | `#253662` / `#3d4f6f` / `#4a6090` | tema (duplicado en `index.css`) | D18 |

### Roles nuevos que proponen las secciones de átomos

Aparecieron al mapear los átomos. Son valores observados; el nombre es una
propuesta.

| Rol propuesto | Claro | Oscuro | Dónde | Nota |
|---|---|---|---|---|
| `onRail.dangerHover` / `onRail.dangerHoverText` | `rgba(255,100,100,0.2)` / `rgba(255,180,180,1)` | igual | «Cerrar sesión» (`tokens.rail.logoutHover*`) | ya existe como token del rail |
| `bg.unread` | `rgba(0,101,187,0.04)` | `rgba(0,101,187,0.08)` | fila no leída de notificaciones | en oscuro usa la base de claro (D11) |
| `bg.readOnly` | `rgba(15,23,42,0.035)` | `rgba(255,255,255,0.045)` | celda de solo lectura | mismo valor que `bg.sunken`; probablemente un solo rol |
| `border.onHead` | `rgba(255,255,255,0.12)` | `rgba(74,144,226,0.12)` | separador derecho de la cabecera de tabla (`T:235`) | — |
| `border.brandSoft` | `#0065BB` al 50 % (MUI) | igual | borde del botón outlined | lo calcula MUI (D21) |

## Capa 3 · Átomos

Una tabla por átomo y variante. Cada celda da el rol y su valor literal
(claro / oscuro). Las tres secciones siguientes son Controles, Navegación y
capas flotantes, y Datos y retroalimentación.

## Controles

Convenciones de esta sección: `L / D` = claro / oscuro (un solo valor = igual en ambos modos). `[M]` = medido en navegador. `MUI:` = `node_modules/@mui/material` v7.3.9. Los hovers integrados de MUI (Button text/outlined, IconButton, Checkbox, Radio, Switch) usan `alpha(<color del componente>, hoverOpacity)` con hoverOpacity 0.04 L / 0.08 D; **no** leen `action.hover` (0.05 L / 0.08 D) del tema (D21). Cuando un hover sale de ahí se escribe el literal medido, no el rol `overlay.hover`.

### Button — contained primary
Fuente: `T:131-136` (override `containedPrimary`), `T:124-129` (base), `T:20` (palette), `T:66` (typography.button). ~74 usos.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `brand.default` `#0065BB` | `text.onBrand` `#fff` | ninguno | `shadow.button` `0 2px 8px rgba(0,101,187,0.3)` | `radii.control` 8px · padding `6px 16px` (MUI) · alto 36.5px [M] · 14px / `fontWeight` 600 / ls `0.01em` / `textTransform: none` · `motion.control` `all 0.2s ease` |
| hover | `brand.hover` `#004696` | `#fff` | — | `shadow.buttonHover` `0 4px 12px rgba(0,101,187,0.4)` | — |
| activo (pressed) | ⚠ sin valor → MUI: igual que hover (la regla hover del tema gana sobre `shadows[8]`) (D3) | `#fff` | — | ⚠ sin valor → MUI: igual que hover | ripple `currentColor` `#fff`, opacidad 0.3, scale 0→1, 550ms `cubic-bezier(0.4,0,0.2,1)` (MUI:ButtonBase/TouchRipple.js:15-107) |
| focus-visible | ⚠ sin valor → MUI: igual que reposo (D2) | `#fff` | `outline: 0` | ⚠ sin valor → MUI: `0 16px 40px rgba(0,0,0,0.16)` L / `0 16px 40px rgba(0,0,0,0.65)` D (`shadows[6]`) [M] (D6) | ripple pulsante 0.3, 2500ms, infinito; `focus.ring` no aplicado |
| deshabilitado | `overlay.disabledBg` ⚠ sin valor L → MUI: `rgba(0,0,0,0.12)` (D3) / D `rgba(255,255,255,0.08)` (`T:39`) | `overlay.disabled` ⚠ sin valor L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` (`T:38`) | ninguno | `none` | `cursor: default`, `pointer-events: none` (MUI:ButtonBase.js:75-79) |
| cargando | = deshabilitado | = deshabilitado | — | `none` | patrón: `disabled` + `<CircularProgress size 14\|16 color="inherit"/>` en `startIcon` (o spinner que reemplaza la etiqueta, size 22); la prop `loading` de MUI 7 no se usa; spinner `color="inherit"` = color deshabilitado (muy tenue) |

Notas:
- `disableElevation` no funciona en primary/secondary: la sombra azul del tema gana sobre `boxShadow: none` de MUI (9 usos: DialogoCampoNuevo.tsx:140, MisPlantillas.tsx:228,258,273 …); el hover del tema también gana sobre `sx boxShadow:'none'`.
- Foco por teclado = sombra gigante accidental (G1), casi seguro no intencionada; el input sí tiene `focus.ring`, el botón no (D2, D6).
- Contraste blanco sobre `#0065BB` 5.87:1.

### Button — contained secondary
Fuente: `T:139-144`, `T:21`. **0 usos** en el código de la app (solo está estilado en el tema).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `secondary.default` `#29ABE2` | `text.onBrand` `#fff` | ninguno | `shadow.buttonSecondary` `0 2px 8px rgba(41,171,226,0.3)` | mismas métricas que contained primary; contraste blanco 2.62:1 |
| hover | `secondary.hover` `#1a8ab8` | `#fff` | — | `shadow.buttonSecondaryHover` `0 4px 12px rgba(41,171,226,0.4)` | — |
| activo | ⚠ sin valor → MUI: igual que hover + ripple (D3) | `#fff` | — | — | — |
| focus-visible | ⚠ sin valor → MUI: `0 16px 40px rgba(0,0,0,0.16)` L / `…0.65` D (D6) | `#fff` | `outline: 0` | idem | (D2) |
| deshabilitado | `overlay.disabledBg` ⚠ sin valor L → MUI: `rgba(0,0,0,0.12)` (D3) / D `rgba(255,255,255,0.08)` | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` | — | `none` | — |

Notas:
- `shadow.buttonSecondaryHover` no existe en `tokens.shadows` de cts-manager (solo en el tema: `T:144`) (D15).

### Button — outlined
Fuente: `T:146-149` (`borderWidth: '1.5px'` también en hover); resto MUI. ~44 `small` + 20 `medium`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `brand.default` `#0065BB` / `#0065BB` (D14) | `borders.emphasis` 1.5px solid `rgba(0,101,187,0.5)` (NUEVO: `border.brandSoft`; MUI `alpha(main,.5)`, D21) | ninguna | `radii.control` 8px · padding `5px 15px` + borde · `motion.control` |
| hover | `rgba(0,101,187,0.04)` L / `rgba(0,101,187,0.08)` D (MUI derivado, D21) | `#0065BB` | `border.brand` `#0065BB` | ninguna | — |
| activo | ⚠ sin valor → MUI: igual que hover + ripple 0.3 (D3) | `#0065BB` | — | — | — |
| focus-visible | ⚠ sin valor → MUI: sin cambio estático, solo ripple pulsante; sin anillo [M] (D2, D6) | — | — | ⚠ sin valor | — |
| deshabilitado | transparente | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` | `1px solid` `overlay.disabledBg` ⚠ L → MUI: `rgba(0,0,0,0.12)` (D3) / D `rgba(255,255,255,0.08)` | — | el ancho baja a 1px (la regla MUI gana al 1.5px del tema) |

Variantes de color (mismos estados, mismo patrón `alpha(color, hoverOpacity)`):

| Color | Texto / borde reposo | Hover (fondo) | Fuente |
|---|---|---|---|
| error | `feedback.error.default` `#e2445c` / `#ef4444`; borde `rgba(226,68,92,0.5)` / `rgba(239,68,68,0.5)` | `rgba(226,68,92,0.04)` / `rgba(239,68,68,0.08)` | FormBuilder.tsx:2211,2282,2328; LinkBoardsDialog.tsx:1447 |
| inherit | `text.primary` `#1a2236` / `#e8edf4`; borde = `currentColor` | `rgba(26,34,54,0.04)` / `rgba(232,237,244,0.08)` | LinkBoardsDialog.tsx:884; UpdateAvailableBanner.tsx:61 |
| toolbar (estilo de casa) | `text.secondary` `#5a6a80` / `#a6b4c8`; borde `border.subtle` `#dde3ec` / `rgba(74,144,226,0.12)` | borde y texto → `brand.default` `#0065BB`; fondo MUI `rgba(0,101,187,0.04)` L / `0.08` D | ViewToolbar.tsx:98-101 (12px/600) |

Notas:
- Dos copias del botón de toolbar: ViewToolbar.tsx:98-101 (12px, sin fondo hover) vs BoardToolbar.tsx:16-22 (13px, `bgcolor: "primary.50"`, clave inexistente, el hover se ignora) (D20).
- `#0065BB` como texto/borde sobre superficies oscuras = 2.01:1 `#253662` (D14).
- Alto outlined small 31px [M] vs `density.toolbarControl` 32 (D15).

### Button — text
Fuente: MUI (`--variant-textColor`); `T:150` para `small`. ~120 `small` + 63 planos (sobre todo "Cancelar").

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `brand.default` `#0065BB` / `#0065BB` (D14) | ninguno | ninguna | `radii.control` 8px · padding medium `6px 8px` |
| hover | `rgba(0,101,187,0.04)` L / `rgba(0,101,187,0.08)` D (MUI derivado, D21) | `#0065BB` | — | — | — |
| activo | ⚠ sin valor → MUI: solo ripple, sin cambio estático (D3) | — | — | — | — |
| focus-visible | ⚠ sin valor → MUI: solo ripple pulsante; sin anillo (D2, D6) | — | — | ⚠ sin valor | — |
| deshabilitado | transparente | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` | ninguno | — | — |

Variantes de color:

| Color | Texto reposo | Hover (fondo) | Fuente |
|---|---|---|---|
| inherit (27 "Cancelar") | `text.primary` `#1a2236` / `#e8edf4` | `rgba(26,34,54,0.04)` / `rgba(232,237,244,0.08)` | DeleteDialog.tsx:112; MoveToBoardDialog.tsx:588 |
| error (×6) | `feedback.error.default` `#e2445c` / `#ef4444` | `rgba(226,68,92,0.04)` / `rgba(239,68,68,0.08)` | BatchActionBar.tsx:336; AutomationBuilder.tsx:1057; LockByStatusDialog.tsx:270; RequireColumnsDialog.tsx:174; MisPlantillas.tsx:257; ShareTemplateDialog.tsx:132 |
| fantasma tipo link | rest `text.secondary`/`text.disabled`; hover `brand.default` o `feedback.error.default`/`feedback.warning.default`; `bgcolor: transparent` | — | AutomationBuilder.tsx:499-504; LinkBoardsDialog.tsx:630-634,1459-1466; editores.tsx:241; GlobalCommentsPage.tsx:238 |

Notas:
- Estado `seleccionado` no existe en Button (ToggleButton fuera de este audit).

### Button — tamaños
Fuente: `T:150` (small), MUI Button.js:212-258 (resto).

| Tamaño | Padding | Fuente | Alto | Otros |
|---|---|---|---|---|
| small | `4px 12px` (override del tema, reemplaza `3px 9px` de MUI; aplica a **todas** las variantes) | 13px (0.8125rem) | — (outlined small 31px [M]) | NUEVO: `density.buttonSmall` (padding `4px 12px`, fs 0.8125rem); `startIcon` margen `-2px` |
| medium (por defecto) | contained `6px 16px` · outlined `5px 15px` + borde · text `6px 8px` (MUI) | 14px (typography.button, lh 1.75) | 36.5px contained [M] | `startIcon` margen `-4px 8px -4px`, ícono 20px (la app lo baja a 14-18px por `sx`) |
| large | `7px 21px` (MUI) | 15px | 42.25px | ⚠ sin valor en tema → MUI (4 usos); ícono 22px |

Notas:
- `radii.control` 8px es el único radio del tema para Button; hay `sx borderRadius: 2` (=20px) en 17 sitios (FileGalleryDialog.tsx:215,395; TeamsAdminPanel.tsx:486,538,684,728,756,779,828,855; AdminPage.tsx:340,631,707,867; TemplatesPage.tsx:158 …), `1.5` (=15px) en StatusCell.tsx:348,566 y `999` en InsertarBloque.tsx:251,255 (D7).
- El easing real del botón es `ease` (CSS), no `tokens.motion.easing` `cubic-bezier(0.32,0.72,0,1)` ni el de MUI (`T:128` reemplaza la transición de MUI) (D15).

### Botón verde personalizado (#00c875)
Fuente: `features/shared-view/SharedViewPage.tsx:703-705` (toolbar), `:809-811` (diálogo). "Aplicar cambios / Aplicar". Contained con `sx` local, sin soporte del tema.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `feedback.success.default` `#00c875` / `#00c875` (no cambia a `#22c55e` en oscuro) (D8) | `feedback.success.onColor` `#fff` (contraste 2.21:1, D8) | ninguno | `none` (`boxShadow:'none'`) | `radii.control` `'8px'` · toolbar: 12px/700, alto 34, `px 2`, `size="small"`, `nowrap` · diálogo: 14px/700, alto auto (36.5) |
| hover | `feedback.success.hover` `#00a65c` (literal; no está en colors.ts) | `#fff` | — | **fuga**: `0 4px 12px rgba(0,101,187,0.4)` azul [M] (el tema `T:135` gana sobre `sx` base) | no intencionado (G2) |
| activo | ⚠ sin valor → MUI: igual que hover + ripple (D3) | `#fff` | — | — | — |
| focus-visible | ⚠ sin valor → MUI: igual que reposo (D2) | `#fff` | `outline: 0` | ⚠ sin valor → MUI: `0 16px 40px rgba(0,0,0,0.16)` L / `…0.65` D [M] (D6) | — |
| deshabilitado | `overlay.disabledBg` ⚠ L → MUI: `rgba(0,0,0,0.12)` (D3) / D `rgba(255,255,255,0.08)` | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` | — | — | el verde no sobrevive a `disabled` (SharedViewPage.tsx:798) |
| cargando | = deshabilitado | spinner `size 14 color="inherit"`, etiqueta "Aplicando..." | — | — | SharedViewPage.tsx:799-806,812 |

Notas:
- Hermano ámbar de desbloqueo: `#fdab3d` reposo / `#e69b2e` hover (`feedback.warning.default` / `feedback.warning.hover`), `boxShadow: none`, 700, `'8px'`, texto blanco 1.9:1 (SignatureCell.tsx:357; StatusCell.tsx:707) (D8).
- `Button color="success"` estándar da texto `rgba(0,0,0,0.87)` sobre `#00c875` y hover derivado `rgb(0,140,81)` (ApprovalDialog.tsx:229), distinto de este botón: blanco / `#00a65c` (D8, D21).
- Botón de acento dinámico (form público): `bgcolor: accent`, `color: textOn(accent)`, hover `filter: brightness(0.9)` (FormPublicPage.tsx:351-353); la celda de estado usa 0.88 (D15).

### Button — destructivo (color="error")
Fuente: sin override en el tema (MUI con la paleta); ~16 usos contained: DeleteDialog.tsx:112-119; BatchActionBar.tsx:614,625; GroupContextMenu.tsx:124,129; ItemContextMenu.tsx:177; FileGalleryDialog.tsx:390; AdminPage.tsx:867 …

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `feedback.error.default` `#e2445c` / `#ef4444` | `feedback.error.onColor` `#fff` (auto MUI) | ninguno | `shadow.e2` `0 2px 8px rgba(0,0,0,0.08)` L / `…0.45` D (neutra, no azul) | métricas = contained primary |
| hover | `feedback.error.hover` `rgb(158,47,64)` L / `rgb(167,47,47)` D (derivado por MUI, no literal; D21) | `#fff` | — | `shadow.e4` `0 8px 24px rgba(0,0,0,0.12)` L / `…0.55` D | — |
| activo | ⚠ sin valor → MUI: bg de hover; sombra `0 16px 40px rgba(0,0,0,0.16)` L / `…0.65` D (`shadows[8]`) (D3) | `#fff` | — | — | — |
| focus-visible | ⚠ sin valor → MUI: igual que reposo (D2) | `#fff` | `outline: 0` | ⚠ sin valor → MUI: `0 16px 40px rgba(0,0,0,0.16)` L / `…0.65` D [M] (D6) | — |
| deshabilitado | `overlay.disabledBg` ⚠ L → MUI: `rgba(0,0,0,0.12)` (D3) / D `rgba(255,255,255,0.08)` | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` | — | `none` | — |

Notas:
- Variantes outlined/text de `color="error"` están en sus bloques; `contained` ignora los tokens `shadow.button*` (familia azul solo para primary/secondary).
- `error.light/dark` los calcula MUI (D21).

### IconButton — por defecto
Fuente: sin override en el tema (no hay `MuiIconButton`); MUI IconButton.js:50-151. `size="small"` en 186 de 192 usos.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | ⚠ sin valor L → MUI: `rgba(0,0,0,0.54)` (action.active, D3) / D `rgba(255,255,255,0.6)` (`T:35`) | ninguno | ninguna | radio `50%` (NUEVO: `radii.circle`) · small padding 5 / ícono 18px / 30×30 · medium 8 / 24px / 40 · large 12 / 28px |
| hover | ⚠ sin valor L → MUI: `rgba(0,0,0,0.04)` / D `rgba(255,255,255,0.08)` (`alpha(active, hoverOpacity)`; no es `overlay.hover` 0.05) (D3) | — | — | — | `motion.nav` `background-color 0.15s cubic-bezier(0.4,0,0.2,1)` [M] |
| activo | ⚠ sin valor → MUI: bg de hover + ripple 0.3 (D3) | — | — | — | — |
| focus-visible | ⚠ sin valor → MUI: solo ripple pulsante; sin anillo (D2) | — | — | ⚠ sin valor | — |
| deshabilitado | transparente | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` | — | — | `cursor: default` |

Variantes (solo cambia el color; hover = color × hoverOpacity):

| Variante | Reposo | Hover | Fuente |
|---|---|---|---|
| `color="primary"` | `brand.default` `#0065BB` | fondo `rgba(0,101,187,0.04)` L / `0.08` D | ChartSettingsDialog.tsx:229; KpiEditorDialog.tsx:109 |
| `color="error"` | `feedback.error.default` `#e2445c` / `#ef4444` | fondo `rgba(226,68,92,0.04)` / `rgba(239,68,68,0.08)` | TemplateDetailPage.tsx:482; AutomationList.tsx:347; TeamsAdminPanel.tsx:641 |
| toolbar (estilo de casa) | `text.secondary` `#5a6a80` / `#a6b4c8` | ícono `brand.default` `#0065BB` (2.01:1 en oscuro, D14); fondo `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | BoardToolbar.tsx:98-121; ReleaseHeader.tsx:97; BoardGridV2.tsx:1415 |
| destructivo (~30 usos) | `text.disabled` ⚠ L → MUI: `rgba(0,0,0,0.38)` / D `rgba(255,255,255,0.5)` (D4) | ícono `feedback.error.default` `#e2445c` / `#ef4444`; fondo hover MUI `rgba(0,0,0,0.04)` / `rgba(255,255,255,0.08)` | FormBuilder.tsx:3096,3120,3189; StatusCell.tsx:519; DropdownCell.tsx:275; NotificationBell.tsx:317 |
| revelar al pasar por la fila | `opacity` 0 → 1 | `transition: opacity` 0.15s (`motion.nav`) / `.12s` (`motion.micro`) / `.1s` | DropdownCell.tsx:266-275; ViewTabBar.tsx:130,453; DateCell.tsx:103 |

Notas:
- Rojo permanente: `error.main` siempre (SharedViewsPanel.tsx:142; MembersDialog.tsx:220; BoardMembersDialog.tsx:246).
- Tres duraciones (0.1 / 0.12 / 0.15s; también 0.2s en TemplatesPage.tsx:264) para el mismo patrón "revelar al hover" (D15).
- Hover del tema (`action.hover`) solo aplica donde el `sx` lo pide; el hover nativo del IconButton ignora `action.hover` (D3).

### IconButton — sobre rail
Fuente: `layout/sidebar/Sidebar.tsx:463,571-594`; `BoardList.tsx:119-126,231`; `PersonalFoldersSection.tsx:102,199,434`. Mismos literales en L y D (el rail es sólido: `bg.rail` `#0065BB` L / `#253662` D).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (colapsar cabecera) | transparente | `text.onRail` `rgba(255,255,255,0.7)` (tokens.rail.itemIdleColor = 0.65, D10) | ninguno | ninguna | — |
| hover | `onRail.hover` `rgba(255,255,255,0.1)` | `#fff` | — | — | — |
| reposo ("…" del workspace, 24×24) | transparente | `text.onRailMuted` `rgba(255,255,255,0.55)` (D10) | — | — | radio 6px = `radii.chip` |
| hover | `rgba(255,255,255,0.12)` (D10) | `#fff` | — | — | — |
| reposo ("⋮" del board, aparece en hover de fila) | transparente | `rgba(255,255,255,0.6)` (D10) | — | — | `opacity` 0→1 `transition: opacity 0.12s` (`motion.micro`) |
| hover | `rgba(255,255,255,0.15)` (D10) | `#fff` | — | — | — |
| reposo ("⋮" de carpeta, p 0.25) | transparente | `rgba(255,255,255,0.5)` (0.6 en add-folder) (D10) | — | — | hover → `#fff`, sin fondo |
| reposo / hover ("+" nuevo board, 26×26) | **`rgba(25,118,210,0.9)`** / hover **`#1976d2`** (azul por defecto de MUI, no el azul CTS; D20) | `#fff` | — | — | radio 7px · `transition: all 0.15s` · hover `transform: scale(1.05)` |
| activo / focus-visible | ⚠ sin valor → MUI: solo ripple (D2, D3) | — | — | ⚠ sin valor | — |
| deshabilitado | transparente | ⚠ sin valor → MUI: `rgba(0,0,0,0.26)` L / `rgba(255,255,255,0.28)` D = gris oscuro sobre azul (D3) | — | — | — |

Notas:
- Escalera de alfas blancas: reposo 0.7 / 0.65 / 0.6 / 0.55 / 0.5; hover bg 0.1 / 0.12 / 0.15 (D10).
- Sobre tarjetas de color: `rgba(255,255,255,0.7)` → `#fff`, hover `rgba(255,255,255,0.15)` (WorkspacesPage.tsx:175-181; BoardsPage.tsx:160); sobre visor oscuro `#fff` / `alpha('#fff',0.15)` (FilePreviewDialog.tsx:369-390; PdfViewer.tsx:163-181) (D10).

### Botón flotante para reabrir el sidebar
Fuente: `layout/AppLayout.tsx:34-37`. IconButton `size="small"`, `ChevronRight`, `position: sticky`, top 12, `ml 1.5`, `mt 1.5`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `brand.default` `#0065BB` / `bg.surface` `#253662` | `text.onBrand` `white` | ninguno | `shadow.e1` `0 1px 4px rgba(0,0,0,0.06)` L / `0 1px 4px rgba(0,0,0,0.4)` D (`boxShadow: 1`) | 30×30 [M] vs `density.floatingAction` 38 (D15) |
| hover | `#0078d4` L / `#2e4275` D (literales fuera de toda paleta; D13) | `white` | — | — | — |
| activo | ⚠ sin valor → MUI: ripple (D3) | — | — | — | — |
| focus-visible | ⚠ sin valor → MUI: solo ripple (D2) | — | — | ⚠ sin valor | — |
| deshabilitado | ⚠ sin valor → MUI (D3) | — | — | — | — |

Notas:
- Familia parecida: campana de notificaciones (`NotificationBell.tsx:165-181`): `bg.surface` `#fff` / `#253662`, borde `border.subtle` `1px solid #dde3ec` / `rgba(74,144,226,0.12)`, `shadow.e1`, hover `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)`, 32×32 [M] (D15).
- "+" de huecos del form builder 22×22: `brand.default` / hover `brand.hover`, `transform: scale(1.2)`, `transition .12s` (FormBuilder.tsx:3235-3244; shell.tsx:77-86).

### Input (OutlinedInput / TextField)
Fuente: `T:182-202`; `T:182` `MuiTextField.defaultProps.variant = 'outlined'`; resto MUI OutlinedInput.js. `size="small"` en 221 de 244 usos.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente (MUI: ninguno) | `text.primary` `#1a2236` / `#e8edf4`; label `text.secondary` `#5a6a80` / `#a6b4c8` | `border.control` `borders.emphasis` 1.5px solid `#d0d8e4` / `rgba(74,144,226,0.25)` | ninguna | `radii.control` 8px · 15px (body1) · small: input `8.5px 14px`, alto 38.56px [M]; medium `16.5px 14px` / 54.56px · `motion.control` `box-shadow 0.2s` · placeholder ⚠ sin valor → MUI: `currentColor` opacidad 0.42 L / 0.5 D (D4) |
| hover | sin cambio | — | `border.controlHover` **renderizado** `#1a2236` L / `#e8edf4` D (= `text.primary`); **pedido por el tema** `#0065BB` L / `rgba(41,171,226,0.5)` D (`T:197-199`, código muerto) (D5) | ninguna | sin transición en el fieldset (instantáneo) |
| activo (press) | = focus (el campo toma foco al presionar) | — | — | — | — |
| focus-visible | label `brand.default` `#0065BB` (2.01:1 en oscuro, D14) | — | `border.brand` `borders.accent` 2px solid `#0065BB` (el 1.5px del tema no aplica con foco) | `focus.ring` `0 0 0 3px rgba(0,101,187,0.15)` en el root (`T:190-192`) | los inputs ignoran `:focus-visible`: borde + anillo aparecen también con foco de mouse (D2) |
| seleccionado | n/a | — | — | — | — |
| deshabilitado | ninguno | `text.disabled` ⚠ L → MUI: `rgba(0,0,0,0.38)` / D `rgba(255,255,255,0.5)` (D4); `-webkit-text-fill-color` igual | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` (el `#d0d8e4` del tema se sobrescribe) | — | `cursor: default` |
| error | — | label y helperText `feedback.error.default` `#e2445c` / `#ef4444` | `feedback.error.default` 1.5px (2px con foco); hover sin cambio | ⚠ sin valor: el anillo sigue **azul** `0 0 0 3px rgba(0,101,187,0.15)` (no hay anillo de error) (D2) | helperText 12px `text.secondary`, margen `3px 14px 0` |

Variantes y tamaños:

| Variante | Valor | Fuente |
|---|---|---|
| multiline | root padding `8.5px 14px` (small) / `16.5px 14px` (medium); input `padding: 0` | MUI OutlinedInput.js:94-105 |
| adornment de inicio | ícono `rgba(0,0,0,0.54)` L / `rgba(255,255,255,0.6)` D (action.active, D3); la app pone 16-18px y `text.secondary`/`text.disabled` | AuthPage.tsx:174-183; ViewToolbar.tsx:115-117 |
| búsqueda de toolbar | `width: 200`, root `fontSize 13`, `height: 32` (`density.toolbarControl`), input sigue en `8.5px 14px` | ViewToolbar.tsx:108-115 |
| búsqueda de vista compartida | root `height: 34`, ancho `{xs:'100%', md:200}` | SharedViewPage.tsx:679 |
| edición compacta de fila | root `height: 26` (`density.inlineEdit`), 13px/600, `fieldset borderColor: primary.main` siempre, input `p: '2px 6px'` | ItemRow.tsx:398; PrimaryColumnHeader.tsx:26-33; ColumnHeaderCell.tsx:105-110 |
| aún más pequeño | alto 24 / 22, fs 11 / 10, peso 700 | TemplateItemsTable.tsx:262,560 |
| edición en línea (`variant="standard"` `disableUnderline`) | reposo transparente, `borderRadius: 1` = 10px (`radii.base`), hover `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)`, foco: bg igual + `0 0 0 2px rgba(41,171,226,0.45)` (otro anillo; D2), `transition .12s` (`motion.micro`) | piezas.tsx:81-86; shell.tsx:172-176; FormBuilder.tsx:3032-3037 |
| editores de celda (Number/Email/Phone) | `standard` + `disableUnderline`, `px 1`, 13px: sin hover/foco/error/deshabilitado (solo caret) | NumberCell.tsx:34-47; EmailCell.tsx:23-37; PhoneCell.tsx:28-42 |
| autofill (solo AuthPage) | fondo `#e8f0fe` L / `#253662` D; texto y caret `#1a1a1a` L / `#fff` D (no son `text.primary`); en el resto de formularios: MUI (`0 0 0 100px #266798 inset` en oscuro) | AuthPage.tsx:19-23,66-67 |
| radio ≠ 8 | `borderRadius: 2` (=20px), `1.5` (=15px), `1` (=10px), `999` | AdminPage.tsx:376,436; TeamUsersGlobalPanel.tsx:75,80; TeamsAdminPanel.tsx:416,554; TrashPanel.tsx:245; InsertarBloque.tsx:152 (D7) |
| `type="date"/"time"` nativos | solo el cascarón outlined está tematizado | FormPublicPage.tsx:510-511; DateCell.tsx:143 |

Notas:
- Hover del borde: el tema pide azul, MUI gana por especificidad (`&:hover .notchedOutline` > `&:hover fieldset`); la hoja de diseño aún documenta el azul (`docs/demo/build.py:288`) (D5).
- Único átomo con anillo de foco (`T:190-192`) y no es consistente con edición en línea (`rgba(41,171,226,0.45)`), pill (`0 0 0 2px rgba(41,171,226,0.55)`, FormBuilder.tsx:3266) ni con el error (D2).
- Label con foco en `#0065BB` sobre fondos oscuros = 2.01:1 (D14).

### InputBase en popovers
Fuente: DropdownCell.tsx:192-197,294; LabelCell.tsx:64-67; StatusCell.tsx:288-292,422. Sin borde ni fondo; la fila lleva solo `borderBottom: 1px solid divider` (`border.subtle` `#dde3ec` / `rgba(74,144,226,0.12)`).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | ninguno | `text.primary`; 13px (12px "Nueva opción"), `flex: 1`; ícono `SearchIcon` 16px `text.secondary` (DropdownCell, LabelCell) **o** `text.disabled` (StatusCell.tsx:287) | `border.subtle` solo inferior de la fila, 1px (`borders.hairline`) | ninguna | placeholder ⚠ sin valor → MUI: `currentColor` 0.42 L / 0.5 D (D4) |
| hover | ⚠ sin valor → MUI: ninguno | — | — | — | — |
| focus-visible | ⚠ sin valor → MUI: solo caret (D2) | — | — | ⚠ sin valor | — |
| deshabilitado / error | ⚠ sin valor → MUI: ninguno | — | — | — | — |
| renombrar opción (editor de estados) | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` (hover y foco) | tachado si está deshabilitada | — | — | radio `1` = 10px (`radii.base`), `px 0.75 py 0.4` (StatusCell.tsx:475-487) |

Notas:
- Ícono de búsqueda inconsistente: `text.secondary` vs `text.disabled` (D4).

### Búsqueda del rail
Fuente: `layout/sidebar/BoardSearch.tsx:63-118`. Mismos literales en L y D (blanco-alfa sobre `bg.rail`).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `onRail.searchBg` `rgba(255,255,255,0.08)` | texto `#fff` 12.5px; placeholder `text.onRailMuted` `rgba(255,255,255,0.4)` (opacidad 1); ícono 15px `rgba(255,255,255,0.45)` (D10) | `border.onRail` 1px (`borders.hairline`) solid `rgba(255,255,255,0.15)` | ninguna | `radii.base` 10px (no 8) · alto 34 · `px 1.25` (10px) · `gap 0.75` (6px) · `motion.nav` `all 0.15s` |
| hover | ⚠ sin valor (no hay regla) | — | — | — | — |
| activo | ⚠ sin valor | — | — | — | — |
| focus-visible (`:focus-within`) | `onRail.searchBgFocus` `rgba(255,255,255,0.12)` | — | `border.onRail` `rgba(255,255,255,0.35)` | ninguna (solo borde/fondo; D2) | — |
| deshabilitado / error | n/a | — | — | — | — |
| cargando | — | spinner `CircularProgress size 18`, `rgba(255,255,255,0.5)` | — | — | — |
| botón limpiar | — | `rgba(255,255,255,0.5)` → `#fff` en hover, p 0.25, ícono 13px | — | — | — |
| fila de resultado (hover) | `rgba(255,255,255,0.12)` | título 12.5px/600 `#fff`; contexto 10px `rgba(255,255,255,0.45)` | — | — | radio `'8px'`, `px 1 py 0.7`, `transition: background-color 0.12s` |

Notas:
- Alfas blancas 0.08 / 0.12 / 0.15 / 0.35 / 0.4 / 0.45 / 0.5: escalera sin consolidar (D10).

### Select / Autocomplete
Fuente: sin `MuiSelect` ni `MuiAutocomplete` en el tema; el campo es un OutlinedInput (aplican todas las filas de **Input**, incluida la anomalía del hover D5). Menú: `T:375-398`; popup del Autocomplete: `T:156-163`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| campo reposo | transparente | flecha 24px `rgba(0,0,0,0.54)` L / `rgba(255,255,255,0.6)` D (action.active, D3); gira 180° al abrir | `border.control` (ver Input) | ninguna | padding-right 32px, `cursor: pointer`; `fontSize 13` (12 en toolbar), `minWidth` 120-200, compacto `height: 30` (`layout.toolbarSelectMin/MaxWidth` 135/185) |
| campo hover / focus-visible / error / deshabilitado | = Input | = Input | = Input (hover D5) | `focus.ring` en foco (D2) | — |
| abierto (menú) | `bg.raised` ⚠ sin valor en el audit | — | `border.subtle` 1px solid `#dde3ec` / `rgba(74,144,226,0.1)` | `shadow.menu` `0 8px 24px rgba(0,101,187,0.15)` L / `0 8px 24px rgba(0,0,0,0.5)` D | `radii.base` 10px (`T:377-385`) |
| MenuItem reposo | transparente | 14px (0.875rem) | ninguno | — | `radii.chip` 6px · margen `2px 6px` · padding `7px 10px` · `motion.nav` `background 0.15s` |
| MenuItem hover | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | — | — | — | — |
| MenuItem seleccionado | `rgba(0,101,187,0.08)` L / `rgba(0,101,187,0.16)` D (MUI: `alpha(primary, selectedOpacity)`; **no** `overlay.selected` 0.1 / 0.16 de `74,144,226`) (D1) | — | — | — | + hover `rgba(0,101,187,0.12)` / `0.24`; + focus-visible `rgba(0,101,187,0.2)` / `0.28` (MUI, D1) |
| MenuItem deshabilitado | — | `opacity: 0.38` (MUI) | — | — | — |
| Autocomplete popup | `bg.raised` ⚠ sin valor | indicador `rgba(0,0,0,0.54)` L / `rgba(255,255,255,0.6)` D | — | `0 2px 8px rgba(0,0,0,0.07)` L / `…0.4` D (D16) | `radii.card` 12px |
| Autocomplete opción | hover `overlay.hover`; seleccionada `rgba(0,101,187,0.12)` L / `0.24` D (MUI, D1) | 15px | — | — | padding `6px 16px` (MUI); input con `fontSize: 12` por `sx` |
| activo / cargando | ⚠ sin valor → MUI (hereda el foco de OutlinedInput: 2px `#0065BB` + anillo 3px) | — | — | — | `loadingText` en AdminPage.tsx:738 |

Notas:
- Radio ≠ 8: `borderRadius: 2` (=20px) en TemplatesPage.tsx:184,191 (D7).
- Selected del MenuItem/Autocomplete usa primary@0.08/0.16/0.12/0.24 por MUI, no `overlay.selected` (D1).

### Checkbox
Fuente: sin override en el tema (MUI Checkbox.js:55-96). `size="small"` en ~40 de 44 usos; medium en FormPublicPage.tsx:516,525,545.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (sin marcar) | transparente | `text.secondary` `#5a6a80` / `#a6b4c8` | — | — | ícono 20px small / 24px medium · padding 9px MUI (área 38/42px, radio 50%); la app lo baja a `p: 0.25` (24px), `0.5` (28px) o `0` |
| hover | halo `rgba(0,101,187,0.04)` L / `rgba(0,101,187,0.08)` D (MUI derivado; no lee `action.hover`, D21) | — | — | — | — |
| activo | ⚠ sin valor → MUI: ripple 0.3 `currentColor` (D3) | — | — | — | — |
| focus-visible | ⚠ sin valor → MUI: ripple pulsante; sin anillo estático (D2) | — | — | ⚠ sin valor | — |
| seleccionado (marcado) | — | `brand.default` `#0065BB` / `#0065BB` (D14) | — | — | `transition: fill 0.2s cubic-bezier(0.4,0,0.2,1)` (`motion.control`) |
| indeterminado | — | `brand.default` `#0065BB` | — | — | SelectAllCheckbox.tsx:111-117 |
| deshabilitado | — | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` (marcado o no) | — | — | — |
| error | ⚠ sin valor: no hay `color="error"` en ningún Checkbox | — | — | — | — |
| cargando | — | spinner `size 14` absoluto junto a la caja | — | — | SelectAllCheckbox.tsx:119-128 |

Notas:
- Variante densa de grilla: `disableRipple` + `'& .MuiSvgIcon-root': { transition: 'none' }` (ItemCheckbox.tsx:32-34; CheckboxCell.tsx:18-20; HideColumnsPanel.tsx:79-81).
- TablaEnLinea.tsx:118 usa reposo `#8a93a3` (fuera de `text.secondary`), `p: '2px'` (D9).
- Área táctil muy variable (9px vs 2/4px/0).

### Radio
Fuente: sin override en el tema (MUI Radio.js:56-90). `size="small"`; usos: ChartSettingsDialog.tsx:377,378; CodigosDialog.tsx:135,137; MonedaDialog.tsx:107,108,116; TokenNamePicker.tsx:52,57; LinkBoardsDialog.tsx:1048,1066,1166,1194; DuplicatesDialog.tsx:653.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `text.secondary` `#5a6a80` / `#a6b4c8` | — | — | — |
| hover | halo `rgba(0,101,187,0.04)` L / `rgba(0,101,187,0.08)` D (D21) | — | — | — | — |
| activo | ⚠ sin valor → MUI: ripple (D3) | — | — | — | — |
| focus-visible | ⚠ sin valor → MUI: ripple pulsante (D2) | — | — | ⚠ sin valor | — |
| seleccionado | — | `brand.default` `#0065BB` (D14) | — | — | punto interior `scale(0→1)` 0.15s (MUI, `shortest`) |
| deshabilitado | — | `overlay.disabled` ⚠ L → MUI: `rgba(0,0,0,0.26)` (D3) / D `rgba(255,255,255,0.28)` | — | — | — |
| error (`color="error"`, 1 uso: LinkBoardsDialog.tsx:1066) | halo `rgba(226,68,92,0.04)` / `rgba(239,68,68,0.08)` | `feedback.error.default` `#e2445c` / `#ef4444` | — | — | — |

### Switch
Fuente: sin override en el tema (MUI Switch.js:127-195). Mayoría `size="small"` (FormBuilder.tsx:1347,1880,2161,2367,3530; ShareModal.tsx:247,278,314; RulesPanel.tsx:235,303; AutomationList.tsx:274; AdminPage.tsx:461; TeamsAdminPanel.tsx:612); default en FormBuilder.tsx:1787,1792,1797.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (off) | pista `#000` opacidad 0.38 L / `#fff` opacidad 0.3 D (MUI) | thumb `#fff` L / `#e0e0e0` D (MUI grey 300) | — | thumb `shadow.e1` `0 1px 4px rgba(0,0,0,0.06)` L / `…0.4` D | small 40×24 (padding 7), thumb 16px; medium 58×38, thumb 20px · pista radio 7px · ⚠ sin valor en tema → MUI |
| hover (off) | halo `rgba(0,0,0,0.04)` L / `rgba(255,255,255,0.08)` D | — | — | — | — |
| activo | ⚠ sin valor → MUI: ripple (D3) | — | — | — | — |
| focus-visible | ⚠ sin valor → MUI: ripple pulsante (D2) | — | — | ⚠ sin valor | — |
| seleccionado (on) | pista `brand.default` `#0065BB` opacidad 0.5 | thumb `brand.default` `#0065BB` | — | — | NUEVO: `opacity.switchTrackOn` 0.5 · thumb `translateX` 16px small / 20px medium · hover halo `rgba(0,101,187,0.04)` L / `0.08` D (D21) |
| `color="success"` (AdminPage.tsx:461; TeamsAdminPanel.tsx:612) | pista `feedback.success.default` `#00c875` / `#22c55e` opacidad 0.5 | thumb igual | — | — | halo hover `rgba(0,200,117,0.04)` / `rgba(34,197,94,0.08)` |
| deshabilitado (off) | pista opacidad 0.12 L / 0.2 D | thumb `#f5f5f5` L / `#757575` D (MUI grey 100/600; D3) | — | — | — |
| deshabilitado (on) | pista `#0065BB` opacidad 0.12 L / 0.2 D | thumb `rgb(158,196,229)` L / `rgb(0,45,84)` D (derivados, D21) | — | — | — |
| error / cargando | ⚠ sin valor (no hay) | — | — | — | — |

Notas:
- `transition`: thumb `left, transform 0.15s cubic-bezier(0.4,0,0.2,1)`, pista `opacity, background-color 0.15s` (`motion.nav`).
- Los grises de MUI (grey 100/300/600/800) no son colores CTS (D9, D21).

### Swatch de color
Fuente: seis implementaciones independientes. Paleta de 8 valores `#0065BB #29ABE2 #00c875 #fdab3d #e2445c #a25ddc #ff642e #579bfc` repetida en `layout/sidebar/constants.ts:2`, `NewGroupDialog.tsx:14`, `GroupColorPicker.tsx:6`, `ui/ColorPicker.tsx:19-22`, `WorkspacesPage.tsx:25` = `swatch.group` (data8). Mismos valores en L y D salvo donde se indica.

| Variante | Estado | Fondo | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| A. Preset (`ui/ColorPicker.tsx:86,235-243`) | reposo | `swatch.group.*` (color `c`) | `2px solid transparent` | ninguna | 24/26/28px; radio 6/7/8 según tamaño (≥28: 8 = `radii.control`; ≥26: 7; resto: 6 = `radii.chip`) |
| | hover | — | — | — | `transform: scale(1.08)`, sin cambio de sombra |
| | seleccionado | — | `2px solid white` | `0 0 0 2px <c>` (anillo de su propio color) | el borde blanco no se ve sobre fondos claros |
| | focus-visible / activo / deshabilitado | ⚠ sin valor: es un `div` con `onClick`, no enfocable (D2) | — | — | `transition: transform 0.12s, box-shadow 0.12s` (`motion.micro`) |
| B. Guardado (`ui/ColorPicker.tsx:257-284`) | = A + badge de borrar | badge `#333` (no es neutro CTS), ícono blanco 10px | — | `0 1px 3px rgba(0,0,0,0.3)` | 14×14, `top/right -4`, `opacity` 0→1 `0.15s`; hover bg `feedback.error.default` |
| C. Disparador personalizado (`ui/ColorPicker.tsx:115-130`) | reposo | `conic-gradient(from 0deg, #ef4444, #f59e0b, #eab308, #22c55e, #06b6d4, #3b82f6, #8b5cf6, #ec4899, #ef4444)` | `2px solid white` | `0 0 0 2px rgba(0,0,0,0.15)` L / `rgba(255,255,255,0.2)` D | único swatch con anillo por tema; hover `scale(1.08)` |
| D. Sidebar (`layout/sidebar/ColorPicker.tsx:15-21`) | reposo | `c` | `2px solid transparent` | ninguna | 24×24, radio 6px (`radii.chip`), `transition: all 0.12s` |
| | hover | ⚠ sin valor (sin regla) | — | — | — |
| | seleccionado | — | `2px solid white` | `0 0 0 2px <c>` | — |
| E. Grilla (Boards/Workspaces: BoardsPage.tsx:323,341; WorkspacesPage.tsx:404-412) | reposo | `c` | — | — | 28×28, radio 8px (`radii.control`), `transition: transform 0.15s` (`motion.nav`) |
| | hover | — | — | — | `scale(1.15)` |
| | seleccionado | — | `outline: 3px solid <c>` (`borders.indicator`), `outlineOffset: 2` | — | — |
| F. Punto de opción de estado (`StatusCell.tsx:461-470`) | reposo | `swatch.status.*` | `2px solid background.paper` | `0 0 0 1px <c>` | 24×24, `borderRadius: 1` = 10px (D7), `transition: transform 0.1s`; hover `scale(1.1)`; el halo se adapta al modo oscuro |
| G. Mini punto (`editores.tsx:61-67`) | reposo / hover | sin color: `1.5px dashed` `text.disabled` | — | — | 14px, hover `scale(1.2)`, `transition: transform .1s` |
| H. Celdas de paleta (`editores.tsx:70-75`) | reposo | `c` | — | — | 22px, radio 5px, grilla `repeat(4, 22px)`, gap 0.75 |
| I. Tile de red (`ManagedColumnsPage.tsx:611-617`) | hover | — | — | `shadow.e2` | 36px, radio 1.5 = 15px (D7), `scale(1.08)` |
| J. Toggles de ícono KPI (`KpiEditorDialog.tsx:263-269`) | seleccionado | `tint(c,'18')` (`${color}18`, D11) | `1px solid <color>` | — | reposo: borde `border.subtle`, fondo transparente |

Notas:
- Escalas de hover sin unificar: 1.08 / 1.1 / 1.15 / 1.2; selección: borde blanco + anillo vs outline 3px vs halo `background.paper` (sin ID de decisión).
- Los swatches de estado (`swatch.status.*`) usan texto blanco: `#fdab3d`/`#00c875`/`#c4c4c4` no pasan AA y no hay variante oscura (D8).
- Ningún swatch es enfocable por teclado (D2).

### Link / miga de pan
Fuente: sin `MuiLink` ni `MuiBreadcrumbs` en el tema. Miga: `features/board-view/components/BoardBreadcrumb.tsx:13-45`; MUI Link.js:77-164.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | ninguno | `text.secondary` `#5a6a80` / `#a6b4c8` | — | — | 13px (`fontSize.dense`), peso 500, `underline="hover"` → `text-decoration: none`; `component="button"` |
| hover | ninguno | sin cambio de color | — | — | `text-decoration: underline` (NUEVO: `link.hoverDecoration` = underline) |
| activo | ⚠ sin valor | — | — | — | — |
| focus-visible | ninguno | — | `outline: auto` del navegador (MUI Link.js:164) [M] (D2) | ⚠ sin valor → no usa `focus.ring` | único con outline real |
| página actual | ninguno | `text.primary` `#1a2236` / `#e8edf4` | — | — | `Typography body2`, peso 700 |
| separador | — | ⚠ sin valor → MUI: `/` heredado `text.secondary` | — | — | margen `0 8px` |
| deshabilitado | ⚠ sin valor | — | — | — | — |

Otros patrones de link:

| Patrón | Reposo | Hover | Fuente |
|---|---|---|---|
| `<Link>` MUI por defecto (no se usa tal cual) | `brand.default` `#0065BB` siempre subrayado (D14: 2.01:1 en oscuro) | sin cambio; foco `outline: auto` | MUI |
| link de celda (`Typography component="a"`) | `brand.default` `#0065BB`, 12px (13px en vista compartida), sin subrayado | `underline` | LinkCell.tsx:54-60; EmailCell.tsx:57-61; PublicCell.tsx:471-473,503-506 |
| celda de teléfono | `text.primary` | sin regla | PhoneCell.tsx:62-66 |
| cuerpo Markdown | `brand.default`, peso 600, `border-bottom: 1px solid` `brand.default` | `border-bottom-width: 2px`, `mb: -1px`; `transition: all 0.15s` (`motion.nav`) | releases/components/MarkdownBody.tsx:99-105 |
| "Limpiar" | `feedback.error.default`, `Typography caption` | `underline` | TemplateCellEditor.tsx:414-418 |

Notas:
- Hover inconsistente: solo subrayado (migas) vs subrayado + color primary (celdas) vs borde 1px→2px (Markdown) (sin ID de decisión).
- Separación de la miga `mb: 1` (8px) en BoardBreadcrumb.tsx:12 (`layout.breadcrumbMarginBottom`) vs `mb 1.5` (BoardsPage.tsx:171) y `mb 2` (TemplateDetailPage.tsx:398).
- Color de link sin variante oscura (D14).

### DateCalendar
Fuente: `@mui/x-date-pickers` 8.27.2, solo `DateCalendar` inline en popovers (DateCell.tsx:129-137; TokenDateValueInput.tsx:114-121; TimelineCell.tsx:111-130). El tema **no** tiene `MuiPickersDay` ni `MuiDateCalendar`: personalización limitada a dos `sx` (hover y `Mui-selected`).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (día) | transparente | `text.primary` `#1a2236` / `#e8edf4` | — | — | 36×36, radio 50%, 12px/400 (MUI) |
| hover (con override) | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | — | — | — | DateCell.tsx:135; TokenDateValueInput.tsx:120 |
| hover (sin override, Timeline) | `rgba(0,101,187,0.04)` / `rgba(0,101,187,0.08)` (MUI, D21) | — | — | — | inconsistente con DateCell |
| focus | `rgba(0,101,187,0.12)` (MUI focusOpacity; D2) | — | — | — | — |
| seleccionado | `brand.default` `#0065BB` | `#fff`, peso 600 | — | — | + hover/focus `brand.hover` `#004696` (gana sobre el `action.hover` del override) |
| hoy (sin seleccionar) | transparente | — | `1px solid` `text.secondary` `#5a6a80` / `#a6b4c8` | — | ⚠ sin valor en cts-manager → MUI |
| deshabilitado | — | `text.disabled` ⚠ L → MUI: `rgba(0,0,0,0.38)` / D `rgba(255,255,255,0.5)` (D4); seleccionado+deshabilitado opacidad 0.6 | — | — | calendario completo `disabled` (Timeline, fin) |
| fuera del mes | — | `text.secondary` | — | — | `motion.collapse` `background-color 0.25s` |
| cabecera / flechas / días de semana | ⚠ sin valor → MUI default | — | — | — | no medido |

Notas:
- El override `Mui-selected` de DateCell.tsx:134 es redundante con MUI.

## Navegación y capas flotantes

Abreviaturas de ruta: `T` = `theme/ctsTheme.ts`; `SB` = `layout/Sidebar.tsx`; `BL` = `layout/sidebar/BoardList.tsx`; `PFS` = `layout/sidebar/PersonalFoldersSection.tsx`; `WS` = `layout/sidebar/WorkspaceSelector.tsx`; `VTB` = `features/board-view/components/ViewTabBar.tsx`. Valores del rail iguales en claro y oscuro salvo `bg.rail`. Valores marcados "MUI" no están definidos por el tema CTS: vienen de `@mui/material` 7.3.9 (el audit no los midió en navegador).
Accordion: no existe en la app (sin usos en `src`); se omite. Los grupos colapsables del rail son cabeceras propias + `Collapse`.

### NavItem del rail
Fuente: `layout/Sidebar.tsx:59-86` (NavLink + `ListItemButton`).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `text.onRailMuted` `rgba(255,255,255,0.65)` (D10); ícono hereda | izq. `borders.indicator` 3px transparente | — | `radii.control` 8px; `mx` 12px, `mb` 2px, `mt` 1px (tema); `px` 12px `py` 5.2px; `motion.nav` `all 0.15s`; ícono 18px, `minWidth` 32; etiqueta 13.5px / 600 (`fontWeight` semibold). Altura calculada ~40px vs `density.navItem` 34 (sin medir) ⚠ |
| hover | `onRail.hover` `rgba(255,255,255,0.1)` | `text.onRail` `#ffffff` | — | — | — |
| activo (pressed) | ⚠ sin valor → MUI: ripple `currentColor`, opacidad 0.3, 550ms (D3) | idem | — | — | no hay `:active` propio |
| focus-visible | ⚠ sin valor → MUI: `overlay.focus` `rgba(0,0,0,0.12)` / `rgba(74,144,226,0.12)` (D2, D3) | — | — | ⚠ sin anillo (`outline: 0`) (D2) | sobre el rail azul el gris neutro oscurece el azul; con la fila activa el `sx` activo gana y el foco sería invisible (sin verificar) |
| seleccionado (ruta actual) | `onRail.selected` `rgba(255,255,255,0.18)` | `text.onRail` `#ffffff` | izq. `onRail.indicator` `rgba(255,255,255,0.9)` 3px | — | la prop MUI `selected` no se usa; el estado es 100% `sx` |
| seleccionado + hover | `onRail.hover` `rgba(255,255,255,0.1)` | `text.onRail` | — | — | el hover pisa al activo: el ítem actual se apaga al pasar el cursor (D23) |
| deshabilitado | ⚠ sin valor → MUI: `opacity: 0.38`, `pointer-events: none` (D3) | | | | nunca se deshabilita |

Notas:
- Tres lenguajes de "activo" en el rail (NavItem 0.18 + borde 0.9; tablero 0.15 + 0.85; compartido azul) y escalera de alfas de reposo 0.3–0.78 / hover 0.06–0.15 (D10).
- Hermanos Tema (toggle) y Cerrar sesión: reposo `rgba(255,255,255,0.6)` (no 0.65), etiqueta 13px / 500 (peso 500 sin token, D22) (`layout/Sidebar.tsx:651-681`).
- `density.navItem` 34 vs ~40px calculado y token `navItem` sin verificar (D15).

### Ítem de tablero del rail (BoardList)
Fuente: `layout/sidebar/BoardList.tsx:82-144` (`BoardItemRow`); variante compartida `layout/sidebar/PersonalFoldersSection.tsx:67-117`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `text.onRailMuted` `rgba(255,255,255,0.65)` (D10); ícono 15px color de datos del tablero o `rgba(255,255,255,0.55)` | izq. 3px transparente | — | `radii.control` 8px; `mx` 12px `mb` 2px `py` 3.2px; `pl` 20px (32px en carpeta) `pr` 4px; `motion.micro` `all 0.12s`; etiqueta 12.5px / 500 |
| hover | `rgba(255,255,255,0.09)` (D10) | `rgba(255,255,255,0.9)` | — | — | botón "…" `opacity 0 → 1` |
| activo (pressed) | ⚠ sin valor → MUI: ripple 0.3 (D3) | | | | |
| focus-visible | ⚠ sin valor → MUI: `rgba(0,0,0,0.12)` / `rgba(74,144,226,0.12)` (D2, D3) | | | ⚠ sin anillo (D2) | el botón "…" (`opacity:0`) es tabulable e invisible al enfocarlo |
| seleccionado | `rgba(255,255,255,0.15)` (≠ `onRail.selected` 0.18, D10) | `text.onRail` `#ffffff`, peso 700 | izq. `rgba(255,255,255,0.85)` 3px (≠ `onRail.indicator` 0.9, D10) | — | |
| seleccionado + hover | `rgba(255,255,255,0.09)` pisa el 0.15 | | | | (D23) |
| arrastrando | — | — | — | — | origen `opacity 0.4` (+ transform dnd-kit); overlay `opacity 0.92`, fondo `rgba(20,40,70,0.95)` (D10); sin `cursor: grab` |
| deshabilitado | ⚠ sin valor → MUI: `opacity: 0.38` (D3) | | | | |

Variante tablero compartido (PFS): reposo `rgba(255,255,255,0.78)`, sin borde izq.; hover `rgba(255,255,255,0.06)`; seleccionado fondo `rgba(59,130,246,0.18)` + `outline 1px solid rgba(89,131,253,0.6)`, hover del activo `rgba(59,130,246,0.25)` (se intensifica, opuesto al propio, D23); arrastrando `0.4 × 0.5` (doble atenuación).

Notas:
- Azules de selección/drop (`59,130,246`, `89,131,253`) fuera de la paleta CTS (D9, D10).
- Alfa de hover 0.09 vs NavItem 0.1 (`BL:105` vs `SB:71`) (D10).

### Ítem de carpeta del rail
Fuente: `layout/sidebar/BoardList.tsx:182-238` (`DroppableFolderHeader`), `layout/sidebar/PersonalFoldersSection.tsx:136-207`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `rgba(255,255,255,0.7)` (D10); ícono `Folder/FolderOpen` 17px color de carpeta o `rgba(255,255,255,0.5)` | 1px transparente | — | `radii.control` 8px; `mx` 12px `px` 8px `py` 4px; nombre 13px / 700; chevron 18px (cerrada = `ExpandMore` rotado `-90deg`); `motion.micro` `all 0.12s` |
| hover | `rgba(255,255,255,0.08)` (D10) | `text.onRail` `#ffffff` | — | — | botón "…" `opacity 0 → 1` |
| activo (pressed) | ⚠ sin valor → MUI (sin ripple, no es `ButtonBase`) | | | | |
| focus-visible | — | — | — | ⚠ carpeta personal: anillo UA por `tabIndex` de dnd-kit; carpeta de workspace: no enfocable (D2) | |
| arrastrando (origen) | — | — | — | — | `opacity 0.5` (wrapper personal); overlay `width 220`, `opacity 0.9`, fondo `rgba(40,50,70,0.95)` (D10) |
| destino de drop | `rgba(59,130,246,0.25)` (hover `0.3`) | | 1px dashed `rgba(89,131,253,0.7)` | — | `DroppableRoot` usa otros azules (`rgba(74,144,226,0.12)` / dashed `0.45`) (D10) |

Notas:
- Cabecera de sección colapsable ("Compartidos conmigo" / "Espacios compartidos"): `rgba(255,255,255,0.6)`, 12px / 600 / `0.04em`, radio 7px (≠ 8), hover `rgba(255,255,255,0.08)`, no enfocable por teclado (⚠ D2) (`PFS:410-439`, `BL:666-684`).
- Chevron de sección cerrada apunta abajo; el de carpeta cerrada apunta a la derecha (`BL:218` vs `PFS:427`).

### Selector de espacio de trabajo (y sus botones "…" y "+")
Fuente: `layout/Sidebar.tsx:500-598`; avatar `layout/sidebar/WorkspaceAvatar.tsx:12-26`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (fila) | `rgba(255,255,255,0.1)` (≈ `onRail.hover`, D10) | nombre `text.onRail` 12.5px / 700; subtítulo `rgba(255,255,255,0.45)` 10px | 1px `rgba(255,255,255,0.18)` (D10) | — | `radii.base` 10px; alto 42px; `px` 8px `gap` 6px; `motion.nav` `all 0.15s`; avatar 26×26 radio 7px, borde 2px `rgba(255,255,255,0.28)`, sombra `0 2px 6px rgba(0,0,0,0.25)`; separador 1×20px `rgba(255,255,255,0.15)` |
| hover | sin hover propio en la fila; botón nombre `opacity 0.85` (sin transición) | | | | |
| activo (pressed) | ⚠ sin valor (botón nativo, sin ripple) | | | | |
| focus-visible | — | — | — | ⚠ anillo UA (`<button>` nativo sin reset) (D2) | |
| abierto | — | chevron `ExpandLess` (cerrado `ExpandMore` 16px `rgba(255,255,255,0.6)`) | | | |
| botón "…" reposo | transparente | `rgba(255,255,255,0.55)`, ícono 15px | — | — | 24×24, radio 6px |
| botón "…" hover | `rgba(255,255,255,0.12)` | `text.onRail` | | | |
| botón "+" reposo | `rgba(25,118,210,0.9)` (D20) | `#ffffff`, ícono 17px | — | — | 26×26, radio 7px; azul MUI por defecto, no CTS |
| botón "+" hover | `#1976d2` (D20) | | | | `transform: scale(1.05)`, `motion.nav` `all 0.15s` |
| botones "…" / "+": pressed y focus-visible | ⚠ sin valor → MUI IconButton: ripple 0.3 + `focusRipple` (D2) | | | | |

Notas:
- Avatar de workspace sustituye `#0065BB` por `#2979c4` (literal fuera de paleta) (`WorkspaceAvatar.tsx`) (D9).
- "+" con `rgba(25,118,210,0.9)` / `#1976d2` no debe portarse; debe ser `brand.default` / `brand.hover` (D20, D13).
- Selector vs buscador del rail: 0.1/0.18 frente a `onRail.searchBg` 0.08 / 0.15 (D10).

### Título de sección del rail
Fuente: `layout/Sidebar.tsx:487-493` ("Espacios de trabajo", no interactivo).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `text.onRailMuted` blanco con `opacity 0.45` (D10) | — | — | `px` 20px `pt` 16px `pb` 6px; 10px / 700 (`fontWeight` bold), `letterSpacing 0.1em`, mayúsculas |
| hover / activo / focus-visible / seleccionado / deshabilitado | n/a (no interactivo) | | | | |

Notas:
- El token `rail.sectionTitle` guarda alfa en el color; el código usa `opacity` del elemento (mismo resultado visual).

### Pie del rail / cerrar sesión
Fuente: `layout/Sidebar.tsx:688-722` (pie de usuario); `layout/Sidebar.tsx:651-681` (Tema y Cerrar sesión).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (pie) | `rgba(0,0,0,0.15)` | `text.onRail`; nombre 12.5px / 700; rol 10.5px `opacity 0.5` | arriba 1px `border.onRail` `rgba(255,255,255,0.1)` | — | `NavLink` a `/profile`; `padding` 12px 16px, `gap` 12px; `motion.nav` `background-color 0.15s`; avatar 32×32 fondo `rgba(255,255,255,0.2)`, borde 2px `rgba(255,255,255,0.35)` |
| hover (pie) | `rgba(0,0,0,0.25)` (D10) | | | | |
| seleccionado (pie) | ⚠ sin valor: no marca "actual" en `/profile` | | | | |
| focus-visible (pie) | — | — | — | ⚠ anillo UA (`<a>` nativo) (D2) | |
| reposo (Cerrar sesión) | transparente | `rgba(255,255,255,0.6)` (D10) | — | — | como NavItem: `mx` 12px, `px` 12px `py` 5.2px, radio 8px; sin `mb` (margen vertical 1px del tema); etiqueta 13px / 500 (D22); ícono 18px |
| hover (Cerrar sesión) | `rgba(255,100,100,0.2)` — NUEVO: `onRail.dangerHover` | `rgba(255,180,180,1)` — NUEVO: `onRail.dangerHoverText` | — | — | tinte rojo literal; no usa `feedback.error.*` |
| activo (pressed) / focus-visible / deshabilitado (Cerrar sesión) | ⚠ sin valor → MUI ListItemButton: ripple 0.3 / `overlay.focus` / `opacity: 0.38` (D2, D3) | | | | |

Notas:
- Hover rojo propio del rail frente a MenuItem destructivo sin tinte rojo (ver MenuItem).
- Divisores del rail: `border.onRail` `rgba(255,255,255,0.1)`, `my` 12px `mx` 16px; contenedor `bg.rail` `#0065BB` / `#253662`, `shadow.sidebar`, `motion.collapse` `width 0.25s` + fondo `0.3s` (sin token) (`layout/Sidebar.tsx:420-438`).

### ListItemButton genérico
Fuente: `theme/ctsTheme.ts:344-353` (override); resto MUI `ListItemButton.js`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `text.primary` `#1a2236` / `#e8edf4`; `ListItemIcon` ⚠ MUI: `rgba(0,0,0,0.54)` / `rgba(255,255,255,0.6)` (D3) | — | — | `radii.control` 8px; `margin` 1px 8px; `padding` 7px 12px (MUI 8px 16px); `motion.nav` `all 0.15s`; `ListItemText` MUI `margin 4px 0`, `body1` |
| hover | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | | | | |
| activo (pressed) | ⚠ sin valor → MUI: ripple `currentColor` 0.3, 550ms (D3) | | | | |
| focus-visible | ⚠ sin valor → MUI: `overlay.focus` `rgba(0,0,0,0.12)` / `rgba(74,144,226,0.12)` (D2, D3) | | | ⚠ sin anillo (D2) | claro: gris neutro fuera de la familia azul |
| seleccionado | `overlay.selected` ⚠ MUI: `rgba(0,101,187,0.08)` / `rgba(0,101,187,0.16)` (D1) | | | | el tema define `action.selected` `rgba(0,101,187,0.1)` / `rgba(74,144,226,0.16)` pero este estado no lo lee (D1) |
| seleccionado + hover / + focus | ⚠ MUI: `rgba(0,101,187,0.12)` / `0.24`; focus `0.2` / `0.28` (D1) | | | | |
| deshabilitado | ⚠ sin valor → MUI: `opacity: 0.38`, `pointer-events: none` (D3) | | | | |

Notas:
- Dos mecanismos de "seleccionado" conviven: prop `selected` (`VTB:639`) y `bgcolor: 'action.selected'` explícito (`WS:43`) (D1).
- Ejemplo vivo en `VTB:637-642`: `px` 12px `py` 4.8px, texto 13px, seleccionado `brand.default` / `text.primary`.

### Tab (MUI Tabs)
Fuente: sin override de tema (no hay `MuiTab`/`MuiTabs`); usos `features/admin/AdminPage.tsx:347-350`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `text.secondary` `#5a6a80` / `#a6b4c8` (MUI) | — | — | `typography.button` (600) + MUI `0.875rem`, mayúsculas; cada uso pisa `textTransform: 'none'`; `padding` 12px 16px, `minHeight` 48 (compacto 36 en `ImportTemplateDialog` / `TokenOptionList`) |
| hover | ⚠ sin valor (MUI Tab no define `:hover`) | | | | la pestaña MUI no reacciona al hover |
| activo (pressed) | ⚠ sin valor → MUI: ripple 0.3 (D3) | | | | |
| focus-visible | ⚠ sin valor (`outline: 0`, sin `focusRipple`) (D2) | | | ⚠ foco invisible (D2) | |
| seleccionado | transparente | `brand.default` `#0065BB` | indicador `borders.accent` 2px `brand.default` | — | `transition all 300ms cubic-bezier(0.4,0,0.2,1)` (MUI) |
| deshabilitado | ⚠ sin valor → `text.disabled` MUI `rgba(0,0,0,0.38)` / `rgba(255,255,255,0.5)` (D4) | | | | |

Notas:
- Contenedor: `borderBottom` 1px `border.subtle` (`#dde3ec` / `rgba(74,144,226,0.12)`).
- Badge de conteo en `TokenOptionList`: `overlay.selected` explícito, 11px / 700 (peso 700, D22).
- Tres tipos de "tab" (MUI, ViewTabBar, cabecera de Activity `borderBottom 2px solid primary.main`).

### Tab de vista (ViewTabBar)
Fuente: `features/board-view/components/ViewTabBar.tsx:63-141`, `NombreDeLaPestana.tsx:17-26`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `text.secondary` `#5a6a80` / `#a6b4c8`, 13px / 500 (D22); íconos 12–14px `text.disabled` (D4) | abajo 2px transparente (`mb -2px`) | — | `px` 12px `py` 6px `gap` 2px; `cursor: pointer`; botón "⋮" `opacity 0`, `transition opacity 0.15s` (≠ `motion.micro` 0.12s) |
| hover | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | | | | radio `4px 4px 0 0` (sin token; `radii.chip` 6 no coincide); "⋮" `opacity 1` |
| activo (pressed) | ⚠ sin valor (sin ripple) | | | | |
| focus-visible | — | — | — | ⚠ anillo UA (`role=button tabIndex=0` de dnd-kit) (D2) | |
| seleccionado | transparente (con hover `overlay.hover`) | `brand.default` `#0065BB`, 13px / 700; íconos `brand.default` | abajo `border.brand` 2px `#0065BB` | — | "⋮" `opacity 0.6` color `brand.default` |
| arrastrando | — | — | — | — | `opacity 0.5`, `z-index 2`, `cursor: grabbing` |
| deshabilitado | n/a (sin cambio visual si no es reordenable) | | | | |

Notas:
- Único tipo de tab con hover; pestaña "Vista principal" igual pero sin dnd (`flexShrink 0`).
- Franja `borderBottom` 2px `border.subtle`; el borde de 2px de la pestaña la tapa.
- Controles auxiliares (flechas, "+", "⌄", chip "N ocultas") usan IconButton / Chip MUI sin estados propios.

### Menu (papel)
Fuente: `theme/ctsTheme.ts:375-387`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| abierto | `bg.raised` `#ffffff` / `#253662` | `text.primary` | 1px `border.subtle` `#dde3ec` / `rgba(74,144,226,0.1)` (≠ divider 0.12, D9) | `shadow.menu` `0 8px 24px rgba(0,101,187,0.15)` / `0 8px 24px rgba(0,0,0,0.5)` | `radii.base` 10px; `MenuList` `padding 8px 0` y `Grow auto` (MUI) |
| override en llamadas | | | | menú "+" `0 8px 32px rgba(0,0,0,0.15)`, menú "⋯" y selector `0 8px 32px rgba(0,0,0,0.18)` | pierden el tinte azul y quedan más ligeras en oscuro (`layout/Sidebar.tsx:745,840`) (D15) |

Notas:
- Divisores internos `my 4px` vs regla MUI `.MuiMenuItem-root + .MuiDivider-root { margin 8px 0 }`: probablemente gana 8px (sin verificar).
- Anchos mínimos por llamada 180/200px.

### MenuItem (incl. destructivo)
Fuente: `theme/ctsTheme.ts:388-398`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | transparente | `text.primary` `#1a2236` / `#e8edf4` | — | — | `radii.chip` 6px; `margin` 2px 6px; `padding` 7px 10px; `fontSize` 0.875rem (llamadas fuerzan 13px); `motion.nav` `background 0.15s`; `minHeight` MUI 48 en xs |
| hover | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | | | | |
| activo (pressed) | ⚠ sin valor → MUI: ripple 0.3 (D3) | | | | |
| focus-visible | ⚠ sin valor → MUI: `overlay.focus` `rgba(0,0,0,0.12)` / `rgba(74,144,226,0.12)` (D2, D3) | | | ⚠ sin anillo (D2) | el primer ítem se enfoca al abrir con teclado |
| seleccionado | `overlay.selected` ⚠ MUI: `rgba(0,101,187,0.08)` / `rgba(0,101,187,0.16)` (D1) | | | | + hover MUI `0.12` / `0.24`; + focus `0.2` / `0.28` |
| deshabilitado | ⚠ sin valor → MUI: `opacity: 0.38` (D3) | | | | |
| destructivo | hover `overlay.hover` azul (⚠ sin tinte rojo) | `feedback.error.default` `#e2445c` / `#ef4444` (texto e ícono) | — | — | `layout/Sidebar.tsx:955-958`, `VTB:725`; precedido de `Divider` |

Notas:
- Padding de llamadas distinto del tema: `py 10px px 16px` (menú "+"), `py 8px px 16px` (menú "⋯"), `py 6.8px px 12px` (selector) (D15).
- El rail sí tiñe de rojo el hover de Cerrar sesión; el MenuItem destructivo no.

### Tooltip
Fuente: `theme/ctsTheme.ts:296-322` (variante de tema).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| abierto | `bg.inverse` `#1a2236` / `#1e2d42` (flecha igual) | `text.onInverse` ⚠ MUI: `#ffffff` | — (sin borde) | sin sombra | `radii.chip` 6px; `padding` 5px 10px; 12px / 500 (D22); `arrow: true`; `strategy: fixed`; `maxWidth` 300; `enterDelay` 100, `Grow`, `zIndex` 1500 (MUI) |
| focus-visible | abre al enfocar el hijo (MUI) | | | | |
| reposo / hover / activo / deshabilitado | n/a | | | | |

Notas:
- Hay 4 estilos de tooltip (D19); el oscuro `#1e2d42` no está en `colors.ts`.
- Variante tarjeta (`board-view/components/LazyTooltip.tsx:15-58`): fondo `bg.raised` `#ffffff` / `#1e293b`, texto `#1e293b` / `#f1f5f9`, borde 1px `#e2e8f0` / `rgba(255,255,255,0.10)`, sombra `0 8px 28px rgba(15,23,42,0.18)` / `0.45`, radio 15px (D7), 12.5px / 500, retardo 900ms (D19, D9).
- Variante `ItemRow.tsx:401-418`: `bg.raised`, `border.subtle`, `boxShadow: 6` = `shadow.e6` `0 16px 40px rgba(0,0,0,0.16)` / `0.65`, 12.5px (D19, D16).

### Tooltip enriquecido
Fuente: `features/shared-view/SharedViewPage.tsx:38-71` (única aparición, D19).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| abierto | `bg.raised` `#ffffff` / `#1a2333` (D12) | `#1a2333` / `#e4e9f1` (sin rol) | 1px `#e0e7ef` / `#324158`; izq. `borders.indicator` 3px `brand.default` `#0065BB` / `#89AEDC` (D14) | `shadow.tooltipRich` `0 6px 20px rgba(0,101,187,0.12)` / ⚠ sin valor en token oscuro; código `0 6px 20px rgba(0,0,0,0.45)` | radio 15px (D7); `px` 14px `py` 10px; `maxWidth` 420; 13px / 400, `lineHeight 1.55`, `letterSpacing 0.01em`; flecha = fondo con borde |
| hover / activo / focus-visible / deshabilitado | n/a | | | | |

Notas:
- Tercer azul-negro oscuro (`#1a2333`) además de `#1e2d42` y `#1e293b` (D12, D19).

### Popover de selector (papel, fila de búsqueda, opción)
Fuente: base `Popover` MUI elevation 8; `features/board-view/components/cells/StatusCell.tsx:261-398`; `layout/sidebar/WorkspaceSelector.tsx:93-210`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| abierto (papel) | `bg.raised` `#ffffff` / `#253662` | | sin borde | `shadow.e6` `0 16px 40px rgba(0,0,0,0.16)` / `0.65` (elevation 8 heredada, D16); selector de workspace: `0 8px 32px rgba(0,0,0,0.18)` | base `radii.card` 12px; pickers de estado y dropdown: `borderRadius: 2` = 20px (D7); selector `10px`; anchos 280 / 260 / 280; transición `Grow auto` |
| fila de búsqueda | transparente | ícono 16px `text.disabled` (estado) / `text.secondary` (selector, dropdown); `InputBase` 13px | abajo 1px `border.subtle` | — | `px` 12px `py` 8px |
| opción (estado) reposo | color de datos `swatch.status.*` | `#ffffff` (sin rol; ≈ `text.onBrand`), 13px / 600 | — | — | radio 15px (D7); `px` 12px `py` 6.8px; `filter 0.15s`, `transform 0.1s` |
| opción hover | `filter: brightness(0.88)` (no usa `overlay.hover`) | | | | |
| opción activo (pressed) | ⚠ sin valor (`transform` en transición pero sin `:active`) | | | | |
| opción focus-visible | — | — | — | ⚠ sin valor: `Box` sin `tabIndex`, no enfocable (D2) | |
| opción seleccionada (estado) | | | | doble anillo: `outline 2px` color `bg.raised` + `0 0 0 2px {color}` | |
| fila de workspace reposo / hover | transparente / `overlay.hover` | `text.primary` 13px / 400; Check 14px `brand.default` | — | — | `py` 6.8px `px` 12px `gap` 10px |
| fila de workspace seleccionada | `overlay.selected` `rgba(0,101,187,0.1)` / `rgba(74,144,226,0.16)` (explícito, ≠ prop MUI, D1) | peso 600 | | | el `sx hover` aclara la fila seleccionada (queda más claro que selected) |
| fila deshabilitada (edición de etiqueta) | | | | | `opacity 0.45` + `line-through` (≠ 0.38, D3) |

Notas:
- Pickers de estado vs dropdown: lista `maxHeight 320 / p 8px` vs `200 / 4px`; `mt 4px` solo en estado; `PaperProps` obsoleto en `DropdownCell.tsx:187`.
- `slotProps.paper` con radios 20px frente a 12px de base (D7).

### Dialog (papel, título, contenido, acciones, fondo)
Fuente: `theme/ctsTheme.ts:278-293`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| abierto (papel) | `bg.raised` `#ffffff` / `#253662` | `text.primary` | — | `shadow.dialog` `0 24px 64px rgba(0,101,187,0.18)` / `0 24px 64px rgba(0,0,0,0.7)` | `radii.dialog` 14px; `margin` 32 y `maxHeight calc(100% - 64px)` (MUI) |
| título | | 16px / 700, `padding-bottom` 8px (sobre `padding` MUI 16px 24px) | | | sin token de peso 700 en MUI `h6` (CTS 600) (D22) |
| contenido | | | | | ⚠ sin valor → MUI: `padding 20px 24px` |
| acciones | | | | | ⚠ sin valor → MUI: `padding 8px`, `gap` 8px, `flex-end`; la mayoría de llamadas lo pisan (`px 24px pb 16–20px`) |
| fondo (backdrop) | `overlay.scrim` ⚠ MUI: `rgba(0, 0, 0, 0.5)` (ambos modos) | | | | `Fade` 225ms / 195ms; `zIndex` 1300 (MUI) |
| focus-visible | foco atrapado; `outline: 0` en el contenedor (MUI) | | | | |

Notas:
- Radio 14px de tema vs `GlobalConfirmDialog` 30px (`ui/GlobalConfirmDialog.tsx:35`) y StatusCell 12px (D7).
- Títulos 16px (tema) / 15px (Delete/Edit) / 17px (GlobalConfirm) y acciones `px 24px pb 16px` / `pb 20px` (D15).
- Sombra del diálogo `0.18` vs tarjeta del tour `0.22` (D15).

### ConfirmDialog destructivo
Fuente: `ui/ConfirmDialog.tsx:18-31`; variantes `ui/GlobalConfirmDialog.tsx`, `layout/sidebar/DeleteDialog.tsx`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (diálogo) | `bg.raised` (papel del Dialog) | cuerpo `text.secondary` `#5a6a80` / `#a6b4c8`, `body2` | — | `shadow.dialog` | `maxWidth xs`, `fullWidth`, sin overrides; acciones sin `sx` (padding 8px) |
| reposo (confirmar) | `feedback.error.default` `#e2445c` / `#ef4444` | `feedback.error.onColor` ⚠ sin valor en cts-manager (MUI `error.contrastText`, D21) | — | — | `variant contained`, `color error`, etiqueta "Eliminar" |
| reposo (cancelar) | transparente | `brand.default` (texto, color `primary` por defecto) | — | — | otras variantes usan `color inherit` u `outlined` (D15) |
| hover (confirmar) | ⚠ sin valor → MUI: `error.dark` derivado de `main` (D21) | | | ⚠ MUI: `shadows[4]` (D6) | el tema solo define hover para `containedPrimary/Secondary` (`T:130-145`) |
| activo (pressed) | ⚠ sin valor → MUI: ripple (D3) | | | | |
| focus-visible | ⚠ sin valor → MUI: contained recibe `shadows[6+]` = `0 16px 40px …` (D6); cancelar sin indicador (D2) | | | | |
| deshabilitado (confirmar) | ⚠ MUI: `overlay.disabledBg` `rgba(0,0,0,0.12)` / `rgba(255,255,255,0.08)` | ⚠ MUI: `overlay.disabled` `rgba(0,0,0,0.26)` / `rgba(255,255,255,0.28)` (D3) | | | en `GlobalConfirmDialog` hasta que el texto coincida (modo `input`) |

Notas:
- Variante más usada, `GlobalConfirmDialog`: radio 30px (`radii.dialogFeature`), título 17px / 700, cuerpo 14px, acciones `px 24px pb 20px`, botones `textTransform: none`, `fontWeight 600` (D7, D15, D22).
- `DeleteDialog`: título 15px / 700, cuerpo `text.primary` 14px (≠ `text.secondary`), acciones `px 24px pb 16px`.
- Desbloqueo de StatusCell usa `#fdab3d` / hover `#e69b2e` hardcoded (D9, D21).

### Drawer
Fuente: `theme/ctsTheme.ts:205-211` (solo oscuro); temporal en `features/board-view/components/TrashPanel.tsx:207`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| abierto (temporal) | `bg.raised` ⚠ claro MUI `#ffffff` / oscuro `#253662` (override redundante) | `text.primary` | — | `shadow.e6` `0 16px 40px rgba(0,0,0,0.16)` / `0.65` (elevation 16 heredada, D16) | radio 0 (`square`); `Slide` 225ms / 195ms; `zIndex` 1200 (MUI) |
| fondo (backdrop) | `overlay.scrim` ⚠ MUI: `rgba(0,0,0,0.5)` | | | | |
| cabecera | | título `h6` (600); chip contador 11px / 700 | abajo 1px `border.subtle` | — | `px` 20px `py` 16px (SharedViews / ItemComments `p` 20px); Activity sin borde |
| rail (permanente) | `bg.rail` `#0065BB` / `#253662` | `text.onRail` | ninguno | `shadow.sidebar` `4px 0 20px rgba(0,0,0,0.2)` | ancho 256px (colapsado 0); `motion.collapse` 0.25s |

Notas:
- Anchos 440 / 460 / 720px (`xs: 100%`) vs `layout.panelMin/Max` 300/360 (D15).
- Título 1.25rem / 1rem / 1.35rem según panel; scrollbar global se pinta sobre el rail azul (track `#f0f4f9`) (D18).

### Miga de pan (ítem)
Fuente: `features/board-view/components/BoardBreadcrumb.tsx:12-45`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (enlace) | transparente | `text.secondary` `#5a6a80` / `#a6b4c8` | — | — | `Link component="button"` `body2` (13px), 500 (D22); `mb` 8px; separador "/" margen 0 8px (MUI) |
| hover | transparente | color sin cambio | — | — | `text-decoration: underline` |
| activo (pressed) | ⚠ sin valor (no es `ButtonBase`) | | | | |
| focus-visible | — | — | — | ⚠ sin valor → MUI: `outline: auto` UA en lugar de `focus.ring` (D2) | único elemento de navegación con anillo nativo |
| actual (último) | transparente | `text.primary` `#1a2236` / `#e8edf4`, 700 (D22) | — | — | `Typography body2`, no interactivo |
| deshabilitado | n/a | | | | |

Notas:
- El color no cambia al hover; solo aparece el subrayado.

## Datos y retroalimentación

Rutas relativas a `cts-manager/frontend/src`; `T` = `theme/ctsTheme.ts`. "MUI" = valor calculado por MUI 7.3.9 con la paleta CTS (no lo fija la app). El `borderRadius` numérico en `sx` se multiplica por 10 (`1.5` = 15px, `2` = 20px, `2.5` = 25px, `3` = 30px): ninguno está en `radii` (D7).

### Chip — por defecto
Fuente: `T:326-332` + defaults MUI; ~151 usos con `sx` local.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `overlay.selected` `rgba(0,101,187,0.1)` / `rgba(74,144,226,0.16)` (D1) | `text.primary` `#1a2236` / `#e8edf4` | — | — | h `density.chip` 24px · `radii.chip` 6px · 12px/600 (`fontSize.caption`, `fontWeight.semibold`) · label px 8px · transición MUI `300ms cubic-bezier(0.4,0,0.2,1)` (≠ `motion.nav`) |
| hover (clickable) | ⚠ sin valor → MUI: `rgba(0,101,187,0.12)` / `rgba(74,144,226,0.24)` (D1) | = | — | — | cursor pointer; sin `onClick` no cambia |
| activo (pressed) | = | = | — | `shadow.e1` `0 1px 4px rgba(0,0,0,0.06)` / `0 1px 4px rgba(0,0,0,0.4)` (D16) | solo clickable |
| focus-visible | ⚠ sin valor → MUI: `rgba(0,101,187,0.2)` / `rgba(74,144,226,0.28)` (D1, D3) | = | — | ⚠ sin valor → MUI: `outline: 0`, sin anillo (D2) | |
| seleccionado | sin estado nativo; se simula con `variant` filled/outlined + `color primary` | `brand.default` `#0065BB` | | | `features/board-view/components/cells/ConnectCell.tsx:137-142` (D1) |
| deshabilitado | = | ⚠ sin valor → MUI: opacity 0.38 (D4) | — | — | `pointer-events: none`; único uso `ManagedColumnsPage.tsx:752` |
| error | sin variante propia; se usa `color="error"` (fila siguiente) | | | | |
| reposo `color=*` (filled) | `feedback.{success,warning,error,info}.default` `#00c875 #fdab3d #e2445c #29ABE2` / `#22c55e #f59e0b #ef4444 #06b6d4`; primary `brand.default` `#0065BB` | `feedback.*.onColor` ⚠ sin valor → MUI: `#fff` (primary, error), `rgba(0,0,0,0.87)` (warning, success, info) (D21) | — | — | ver forzado a blanco en Chip contador (D8) |
| hover/focus `color=*` | `feedback.*.hover` ⚠ sin valor → MUI `palette.dark`: primary `#004696`, warning `#B1772A`/`#AB6E07`, error `#9E2F40`/`#A72F2F`, success `#008C51`/`#178941`, info `#1C779E`/`#047F94` (D13, D21) | = | — | — | deleteIcon: `alpha(contrastText,0.7)`, hover `contrastText` |

Notas:
- El tamaño real casi nunca es el del tema: alturas 14/16/17/18/20/22/26/28 y fuentes 7–12px por sitio (solo `density.chip/chipCount/chipBadge` tokenizadas).
- Radios locales `'4px'` (`features/releases/ReleaseEntry.tsx:127,138,149`) y `'3px'` (`features/shared-view/SharedViewPage.tsx:186,298`); `ReleaseEntry.tsx:149` usa `#ff5252` fuera de toda paleta (D9). `features/admin/DuplicatesDialog.tsx:492` usa `success.50`/`warning.50` inexistentes (D20).
- Transición MUI 300ms contradice `motion.nav` .15s / `motion.control` .2s (D15).

### Chip — contador
Fuente: `features/board-view/components/toolbar/ViewToolbar.tsx:135-175`, `TrashPanel.tsx:218`, `AdminPage.tsx:326`, `ItemCommentsDrawer.tsx:188`, `GlobalHistoryPage.tsx:177`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (genérico) | `overlay.selected` `rgba(0,101,187,0.1)` / `rgba(74,144,226,0.16)` (D1) | `text.primary` | — | — | h `density.chipCount` 20px · 11px/700 (`TrashPanel.tsx:218`, `SharedViewsPanel.tsx:90`) o 10px/700 (`AdminPage.tsx:326`, `TemplatesPage.tsx:148`) |
| reposo (badge 18) | = | = | — | — | h `density.chipBadge` 18px · 10px/700 (`ItemCommentsDrawer.tsx:188`) |
| reposo (toolbar, primario) | `brand.default` `#0065BB` | `text.onBrand` `#ffffff` | — | — | h18 · 10px (Persona, Filtrar, Ordenar, Agrupar) |
| reposo (toolbar, Ocultar) | `feedback.warning.default` `#fdab3d` / `#f59e0b` | `#ffffff` (blanco sobre `#fdab3d` = 1.90) (D8) | — | — | MUI daría `rgba(0,0,0,0.87)` |
| reposo (grupo, tintado) | `tint(c,'20')` (`TemplateItemsTable.tsx:216`) o `tint(c,'18')` + opacity 0.7 (`SharedViewPage.tsx:142-151`) (D11) | color del grupo | — | — | h20 · 11px/700; hover del encabezado → opacity 1, `transition opacity 0.15s` (`motion.nav`) |
| reposo (etiqueta Tuyo/Compartido) | propio `brand.default` / compartido `overlay.selected` | `#ffffff` / `text.secondary` | — | — | h16 · 9px/700 · letter-spacing `0.04em` (`NewColumnDialog.tsx:481`) |
| hover / activo / focus-visible / deshabilitado | no interactivo | | | | sin valor en cts-manager |

Notas:
- h20 mezcla 11px y 10px; h22 con 11.5px (`NewGroupDialog.tsx:139`); h16/h18/h22 sin token (D15).
- Blanco forzado sobre `warning`/`success`/`info` contradice el default MUI (D8, D21).

### Chip — tintado (grupo / rol)
Fuente: `TemplatePreviewDialog.tsx:222,250`, `TemplatesPage.tsx:294`, `BoardsPage.tsx:157,219`, `ItemCommentsDrawer.tsx:225`, `MembersDialog.tsx:230`, `features/board-view/components/cells/MirrorCell.tsx:38`, `AdminPage.tsx:426-446`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (grupo) | `tint(c,'20')` ≈12.5% | color de dato `swatch.group.*` | — | — | h20 · 11px/700 · sin variante dark (D11) |
| reposo (grupo/rol) | `tint(c,'18')` ≈9.4% | = | — | — | h20/22 · 10–11px · `ItemCommentsDrawer.tsx:225`, `MembersDialog.tsx:230` |
| reposo (con borde) | `${c}15` | = | `${c}40` 1px | — | h22 · 11px · único chip con borde tintado (D11) |
| reposo (celdas espejo) | `tint(hex,'26')` ≈15% (no existe en `tint()`) | `#9d50dd`, `#579bfc`, `#00a05f`, `#0065BB` | — | — | h20 · 10px/600; `#9d50dd` ≠ `swatch.group` morado `#a25ddc` (D9, D11) |
| reposo (rol, AdminPage) | `alpha(c,0.12)` / `alpha(c,0.18)` | `c`: ADMIN `#fdab3d`, MEMBER `#0065BB`, VIEWER `#787d80`, GUEST `#a25ddc` | none | — | h20 · 10px · 700 ADMIN / 600 resto |
| reposo (rol, MembersDialog) | `${c}18` (sin ajuste dark) | `#0065BB`, `#22c55e`, `#f59e0b` (tonos dark usados en light) | — | — | `MembersDialog.tsx:24-26` (D9) |
| reposo (rol en tarjeta) | `rgba(255,255,255,0.25)` | `#ffffff` | — | — | `WorkspacesPage.tsx:264,336` · h20 · 10px/600 |
| hover / activo / focus / deshabilitado | ⚠ sin valor → MUI: igual al chip por defecto (no clickable) (D2) | | | | |

Notas:
- Siete recetas de alfa para el mismo concepto (`20/18/15/26/30/33` + `alpha` por modo); `tint()` solo soporta `'20'|'18'` (D11).
- `RulesPanel.tsx:222` usa `grey.300` y `#fff` sobre color de estado (D8).

### Chip — outlined
Fuente: defaults MUI; usos `SharedViewsPanel.tsx:179`, `TrashPanel.tsx:349-355`, `LinkBoardsDialog.tsx:810,821`, `ChartSettingsDialog.tsx:213`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (default) | transparent | `text.primary` `#1a2236` / `#e8edf4` | ⚠ sin valor → MUI: `1px solid #bdbdbd` / `#616161` (no es `border.subtle`) (D9, D21) | — | `TablaCell.tsx:72` lo sobrescribe con `divider` |
| reposo (`color=*`) | transparent | `feedback.*.default` | ⚠ sin valor → MUI: `1px solid alpha(main,0.7)` (D11, D21) | — | usado con info/warning/error/success/primary |
| hover (default) | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | = | = | — | clickable |
| hover (`color=*`) | `alpha(main,0.04)` / `alpha(main,0.08)` | = | = | — | MUI |
| activo | ⚠ sin valor → MUI: igual que filled (`shadow.e1`) (D16) | | | | |
| focus-visible | default: `overlay.focus` ⚠ sin valor → MUI: `rgba(0,0,0,0.12)` (light, gris neutro) / `rgba(74,144,226,0.12)` (D3); `color=*`: `alpha(main,0.12)` | = | = | ⚠ sin valor → MUI: sin anillo (D2) | |
| deshabilitado | ⚠ sin valor → MUI: opacity 0.38 (D4) | | | | |
| "eliminado" (dashed) | transparent | `text.disabled` ⚠ MUI `rgba(0,0,0,0.38)` / `rgba(255,255,255,0.5)` (D4) | `border.subtle` `1px dashed #dde3ec` / `rgba(74,144,226,0.12)` | — | `features/historial/piezas.tsx:680,694` |

Notas:
- Borde outlined por defecto es gris MUI, no el divisor azulado del tema (D9).
- `overlay.focus` light no está definido en el tema (D3).

### Chip — de celda
Fuente: `LabelCell.tsx:49-52,91`, `DropdownCell.tsx:160-176`, `FileCell.tsx:128-143`, `ConnectCell.tsx:112-142,196` (en `features/board-view/components/cells/`).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (Label/Dropdown) | `overlay.selected` (sin color por opción) | `text.primary` | — | — | h 22px (sin token) · 11px/600 · maxWidth 100% |
| reposo (opción de menú) | = | = | — | — | h `density.chipCount` 20px · 11px/600 · `pointer-events: none` |
| reposo ("+N", Dropdown/File) | `brand.subtle` `rgba(0,101,187,0.09)` / `rgba(41,171,226,0.15)` (D11) | `text.brand` `#0065BB` | — | — | h22 · 10.5px/700 |
| reposo (Connect) | `brand.subtle` `rgba(0,101,187,0.08)` / `rgba(41,171,226,0.15)` (0.08 vs 0.09: D11) | `text.brand` | — | — | h22 · 11px/500 (D22) · ícono 13px |
| reposo (File) | `overlay.selected` | `text.primary` | — | — | h22 · 10px · maxWidth 120 · cursor pointer · deleteIcon 12px |
| hover (celda) | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | = | — | — | el hover es de la CELDA, no del chip; solo lectura: sin hover |
| hover ("+N" File) | `rgba(0,101,187,0.18)` / `rgba(41,171,226,0.28)` | = | — | — | `FileCell.tsx:143` |
| activo | ⚠ sin valor → MUI: sin estilo propio (D2) | | | | |
| focus-visible | ⚠ sin valor → MUI: sin anillo en celdas (D2) | | | | |
| seleccionado | `brand.default` `#0065BB` (filled+primary) / outlined+default si no | `text.onBrand` | | | solo `ConnectCell.tsx:137-142` (D1) |
| deshabilitado / solo lectura | = | = | — | — | cursor default; el wrapper `CellRenderer.tsx:292-295` aplica opacity 0.7 + candado 12px |
| deleteIcon | — | `text.disabled` → hover `feedback.error.default` `#e2445c` / `#ef4444` (D4) | — | — | por defecto MUI `alpha(text.primary,0.26)` / hover `0.4`; 16px |

Notas:
- Primary tint 0.08 / 0.09 / 0.07 / 0.1 según archivo; dark alterna `74,144,226`, `41,171,226` y `0,101,187` (D11).
- Altura 22px es la más común y no tiene token.

### StatusPill (celda de estado)
Fuente: `features/board-view/components/cells/StatusCell.tsx:25-31,76-85,211-255`, espejo `features/shared-view/PublicCell.tsx:345-383`. No es una píldora: rellena toda la celda (h 100%, sin radio).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `swatch.status.*` color de dato: `#0065BB #29ABE2 #00c875 #fdab3d #e2445c #a25ddc #ff642e #579bfc`; sin color `#c4c4c4`; sin variante dark | `swatch.status.onColor` `#ffffff` (blanco falla AA: `#fdab3d` 1.90, `#c4c4c4` 1.74, `#00c875` 2.21) (D8) | — | — | 11px/600 · radio none · cursor pointer · `filter 0.15s` (`motion.nav`) |
| reposo (reservados) | `#00c875` "Aprobado por cliente" / `#e2445c` "Rechazado por cliente" | `#ffffff` | — | — | hard-coded en 2 archivos; en dark no usa `#22c55e`/`#ef4444` (D8, D9) |
| vacío | transparent | `text.secondary` `#5a6a80` / `#a6b4c8` | — | — | valor `''` no pinta nada |
| hover (con valor) | = | = | — | — | `filter: brightness(0.88)` (`FormPublicPage.tsx:352` usa 0.9) |
| hover (vacío) | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | = | — | — | |
| activo | ⚠ sin valor → MUI: sin estilo (es un `Box`) (D2) | | | | |
| focus-visible | ⚠ sin valor → MUI: no enfocable, sin anillo (D2) | | | | |
| seleccionado | n/a (el valor es la selección) | | | | |
| deshabilitado / bloqueado | = (se mantiene) | candado 12px `LockOutlined` | — | — | cursor `not-allowed`; owner: candado clickable, hover `rgba(255,255,255,0.25)`; sin cambio visual en hover |
| error / cargando | ⚠ sin valor → MUI: no existen (D2) | | | | |

Notas:
- Contraste blanco-sobre-swatch sin resolver; no existe adaptación dark de los 8 colores (D8).
- Solo-lectura por columna restringida: wrapper opacity 0.7 (`CellRenderer.tsx:292-295`); STATUS final/aprobado gestiona su propio candado.

### Opción del selector de estado
Fuente: `StatusCell.tsx:267-550` (popover) y `:315-329` (opciones).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `swatch.status.*` color de opción | `#ffffff` (D8) | — | — | radio 15px (`borderRadius 1.5`, D7) · px 12px py 6.8px · 13px/600 · gap 4px · transición `filter 0.15s, transform 0.1s` (0.1s ≠ `motion.micro` .12s) |
| hover | = | = | — | — | `filter: brightness(0.88)` |
| activo | ⚠ sin valor → MUI: sin estilo (D2) | | | | |
| focus-visible | ⚠ sin valor → MUI: sin anillo (`Box`) (D2) | | | | |
| seleccionado | = | = | `outline 2px solid` `bg.surface` `#ffffff` / `#253662` | `0 0 0 2px <color de opción>` (doble anillo, sin offset) | |
| deshabilitado | filtrada del picker (`!o.disabled`); en edición opacity 0.45 + `line-through` | | | | |
| contenedor | `bg.surface` | — | — | `shadow.menu` | 280px · radio 20px (`borderRadius 2`, sobrescribe `Paper` 12px) (D7) |
| "Limpiar selección" / "Agregar etiqueta" | transparent → hover `overlay.hover` | `text.secondary` / `brand.default` | `border.subtle` `1px dashed #dde3ec` / `rgba(74,144,226,0.12)`; hover `text.secondary` / `brand.default` | — | radio 15px · 12.5px (/600 en agregar) |

Notas:
- `transform` 0.1s declarado y nunca usado (`StatusCell.tsx:325`).
- Acciones de la fila de edición: opacity 0 → 1 con `transition opacity 0.15s`; swatch 24px radio 10px con `scale(1.1)`.

### Badge / punto (NUEVO, no leído, beta)
Fuente: `features/home/HomePage.tsx:141-203`, `features/board-view/components/ViewTabBar.tsx:543-557`, `layout/NotificationBell.tsx:182,267-302`, `BoardGridV2.tsx:294`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| NUEVO · reposo | `feedback.error.default` `#e2445c` / `#ef4444` | `text.onBrand` `#ffffff` | — | pulso `0 0 0 5px rgba(211,47,47,0)` (D20) | 10px/800 (D22) · letter-spacing 0.4px · px 7.2px py 0.8px · `radii.pill` 99px · `freshPulse 2s ease-in-out infinite` |
| NUEVO · hover/activo/focus/deshabilitado | no interactivo | | | | |
| beta · reposo | `feedback.warning.default` `#fdab3d` / `#f59e0b` | `#ffffff` (1.90) (D8) | — | — | 10.5px/700 uppercase · letter-spacing 0.4 · radio 10px (`radii.base`) · duplicado 2× en el archivo |
| MUI Badge (conteo) | `feedback.error.default` | `#ffffff` | — | — | ⚠ sin valor → MUI: h20, min 20, radio 10, padding `0 6px`, 12px/600, entra `scale` 225ms / sale 195ms (D21) |
| MUI Badge (punto) | `brand.default` `#0065BB` | — | — | — | 8×8px · radio 4px (MUI) · `ChartSettingsDialog.tsx:223` |
| no leído · punto | `brand.default` `#0065BB` | — | — | — | 8×8px · radio 50% · `NotificationBell.tsx:296-302` |
| no leído · fila | NUEVO: `bg.unread` `rgba(0,101,187,0.04)` / `rgba(0,101,187,0.08)` (dark usa primary de light, D11) | peso 600 (leído 400) | — | — | hover `overlay.hover` · transición `background-color 0.15s` |
| contador no leído (grilla) | `feedback.error.default` `#e2445c` fijo (sin dark, D9) | `#ffffff` | — | — | 14×14px · 8px/700 · radio 50% |
| focus-visible (todos) | ⚠ sin valor → MUI: sin anillo (D2) | | | | |

Notas:
- El anillo del pulso es `#d32f2f` (rojo MUI stock), no `error.main` (D20); `ReleaseEntry.tsx:149` usa otro rojo `#ff5252` (D9).
- Radio 25px en el callout de `HomePage.tsx:184-203` (D7); badge 10.5px/700 y 10px/800 sin token (D22).

### Tabla — celda de cabecera
Fuente: `T:217-235` (MUI `TableCell` head).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `bg.tableHead` `#0065BB` / `#2d3c53` (D12) | `text.onBrand` `#ffffff` | NUEVO: `border.onHead` derecho `1px solid rgba(255,255,255,0.12)` / `rgba(74,144,226,0.12)` | — | 11px/600 (`fontSize.overline`) · `text-transform: none` · letter-spacing `0.01em` · padding `9px 12px` · nowrap |
| borde inferior | — | — | ⚠ sin valor → MUI: `rgba(250,251,252,1)` / `rgba(23,46,72,1)` (D21) | — | casi invisible sobre el azul |
| hover / activo / focus-visible / seleccionado | no interactiva | | | | |

Notas:
- El token `letterSpacing.tableHeader` `0.06em` no coincide con el `0.01em` real (T:230) (D15); uppercase eliminado en T:221-229.
- Cabeceras locales divergen: grilla `bg.groupHeader` `#f0f4f9`/`#2d3c53` 13px/700 (`BoardGridV2.tsx:1346`), `#f5f7fa` 11px/700 uppercase (`TemplateItemsTable.tsx:236-244`), 0.72rem (`SharedViewPage.tsx:165-181`), `ColumnHeaderCell.tsx:92-98` translúcida (D9, D12).

### Tabla — celda de cuerpo
Fuente: `T:238-262`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | ⚠ sin valor → MUI: transparent (hereda de Paper) | `text.primary` | `border.subtle` derecho e inferior `1px solid #dde3ec` / `rgba(74,144,226,0.1)` (el resto del dark usa 0.12) (D9) | — | padding 0 · 13px (`fontSize.dense`) · alto `density.tableRow` 38px |
| hover (fila) | `bg.rowHover` `#f7fafd` / `#2f435e` (sólido para sticky) | = | = | — | sin transición (instantáneo) |
| activo | ⚠ sin valor → MUI: sin estilo (D2) | | | | |
| focus-visible | ⚠ sin valor → MUI: `outline: 0` (D2) | | | | |
| seleccionado | ver "Tabla — fila" | | | | |
| deshabilitado / solo lectura | `bg.readOnly` NUEVO `rgba(15,23,42,0.035)` (dark: ninguno en legacy `ItemRow.tsx:496`) | = | = | — | grilla sí tiene dark `rgba(255,255,255,0.045)` |

Notas:
- Dark `rgba(74,144,226,0.1)` vs divider `0.12` (`T:242,245` vs `T:234,271`) (D9).

### Tabla — fila (reposo / hover / seleccionada / inactiva / solo lectura)
Fuente: `T:258-262`, `ItemRow.tsx:252-357,492-496`, `ui/UsersTable.tsx:113-119`, `TemplateItemsTable.tsx:354`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `bg.surface` `#ffffff` / `#2d3c53` (≠ `background.paper` dark `#253662`) (D12) | `text.primary` | `border.subtle` inferior | — | alto 38px (`density.tableRow`) |
| hover | `bg.rowHover` `#f7fafd` / `#2f435e`; UsersTable `overlay.hover` translúcido | = | = | — | UsersTable `transition background 0.15s`; hover legacy sticky `#e8eef5`/`#344463`, template `#f0f4f9`/`#344463` (D12, D23) |
| activo | ⚠ sin valor → MUI: sin estilo (D2) | | | | |
| focus-visible | ⚠ sin valor → MUI: `outline: 0` (D2) | | | | |
| seleccionada | `bg.selected` ⚠ sin valor → MUI: `rgba(0,101,187,0.08)` / `rgba(0,101,187,0.16)`; + hover `0.12` / `0.24` (D1) | = | = | — | prop `selected` nunca usada; UsersTable usa `ListItemButton selected` |
| inactiva | = | = | = | — | opacity 0.55 (`UsersTable.tsx:117`, `TeamsAdminPanel.tsx:427`) |
| solo lectura | `bg.readOnly` NUEVO `rgba(15,23,42,0.035)` / ninguno | = | = | — | wrapper opacity 0.7 + candado |
| arrastrando | = | = | = | — | opacity 0.4 |
| destino de arrastre | `rgba(0,101,187,0.08)` (centro/hijo) | = | `borders.indicator` 3px `#0065BB` arriba/abajo; centro `outline 2px solid #0065BB` offset -2px | — | `padding-top/bottom 40px`, `transition padding-top 0.15s ease` (sin dark) |
| cargando / vacío | cargando: `<LinearProgress />` reemplaza la tabla; vacío: py 48px, `text.secondary` | | | | `UsersTable.tsx:82,129-135` |

Notas:
- Siete variantes de hover de fila en el repo; `ItemRow.tsx:313` (`rgba(0,101,187,0.03)`) queda tapado por el hover del tema (D23, D12).
- Dimming de filas sin escala: 0.55 / 0.35 / 0.4 / 0.5 / 0.7 (D4).

### Tabla — contenedor
Fuente: `T:269-272`, `ui/UsersTable.tsx:89-92`, `SharedViewPage.tsx:157`, `TemplateItemsTable.tsx:227-229`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `bg.surface` | `text.primary` | `border.subtle` `1px solid #dde3ec` / `rgba(74,144,226,0.12)` | — | `radii.base` 10px |
| variante UsersTable | `bg.surface` | = | = | — | radio 20px (`borderRadius 2`, D7) |
| variante grupo | = | = | `borderLeft 3px` (`SharedViewPage.tsx:157`) / `4px` `borders.groupRail` color de grupo (`TemplateItemsTable.tsx:227`) | — | `SharedViewPage.tsx:209` usa `borderLeft` inválido (D20) |

Notas:
- Rail de grupo 3px vs `borders.groupRail` 4px (D7, D20).

### Grilla virtualizada (BoardGridV2: cabecera, fila, celda, banda de grupo)
Fuente: `features/board-view/components/BoardGridV2.tsx` (`GridColors` :875-905; fila :193-204; celda :179-181; cabecera :1346,1397; banda :340-352).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| cabecera · reposo | `bg.groupHeader` `#f0f4f9` / `#2d3c53` (D12) | `text.secondary` `#5a6a80` / `#a6b4c8` | `border.subtle` derecho | `shadow.stickyHead` `0 1px 3px rgba(0,0,0,0.07)` | 13px/700 · padding `10px 12px` · h `COLHEADER_H` 40px · sticky z4 |
| cabecera · arrastrando | `bg.surface` | = | — | — | opacity 0.5 · cursor grabbing · z10 |
| cabecera · destino | `alpha(primary,0.1)` | | | `inset 0 0 0 2px #0065BB` | |
| fila · reposo | `bg.surface` `#ffffff` / `#2d3c53` (D12) | `text.secondary` (nombre 14px/600) | `border.subtle` inferior | — | `density.gridRow` 40px |
| fila · hover | ⚠ sin valor → MUI: sin hover (los `div` no tienen `:hover`; la tabla MUI sí, `#f7fafd`/`#2f435e`) | | | | |
| fila · seleccionada | `bg.selected` `#eff5fe` / `#2f476d` (sólido) (D1, D12) | = | = | — | aplica también a TAREA sticky y celdas fijas |
| fila · focus-visible | ⚠ sin valor → MUI: ninguno (D2) | | | | |
| fila · arrastrando / en proceso | = | = | = | — | arrastrando opacity 0.4; borrando opacity 0.35 + `grayscale(1)` |
| fila · destino de arrastre | — | — | línea `borders.accent` 2px `#0065BB` | — | z6 |
| celda · reposo | `bg.surface` | `text.primary` | `border.subtle` derecho | — | `overflow hidden`; colapsada 36px |
| celda · solo lectura | NUEVO: `bg.readOnly` `rgba(15,23,42,0.035)` / `rgba(255,255,255,0.045)` | = | = | — | + wrapper opacity 0.7, candado 12px `text.disabled` (D4) |
| celda · focus / editando / seleccionada | ⚠ sin valor → MUI: sin contorno; la edición abre Popover; nombre inline `1px solid #0065BB`, radio 4px (D2) | | | | `SignatureCell.tsx:346` es la única con `&:focus` |
| celda · referencial | — | — | `borderLeft 2px solid #7c5cfc` (CONNECT) / `#00c875` (MIRROR) | — | `#7c5cfc` fuera de toda paleta (D9) |
| banda de grupo · reposo | `bg.groupHeader` `#f0f4f9` / `#2d3c53` (sticky, sólido); colapsada `alpha(groupColor,0.05)` | color de grupo `swatch.group.*` (14px/700) | rail `borders.groupRail` 4px | — | h `density.groupHeader` 44px · z11 · conteo `tint(c,'20')` 11px/700 (D11) |
| banda · arrastrando | `alpha(primary,0.08)` | | línea 3px `#0065BB` | `0 0 4px #0065BB` | etiqueta `#0065BB` + `#fff` 10px/700 radio 10px |
| fila resumen | `bg.surface` | | `2px solid` `border.subtle` inferior | — | h `density.groupSummary` 36px |
| vacío | `bg.surface` | `text.disabled` (D4) | `2px dashed` `border.subtle` | — | `radii.dialogFeature` 30px (`borderRadius 3`, D7) · `EmptyGroupState.tsx:12-19` |
| cargando | MUI `Skeleton text` 50%/60% | | | | |

Notas:
- Sin hover de fila ni foco/selección de celda: brecha de accesibilidad (D2); `#2d3c53` hard-coded ≥10 veces vs `#253662` del tema (D12).
- Drag de columna y fila usan opacity 0.5 / 0.4 sin escala (D4).

### Alert — standard (por severidad, compact)
Fuente: `T:337-341` (solo `borderRadius 8` y `fontWeight 500`); colores = MUI con `palette.*.light` auto-derivado (D21).

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| error | `feedback.error.subtle` ⚠ sin valor → MUI: `#FCF0F1` / `#180A0A` (D17, D21) | texto ⚠ MUI `#5C2A31` / `#F9C3C3`; ícono `feedback.error.default` `#e2445c` / `#ef4444` | — | — | `radii.control` 8px · peso 500 (D22) |
| warning | ⚠ MUI: `#FEF8EF` / `#181105` (D17) | texto ⚠ `#654A27` / `#FBDFB0`; ícono `#fdab3d` / `#f59e0b` | — | — | |
| success | ⚠ MUI: `#EAFAF3` / `#07140C` (D17) | texto ⚠ `#145439` / `#B8ECCB`; ícono `#00c875` / `#22c55e` | — | — | |
| info | ⚠ MUI: `#EDF8FC` / `#051315` (D17) | texto ⚠ `#214A5C` / `#AFE7F1`; ícono `#29ABE2` / `#06b6d4` | — | — | |
| geometría | — | body2 0.8125rem/1.5 · ícono 22px mr 12px opacity 0.9 | — | — | padding `6px 16px`; mensaje `8px 0` (MUI) |
| hover / activo / focus-visible | no interactivo | | | | |
| outlined | transparent | color = standard | ⚠ MUI `palette.light`: `1px solid #E7697C #FDBB63 #33D390 #53BBE7` / `#F26969 #F7B13B #4ED07E #37C4DC` (D21) | — | solo `AvisoCargaIncompleta.tsx:32,84` |
| descartable | — | `IconButton` cierre MUI | — | — | `MembersDialog.tsx:111`, `ProfilePage.tsx:220` |

Notas:
- Fondos dark casi negros sobre `#253662`/`#2A3547`; no existe `feedback.*.subtle` (D17).
- Radio local 20px (`AdminPage.tsx:567`, `TeamsAdminPanel.tsx:545`, `AuthPage.tsx:158`) y 10px (`SharedViewPage.tsx:829`) (D7).

### Alert — filled / Snackbar
Fuente: `ui/GlobalSnackbar.tsx:18-52`, `ui/UpdateAvailableBanner.tsx:36-72`, `SharedViewPage.tsx:819-833`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (default MUI) | light `feedback.*.default` `#e2445c #fdab3d #00c875 #29ABE2`; dark `feedback.*.hover` ⚠ MUI `palette.dark` `#A72F2F #AB6E07 #178941 #047F94` (D21) | `feedback.*.onColor` ⚠ MUI: `#fff` (error) / `rgba(0,0,0,0.87)` (resto) | — | — | |
| reposo (GlobalSnackbar) | = | `#1a2236` (light) / `#ffffff` (dark) | — | `0 4px 20px rgba(0,0,0,0.25)` (banner: `0.3`) (D16) | 600 (D22) · ancho 100% · bottom/right · autoHide 4000ms (7000ms con acción) |
| acción | — | `Button small` 800 underline `color inherit` | banner: `rgba(255,255,255,0.5)`, hover `#ffffff` | — | |
| cargando | = | `CircularProgress` 18px thickness 5 `inherit` | — | — | barra `LinearProgress determinate` h4 radio 2px, pista `rgba(255,255,255,0.3)`, min 220px |
| hover / activo / focus-visible | ⚠ sin valor → MUI: sin estilo (D2) | | | | |
| transición | — | — | — | — | MUI `Slide` 225ms / 195ms `cubic-bezier(0, 0, 0.2, 1)` / `cubic-bezier(0.4, 0, 0.6, 1)`; z-index 1400 (D15, D21) |

Notas:
- Blanco `#1a2236` sobre error da 3.93, blanco-sobre-dark-info 4.70; la regla `onColor` no está decidida (D8, D21).
- Sin `sx`, el tema impone peso 500 (`T:339`); los toasts son 600 (D22).

### LinearProgress
Fuente: `T:358-361`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (barra) | `brand.default` `#0065BB` (fuerza azul aunque `color="error"`) | — | — | — | h 3px · radio 4px · `overflow hidden` |
| reposo (pista) | ⚠ sin valor → MUI: `#9EC4E5` / `#00325D` (D21) | — | — | — | |
| indeterminado | = | = | — | — | MUI `indeterminate1 2.1s cubic-bezier(0.65,0.815,0.735,0.395) infinite` y `indeterminate2 2.1s cubic-bezier(0.165,0.84,0.44,1) 1.15s infinite` (D15) |
| determinado | = | = | — | — | transición MUI `transform .4s linear` |
| variante formulario | pista `${accent}33` | barra `accent` | — | — | h 6px · radio 10px (`borderRadius 1`) (`FormBuilder.tsx:3309`) (D7, D11) |
| hover / activo / focus-visible / deshabilitado | n/a | | | | |

Notas:
- Pista y animación sin token.

### CircularProgress
Fuente: ~50 usos; `ui/GlobalSnackbar.tsx:27`, `SelectAllCheckbox.tsx:120-127`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | — | `brand.default` `#0065BB`; `inherit` en botones; `rgba(255,255,255,0.5)` / `#fff` sobre rail | — | — | ⚠ sin valor → MUI: size 40, thickness 3.6; usados 10–28px (28 ×7, 18 ×4), thickness 5 en tamaños chicos (D15) |
| animación | — | — | — | — | MUI `circularRotate 1.4s linear infinite`, `circularDash 1.4s ease-in-out infinite` |
| en checkbox | — | — | — | — | 14px absolute `left 4` `top 50%` |

Notas:
- Sin escala de tamaños.

### Skeleton
Fuente: MUI (~50 usos, sin sobrescribir); `ui/LoadingScreen.tsx:11-100`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | ⚠ sin valor → MUI: `rgba(26,34,54,0.11)` / `rgba(232,237,244,0.13)` (D21) | — | — | — | text `scale(1,0.60)`; rounded 10px; circular 50% |
| animación | = | = | — | — | pulse `2s ease-in-out 0.5s infinite` opacity 1 → 0.4 → 1 |
| LoadingScreen board | `overlay.hover` | — | rail `borders.groupRail` 4px `#0065BB`; filas `1px solid` `border.subtle` | — | filas 38px · cabecera 36px |
| radios locales | — | — | — | — | 5px / 10px / 20px (`LoadingScreen.tsx:37-77`) (D7) |

Notas:
- LoadingScreen es el único sitio que sobrescribe el fondo (`action.hover`).

### Divider
Fuente: `T:366-372`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | — | — | `border.subtle` `#dde3ec` / `rgba(74,144,226,0.12)` | — | `thin` 1px solid; igual a `palette.divider`, la sobrescritura es redundante |
| sobre rail | — | — | `border.onRail` `rgba(255,255,255,0.1)` | — | `my 1.5 mx 2` (D10) |
| variantes | — | — | `dashed` ×4, `flexItem` vertical ×4 | — | `gapLine` aparece con `transition opacity .12s` (`motion.micro`) |

Notas:
- Patrón `border:'1px solid'` + `borderColor:'divider'` en tarjetas, popovers y marcos de tabla.

### Scrollbar
Fuente: `T:87-117`, `features/board-view/components/WFlowScrollbar.tsx:20-62,207-236`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| pista | `scrollbar.track` `#f0f4f9` / `#253662` | — | — | — | 6×6px · radio 3px |
| thumb reposo | `scrollbar.thumb` `#c0c8d4` / `#3d4f6f` | — | — | — | radio 3px; Firefox `thin` |
| thumb hover | `scrollbar.thumbHover` `#a0aab8` / `#4a6090` | — | — | — | sin transición |
| thumb activo | ⚠ sin valor → MUI: default del navegador | | | | |
| WFlow · pista | `rgba(13,40,73,0.05)` / `rgba(255,255,255,0.05)` | — | `border.subtle` superior | — | h 14px · cursor pointer |
| WFlow · thumb | `alpha(brand.default,0.5)`; hover `0.75`; arrastrando `brand.default` | — | — | — | h 8px · radio 4px · min 48px · `transition background-color 0.15s` (`motion.nav`) |
| WFlow · sin overflow | = | = | — | — | opacity 0.2, ancho 100% |

Notas:
- Doble definición de scrollbar: `T` 6px temada vs `index.css` 8px gris (D18).
- `body` transiciona `background-color 0.25s ease, color 0.25s ease` (`motion.collapse`) (`T:93-102`).

### Avatar
Fuente: defaults MUI; `PersonCell.tsx:63,105`, `ui/UsersTable.tsx:166-173`, `layout/Sidebar.tsx:701-712`, `layout/sidebar/WorkspaceAvatar.tsx:10-40`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo (MUI default) | ⚠ sin valor → MUI: `#bdbdbd` / `#757575` (D21) | ⚠ MUI: `#f0f4f9` / `#2A3547` (`background.default`, no blanco) | — | — | solo hereda si falta `bgcolor` (`ComentariosDelElemento.tsx:467`) |
| reposo (marca) | `brand.default` `#0065BB` | `bg.canvas` `#f0f4f9` por herencia; algunos sitios `#fff` (`GlobalCommentsPage.tsx:310`) | — | — | tamaños 18–36 y 64px; `density.avatar` 32px |
| reposo (usuario por nombre) | paleta propia de 8 colores `#6366f1 #0ea5e9 #10b981 #f59e0b #ef4444 #8b5cf6 #ec4899 #14b8a6` | `#ffffff` | — | — | 34px · 13px/700; distinta de `swatch.group.*` (D9) |
| reposo (rail) | `rgba(255,255,255,0.2)` (D10) | `text.onRail` | `2px solid rgba(255,255,255,0.35)` | — | 32px · 11px/700; hover footer `rgba(0,0,0,0.25)`, `transition background-color 0.15s` |
| reposo (espacio de trabajo) | `workspace.color`, fallback `#2979c4` (fuera de paleta, D9) | `#ffffff` size×0.48/700 | `2px solid rgba(255,255,255,0.28)` | `0 2px 6px rgba(0,0,0,0.25)` | radio `round(size×0.28)` |
| grupo (AvatarGroup) | — | — | `2px solid` `bg.surface` | — | 22px · 10px · max 3 |
| hover / activo / focus-visible / deshabilitado | ⚠ sin valor → MUI: sin estilo (D2) | | | | |

Notas:
- Texto por defecto `background.default` en vez de blanco: inconsistente entre sitios.
- Avatar con radio 20px (`HomePage.tsx:361`) (D7).

### Mosaico de ícono (stat / KPI / empty state)
Fuente: `features/admin/AdminPage.tsx:67-70,357-360`, `ui/EmptyState.tsx:14-23`, `TrashPanel.tsx:258-263`, `features/shared-view/ErrorScreen.tsx:13-18`, `OtpEmailScreen.tsx:44-51`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| stat · reposo | `alpha(c,0.1)` / `alpha(c,0.15)` (D11) | `c`: `#0065BB #00c875 #e2445c #fdab3d` | — | — | 38×38px · radio 15px (`borderRadius 1.5`, D7) |
| empty (genérico) | — | `text.secondary` opacity 0.4, ícono 56px | — | — | título `h6`; `py 6 px 3` |
| empty (Trash) | `overlay.hover` `rgba(0,101,187,0.05)` / `rgba(74,144,226,0.08)` | `text.disabled` 28px (D4) | — | — | 56×56px · radio 16px (fuera de `radii`, D7) |
| error | `feedback.error.default` | `#ffffff` 36px | — | — | 64×64px · radio 16px |
| logo OTP | `linear-gradient(135deg, #0065BB 0%, #29ABE2 100%)` | `#ffffff` 28px | — | — | 56×56px · radio 14px (`radii.dialog`) |
| KPI (gráfico) | sin fondo | valor `brand.default` 800 (D22); título `text.secondary` 600 | — | — | `font-size clamp(20px, min(Ncqw, 42cqh), 120px)` tabular-nums |
| hover / activo / focus-visible | no interactivos | | | | |

Notas:
- Receta de tinte distinta en cada mosaico (D11).
- `TemplatesGallery.tsx:171` usa `primary.50` inexistente (D20).

### StatCard (hover)
Fuente: `features/admin/AdminPage.tsx:60-75`.

| Estado | Fondo | Texto / ícono | Borde | Sombra / anillo | Otros |
|---|---|---|---|---|---|
| reposo | `bg.surface` | valor `h6` 700 lh 1.2 (D22); etiqueta `caption` `text.secondary` | `border.subtle` `1px solid #dde3ec` / `rgba(74,144,226,0.12)` | — | radio 20px (`borderRadius 2`, D7) · px 20px py 16px · gap 16px · transición `border-color 0.15s, box-shadow 0.15s` (`motion.nav`) |
| hover | = | = | color de la métrica `c` | `0 0 0 1px alpha(c,0.3)` | |
| activo / focus-visible / deshabilitado | ⚠ sin valor → MUI: sin estilo (D2) | | | | |

Notas:
- Anillo propio sin rol de sombra (`shadow.*`); el radio 20px no pertenece a `radii` (D7, D16).

### Keyframes

| Nombre | Definición | Duración | Easing | Uso | Fuente |
|---|---|---|---|---|---|
| `freshPulse` | `0%,100% box-shadow 0 0 0 0 rgba(211,47,47,0.45)` · `50% 0 0 0 5px rgba(211,47,47,0)` | 2s infinite | `ease-in-out` | badge NUEVO (D20) | `HomePage.tsx:166-170` |
| `freshCalloutIn` | `from opacity 0, translateY(-6px)` → `to opacity 1, translateY(0)` | .45s both | `cubic-bezier(.2,.9,.3,1.2)` | callout | `HomePage.tsx:192-196` |
| `wfTourPulse` | `0%,100% 0 0 0 9999px rgba(15,23,42,0.55), 0 0 0 0 rgba(0,101,187,0.5)` · `50% … 0 0 0 9px rgba(0,101,187,0.12)` | 1.6s infinite | `ease-in-out` | anillo del tour | `FeatureTour.tsx:216-220` |
| `wfTourDot` | `0%,100% 0 0 0 0 rgba(0,101,187,0.45)` · `50% 0 0 0 6px rgba(0,101,187,0.10)` | 1.6s infinite | `ease-in-out` | punto del tour | `FeatureTour.tsx:295-299` |
| `pulse` (nombre global) | `0%,100% scale(1), opacity 1` · `50% scale(1.6), opacity 0.4` | 1.6s infinite | `ease-in-out` | punto de release | `ReleaseHero.tsx:104-109` |
| `slideRight` | `opacity 0, translateX(-12px)` → `1, 0` | 0.6s, delay 0.1s, both | `cubic-bezier(0.16,1,0.3,1)` | eyebrow hero | `ReleaseHero.tsx:73-77` |
| `drawLine` | `width 0` → `32` | 0.8s, delay 0.2s, both | `cubic-bezier(0.16,1,0.3,1)` | línea hero | `ReleaseHero.tsx:82-86` |
| `fadeIn` v1 | `opacity 0` → `1` | 0.5s, delay 0.5s, both | `ease` | hero "new" | `ReleaseHero.tsx:99-100` |
| `fadeIn` v2 (mismo nombre) | `opacity 0, translateY(8px)` → `1, 0` | 0.8s, delay 0.5s, both | `cubic-bezier(0.16,1,0.3,1)` | Lottie hero (D20) | `ReleaseHero.tsx:216-220` |
| `titleIn` | `opacity 0, translateY(16px)` → `1, 0` | 0.7s, delays .25/.4/.55s, both | `cubic-bezier(0.16,1,0.3,1)` | título hero | `ReleaseHero.tsx:131-161` |
| `enter` | `opacity 0, scale(0.9)` → `1, 1` | 0.35s | `cubic-bezier(0.16,1,0.3,1)` | BrandLoader | `ui/BrandLoader.tsx:19-22,55` |
| `topeDeLaLista` | `opacity 0, scaleY(0.2)` → `25% 1, scaleY(1)` → `0` | .4s forwards | `ease-out` | tope de lista | `form-view/formato/ColumnasSinUsar.tsx:100-104` |
| `bfSpin` / `wfSpin` | `to rotate(360deg)` | 0.8s infinite | `linear` | spinner demo | `BoardFlowDemo.tsx:319`, `BoardDemo2D.tsx:1031` |
| `wfBlink*` | `50% opacity 0` | 0.9s infinite | `step-end` | cursor demo | `BoardDemo2D.tsx:743,778,930` |
| MUI Skeleton pulse | `0% 1` · `50% 0.4` · `100% 1` opacity | 2s, delay 0.5s infinite | `ease-in-out` | Skeleton | MUI |
| MUI circular | rotate 360; dash `1px,200px → 100px,200px(-15px) → 1px,200px(-126px)` | 1.4s infinite | `linear` / `ease-in-out` | CircularProgress | MUI |
| MUI linear indeterminate 1/2 | barra left/right | 2.1s infinite (2: delay 1.15s) | `cubic-bezier(0.65,0.815,0.735,0.395)` / `cubic-bezier(0.165,0.84,0.44,1)` | LinearProgress | MUI |
| MUI badge | `scale(0 ↔ 1)` | 225ms in / 195ms out | `cubic-bezier(0.4,0,0.2,1)` | Badge | MUI |

Notas:
- `motion.easing` `cubic-bezier(0.32, 0.72, 0, 1)` no lo usa ninguna de estas animaciones; el repo mezcla `ease`, `ease-in-out`, `linear`, `step-end` y cuatro `cubic-bezier` distintas (D15).
- Duraciones 0.1s/0.15s/0.4s/0.6s+ no coinciden con `motion.micro .12s / nav .15s / control .2s / collapse .25s` salvo .15s (D15).

## Deriva de cts-theme frente a cts-manager (D15)

Tokens de `src/tokens.ts` y `src/mui/theme.ts` que ya no coinciden con
cts-manager, o que nunca vinieron de su código.

| Token | cts-theme | cts-manager hoy | Fuente | Tipo |
|---|---|---|---|---|
| `letterSpacing.tableHeader` | `'0.06em'` | `'0.01em'`, y `textTransform: 'none'` | `T:229-230` (cambio del 8-sep-2026) | deriva |
| `typography.button.textTransform` | `'none'` en la tipografía | solo en `MuiButton.root` (`T:125`) | `T:66`, `T:125` | deriva: en cts-theme también afecta a `Tab`, `ToggleButton` y `variant="button"` |
| `density.navItem` | `34` | sin alto fijo; unos 40px calculados | `Sidebar.tsx:60-86` | deriva (sin medir) |
| `density.floatingAction` | `38` | unos 30px (`IconButton size="small"`); medido 30 / 32px [M] | `NotificationBell.tsx:166-182` | deriva |
| `motion.easing` | `cubic-bezier(0.32, 0.72, 0, 1)` como «ease global» | solo en la página de novedades; la app usa `ease` | `freshTheme.ts:114` | alcance |
| `letterSpacing.eyebrow` | `'0.32em'` | solo en la página de novedades | `freshTheme.ts:107-113` | alcance |
| `layout.railIconWidth` | `64` | no existe; el rail colapsa a 0 | `build.py` | solo hoja de diseño |
| `layout.toolbarSelectMinWidth` / `MaxWidth` | `135` / `185` | no existe | `build.py` | solo hoja de diseño |
| `layout.panelMinWidth` / `MaxWidth` | `300` / `360` | paneles reales de 440 y 720 | `build.py` | solo hoja de diseño |
| `spacing.cardGapMin` / `Max` | `16` / `24` | no existe como valor | `build.py` | solo hoja de diseño |
| `artboardWidth` | `1440` | no aplica (es de la hoja) | `build.py` | solo hoja de diseño |
| `shadows.elevation1` | `0 1px 4px rgba(0,0,0,0.06)` | `shadows[1]` igual, pero `MuiPaper.elevation1` es `0 2px 8px rgba(0,0,0,0.07)` | `T:75`, `T:161-162` | ambiguo (D16) |
| `shadows.card` | `'none'` | plano solo con `variant="outlined"`; 10 de 22 `<Card>` llevan sombra | `T:172-178` | ambiguo (D16) |
| `rail.sectionTitle` / `rail.descriptor` | `rgba(255,255,255,0.45)` / `0.55` | `opacity: 0.45` / `0.55` sobre blanco | `Sidebar.tsx:455,491` | ambiguo (mismo color, otra técnica) |

Las hojas de `docs/demo/build.py` también quedaron atrás: dibujan la cabecera
de tabla en mayúsculas con `0.06em`, el tooltip enriquecido con radio 12 y
ancho 300 (real: 15 y 420), y el diálogo destacado con radio 24 (real: 30).

## Decisiones abiertas

Cada decisión trae las opciones y una recomendación. Nada marcado con una
decisión se codifica en el paso 2 hasta tener respuesta. Las recomendaciones
usan solo valores que ya existen en cts-manager, salvo donde se dice.

#### Notas del desarrollador

Respuestas generales:

  * No usaremos ningún _default_ de MUI
  * Tomaremos el valor de MUI como primitivo en caso de que sea necesario
  * Sobreescribiremos cualquier valor por defecto que sea necesario

**D2**: Creación de un rol estándar para los 'outline' de los átomos
**D3**: 

### D1 · Un solo «seleccionado»

**Problema.** Hay dos mecanismos. MenuItem, ListItemButton y Select usan el
de MUI: `#0065BB` al 0.08 (claro) y 0.16 (oscuro), 0.12 / 0.24 con hover.
El tema declara `action.selected` (`rgba(0,101,187,0.1)` /
`rgba(74,144,226,0.16)`), que solo se ve donde el código lo escribe a mano.

**Opciones.** (a) Todos usan `overlay.selected` del tema. (b) Todos usan el de MUI.

**Recomendación.** (a). Es el valor que el tema declara; el otro es un efecto
secundario de MUI.

### D2 · Estándar de focus-visible

**Problema.** Solo el input tiene anillo (`0 0 0 3px rgba(0,101,187,0.15)`).
La edición en línea usa `0 0 0 2px rgba(41,171,226,0.45)`, una píldora
`0.55`, los enlaces el `outline: auto` del navegador, y botones outlined, text,
ítems del rail, swatches y celdas de estado no tienen indicador.

**Opciones.** (a) `focus.ring` para todo átomo interactivo sobre superficie
clara u oscura. (b) Anillo de 2px celeste (el de edición en línea).

**Recomendación.** (a). Sobre el rail azul ningún anillo existente se ve bien,
y **no hay valor en cts-manager**: hace falta que definas uno (sería el único
valor nuevo del sistema).

### D3 · `action.*` de modo claro

**Problema.** En claro, `action.active`, `disabled`, `disabledBackground` y
`focus` no están definidos; se ven los negros de MUI
(`rgba(0,0,0,0.54)`, `0.26`, `0.12`, `0.12`). En oscuro sí están definidos.

**Recomendación.** Escribir los valores de MUI tal cual como roles. No cambia
nada visible y los fija aunque MUI cambie sus valores por defecto entre
versiones.

### D4 · `text.disabled`

> **Resuelto (2026-11-13, G8 de Estandares-Globales.md):** `#808a99` claro / `#626e81` oscuro, de E-Panel.

**Problema.** 435 usos y el tema no lo define. Se ve `rgba(0, 0, 0, 0.38)` /
`rgba(255, 255, 255, 0.5)`.

**Recomendación.** Igual que D3: escribir esos dos valores como el rol.

### D5 · Borde del input en hover

**Problema.** `T:197-199` pide `#0065BB` (claro) y `rgba(41,171,226,0.5)`
(oscuro), pero una regla de MUI más específica gana, y el navegador pinta
`text.primary` (`#1a2236` / `#e8edf4`) [M]. La hoja de diseño
(`build.py:288`) documenta el azul.

**Opciones.** (a) Hacer que el azul funcione (intención del tema y de la hoja).
(b) Copiar lo que se ve hoy.

**Recomendación.** (a). Es un cambio visible frente a cts-manager hoy.

### D6 · Foco de los botones contained

**Problema.** Con teclado, un botón contained recibe `shadows[6]`
(`0 16px 40px rgba(0,0,0,0.16)` / `0.65`) [M]. Es un accidente: el arreglo de
sombras repite ese valor del 6 al 24. Outlined y text no tienen indicador.

**Recomendación.** Resolver con D2 (mismo anillo para todos los botones).

### D7 · Radios multiplicados por 10

**Problema.** `borderRadius: 1.5 / 2 / 2.5 / 3 / 3.5` en `sx` dan 15, 20, 25,
30 y 35px. Unos 40 lugares: popovers de celdas (20), alertas de admin (20),
tarjetas de estadística (20), botones e inputs de admin (15–20 en vez de 8),
diálogo de confirmación global (30), tarjeta del recorrido (35).

**Opciones.** (a) Ajustar cada caso a la escala de `radii` según su nivel
(control 8, menú/popover 10, card 12, diálogo 14). (b) Agregar 15, 20, 25 y
35 a `radii`.

**Recomendación.** (a), y mantener `dialogFeature 30`, que ya es un token.

### D8 · Contraste de la celda de estado

**Problema.** Texto blanco sobre `#fdab3d` (1.90:1), `#00c875` (2.21:1) y
`#c4c4c4` (1.74:1); AA pide 4.5:1. No hay variante oscura. Los colores son
datos guardados por el usuario, así que no se pueden cambiar.

**Opciones.** (a) Dejarlo como está. (b) Elegir el color del texto por
contraste: `text.primary` `#1a2236` sobre colores claros, blanco sobre
oscuros. (c) Agregar un borde o ícono.

**Recomendación.** (b). Es un comportamiento nuevo (no existe en
cts-manager), así que necesita tu visto bueno.

### D9 · Familias de casi-duplicados

23 familias; la lista completa está en el panel de la auditoría. Hay dos
grupos:

- **Propuesta de unir (sin cambio visible apreciable).** Por ejemplo
  `#0066B1`, `#0078d4` y `#1976d2` → `#0065BB`; `#808080` / `#888` /
  `#787d80` → `#7F7F7F`; `#e0e7ef` / `#e2e8f0` / `#e4e9f1` → `#dde3ec`;
  `#1a2333` → `#1a2236`; los tres verdes `#00a65c` / `#00a65a` / `#00a05f` →
  uno.
- **Necesitan tu decisión.** Los grises claros `#C9C9C9` / `#c8c8c8` /
  `#c4c4c4` (`#c4c4c4` es dato y se queda). La tinta gris de los documentos
  `#5b6474` frente a `#5a6a80`. El fondo oscuro del login `#1a1a2e` frente a
  `#2A3547`. Los tres tooltips oscuros `#1e2d42` / `#1e293b` / `#1a2333`. El
  divisor oscuro `0.1` frente a `0.12`. El hover de marca (D13). El texto de
  aviso (`#e69b2e` / `#e08a1e` / `#e8a33d`).

**Recomendación.** Aceptar el primer grupo en bloque y decidir el segundo uno
por uno.

### D10 · Escalera de blancos del rail

**Problema.** 24 pasos de alfa en uso; `tokens.rail` tiene 11.

**Recomendación** (todos valores ya presentes): hover `0.1`, activo `0.18`,
indicador `0.9`, texto en reposo `0.65`; unificar `0.09` → `0.1`, `0.15` →
`0.18` (activo de tableros), `0.85` → `0.9`, `0.75` / `0.78` → `0.7`; y
agregar como tokens `0.5` (×13), `0.6` (×9), `0.7` (×6) y `0.3` (×3).

### D11 · Escaleras de tinte

**Problema.** El tinte de marca usa alfas de 0.03 a 0.5. En oscuro alterna
tres bases. `tint()` solo acepta `20` y `18`.

**Recomendación** (valores observados): `brand.subtle` `rgba(0,101,187,0.05)` /
`rgba(41,171,226,0.10)`; fuerte `0.1` / `0.16`; borde `0.15` / `0.25`. En
oscuro, base siempre `41,171,226`. Ampliar `tint()` a `'18' | '20' | '33'`.

### D12 · Escalera de superficies oscuras

**Problema.** `#2d3c53` (×18) es la superficie oscura más usada y no tiene
token. Le siguen `#2f435e` (hover de fila), `#2f476d` (seleccionado),
`#344463` y `#3a4d6a` (hovers de tablas antiguas).

**Recomendación.** Adoptar `#2d3c53` (`bg.raised`, `bg.tableHead`,
`bg.groupHeader`), `#2f435e` (`bg.rowHover`) y `#2f476d` (`bg.selected`). Unir
`#344463` y `#3a4d6a` a `#2f435e`.

### D13 · Hover de marca por modo

**Problema.** Botón primario `#004696`; botón flotante del rail `#0078d4`
(claro, más claro que la base) y `#2e4275` (oscuro); novedades `#1278cf`.

**Recomendación.** `brand.hover` `#004696` en ambos modos para botones; el
botón flotante usa `onRail.hover`, sin azules nuevos.

### D14 · Texto de marca en modo oscuro

**Problema.** `#0065BB` como texto, borde o enlace sobre `#253662` / `#2A3547`
da 2.01:1 / 2.11:1 [M]. El código usa `#89AEDC` (×19) para ese trabajo, y
además `primary.light` y `lighten(primary.main, 0.55)`.

**Recomendación.** `text.brand` = `#0065BB` / `#89AEDC`. `brand.default` sigue
siendo `#0065BB` para rellenos.

### D15 · Deriva de tokens

> **Resuelto en parte (2026-11-13, G11):** `tableHeader` 0.01em, `shadows.paper` y `shadows.buttonSecondaryHover` siguen a cts-manager; el easing único queda en `cubic-bezier(0.32, 0.72, 0, 1)`.

Ver la tabla de deriva. **Recomendación:**

- `letterSpacing.tableHeader` → `'0.01em'`.
- `textTransform: 'none'` → al átomo Button, fuera de `typography.button`.
- `navItem` y `floatingAction` → medir en el paso 3 y fijar el valor medido.
- `motion.easing` → documentarlo como curva de la página de novedades, no
  como global.
- Tokens que solo vienen de las hojas de diseño → mantenerlos, con la nota
  «diseño, sin implementar en cts-manager».

### D16 · Sombra de elevación 1 y de card

**Problema.** Tres sombras parecidas: `shadows[1]` (`0 1px 4px 0.06`),
`MuiPaper.elevation1` (`0 2px 8px 0.07`) y `shadows[2]` (`0 2px 8px 0.08`).
`shadows.card: 'none'` solo se cumple con `variant="outlined"`.

**Recomendación.** `shadow.e1` = `shadows[1]`; `shadow.paper` aparte para
Paper; la card sigue al código (con sombra salvo `outlined`).

### D17 · Fondos suaves de retroalimentación

**Problema.** Unos 83 `Alert` usan el estilo standard de MUI sin colores CTS.
En oscuro sus fondos salen casi negros (`#180A0A`, `#181105`, `#07140C`,
`#051315`). No hay `feedback.*.subtle`.

**Recomendación.** Definir `feedback.*.subtle` con los pares observados en
`FormulaEditor.tsx:427-468` y `ShareModal.tsx:320-344` (alfa 0.06–0.08 en
claro, 0.08–0.1 en oscuro, sobre el color oscuro de cada estado) y usarlos en
el Alert standard.

### D18 · Barra de desplazamiento duplicada

**Problema.** `ctsTheme.ts` la define con 6px y colores del tema; `index.css`
con 8px y grises `#f1f1f1` / `#C8C8C8` / `#8F8F8F`, sin modo oscuro.

**Recomendación.** Solo la del tema.

### D19 · Variantes de tooltip

**Problema.** Cuatro estilos: el del tema, el enriquecido de
`SharedViewPage.tsx` (radio 15, ancho 420), `LazyTooltip` (colores Tailwind) y
un tercero con `#1a2333`.

**Recomendación.** Dos átomos: el tooltip del tema y el tooltip enriquecido
de `SharedViewPage`. `LazyTooltip` queda local.

### D20 · Errores de cts-manager que no se portan

No se copian; conviene abrir un issue en cts-manager para cada uno:

- `#1976d2` y `rgba(25,118,210,0.9)` en el botón «+» del rail (`Sidebar.tsx:588-592`), el azul por defecto de MUI.
- `rgba(211,47,47,α)` (rojo por defecto de MUI) en el pulso de «NUEVO» (`HomePage.tsx:168-169`) y en `AutomationBuilder.tsx:1037`.
- `primary.50`, `warning.50`, `error.50`, `success.50` (23 usos): no existen y no pintan nada; incluye el hover de todos los botones de `BoardToolbar.tsx:21`.
- `borderLeft` inválido en `SharedViewPage.tsx:209`.
- `@keyframes fadeIn` global definido dos veces con cuerpos distintos.
- `disableElevation` no quita la sombra azul de los botones primarios (9 lugares).

### D21 · Tonos que calcula MUI

**Problema.** `error.dark` (`rgb(158, 47, 64)`), `warning.dark`
(`rgb(177, 119, 42)`), los `light`, y `contrastText` (negro al 87 % sobre
aviso, éxito e info) no son literales en cts-manager: MUI los calcula.

**Recomendación.** Escribir los valores calculados como literales. Así no
dependen de la fórmula de cada versión de MUI (6, 7 y 9).

### D22 · Pesos 500 y 800

> **Resuelto (2026-11-13, G5):** no existen en el sistema; 500 → 600 y 800 → 700. El preset de ESLint los rechaza.

**Problema.** `fontWeight` 500 tiene 34 usos (tooltip, alert, migas…) y 800
se usa en KPI y en el título de novedades; ninguno tiene token. Ojo:
`typography.fontWeightMedium` ya vale 600.

**Recomendación.** Agregar los dos. Hay que elegir nombres que no choquen con
`fontWeightMedium`.

### D23 · El hover apaga el ítem activo

**Problema.** En `NavItem` y `BoardItemRow`, la regla `&:hover` pisa el fondo
activo, así que el ítem actual se atenúa (de `0.18` a `0.1`) al pasar el
mouse.

**Recomendación.** El estado activo gana sobre hover.

## Fuera de alcance

- **Paletas locales:** página de novedades (`features/releases/`, 298 usos),
  documentos de formato (136), selector de color con rueda cónica, colores de
  gráficos (Tailwind slate), tipos de archivo. Se quedan en su página.
- **ToggleButton y ToggleButtonGroup** (30 y 14 usos): no se auditaron.
  Pendiente antes del paso 2 si van a ser átomos.
- **Componentes compuestos** (sidebar completo, login, páginas): fuera de esta
  rama. Se construyen sobre los átomos cuando estén aprobados.

## Pasos siguientes

1. **Paso 1 (este documento):** revisar y responder D1–D23.
2. **Paso 2 (código):** `src/colors.ts` (primitivos nuevos) → `src/roles.ts`
   (`roles(mode)`) → `src/atoms.ts` (`atoms(mode)`, tipado por estado) →
   `src/mui/components.ts` (overrides que leen solo átomos) →
   `src/mui/theme.ts` (expone `theme.cts.roles` y `theme.cts.atoms`).
3. **Paso 3:** pruebas de humo en `smoke/`, `pnpm typecheck:matrix`
   (MUI 6, 7 y 9) y `pnpm build`.

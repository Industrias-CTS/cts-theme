# Móvil — lo que el sistema todavía no define

El Sistema de Diseño CTS está especificado **solo para escritorio**: los nueve
artboards de `docs/demo/` miden 1440 px de ancho y la hoja
«Estructura» numera las zonas 1–10 en esa medida. No existe ninguna hoja
móvil.

Este paquete **no inventa** valores móviles. En su lugar deja los *ejes* de la
API abiertos, de modo que cuando el diseño se ratifique sea un cambio de
**valor**, no de firma — sin major de ruptura para las apps que ya consuman
el paquete.

## Ejes ya reservados (implementados como API, no como estilos)

| Eje | Valor ratificado hoy | Valores que el móvil añadirá | Por qué no rompe |
|---|---|---|---|
| `NavRail.variant` | `'permanent'` | `'collapsed'` · `'temporary'` | La hoja «Navegación» ya dice *«colapsable a 0 con FAB de reapertura, o 64px»*. El overlay móvil es un tercer valor sobre un eje que el sistema **ya tiene**. |
| `NavRail.open` / `onOpenChange` | controlado y no controlado desde el día 1 | cierre automático al navegar | Cambio de comportamiento interno, no de API. |
| `SidePanel.variant` | `'inline'` (300–360 px) | `'overlay'` | Zona 10 pasa a hoja deslizante sin tocar la firma. |
| `density` (contexto) | `'compact'` — filas 38 px | `'comfortable'` — **mapeo sin definir** | Ver conflicto 1. |
| `tokens.breakpoints` | valores por defecto de MUI | los que ratifique diseño | Son solo números en `tokens.ts`. |
| `sx` + `className` en todos los componentes | siempre | parche por app antes de la ratificación | Vía de escape mientras tanto. |

## Conflictos que diseño debe resolver

Ninguno de estos tiene respuesta en las hojas actuales. Están numerados para
poder citarlos en la discusión.

1. **Altura de fila contra objetivo táctil.** El sistema fija filas de 38/40 px,
   ítems de nav de 34 px y controles de toolbar de 32 px («densidad de hoja de
   cálculo»). Las guías táctiles piden ≥44 px. Es una contradicción directa:
   o el móvil abandona la densidad, o acepta objetivos pequeños. **Decisión de
   diseño, no de implementación.**
2. **El rail (zona 1) en pantalla estrecha.** 256 px sobre un viewport de 360 px
   es el 71 %. ¿Overlay temporal sobre el contenido, franja de 64 px solo con
   iconos, o barra inferior? La hoja ofrece dos de las tres.
3. **Acciones flotantes (zona 6).** `fixed top:16 right:16` choca con el FAB de
   reapertura del rail cuando el rail está colapsado, y con el *notch* /
   `safe-area-inset` de los teléfonos. Sin definir.
4. **Toolbar de vista (zona 8).** Búsqueda 200 px + selects 135–185 px + CTA no
   caben en una fila a 360 px. ¿Envuelven, hacen scroll horizontal, o colapsan
   en una hoja de filtros? Sin definir.
5. **Panel lateral (zona 10).** 300–360 px es la pantalla entera de un teléfono.
   ¿Hoja deslizante, ruta a pantalla completa, o acordeón bajo el contenido?
6. **Migas de pan (zona 7).** Rutas largas a ancho estrecho: ¿truncado por el
   medio, solo el último nivel, o scroll?
7. **Tablas (hoja «Tablas y listas»).** Filas de 38 px con muchas columnas:
   ¿scroll horizontal conservando la cabecera azul, o transformación a cards?
8. **Diálogos.** Radios 14 / 30 px; en móvil suelen ir a pantalla completa
   (donde el radio desaparece). Sin definir.
9. **Breakpoints.** El sistema no nombra ninguno. `tokens.breakpoints` usa hoy
   los de MUI (0 / 600 / 900 / 1200 / 1536) marcados como **provisionales**.

## Cómo se cierra esto

La ratificación no vive en este paquete: vive en `docs/demo/build.py`,
como hojas nuevas (`v_movil_estructura`, `v_movil_controles`, …) con artboards
de ancho móvil, igual que las nueve existentes. Después:

1. Se copian los valores literales a `src/tokens.ts` (misma regla de oro: sin
   redondear).
2. Se sustituyen los `breakpoints` provisionales por los ratificados.
3. Se implementan los valores nuevos de los ejes ya reservados.
4. Se borran de este archivo los conflictos resueltos.

Mientras tanto, cualquier app que necesite móvil **parchea con `sx`** y anota
aquí qué tuvo que inventar, para que la ratificación parta de datos reales y no
de cero.

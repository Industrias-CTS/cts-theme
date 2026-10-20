# Demo estática de átomos CTS

Página de una sola pantalla que muestra los átomos de [`docs/ATOMOS.md`](../ATOMOS.md)
por sección, en claro y en oscuro, con cada micro-estado.

- `sistema-atomos-cts.html` — la demo. Se abre directo en el navegador; no necesita servidor ni JavaScript.
- `build.py` — generador. Regenera el HTML desde las listas de átomos, captions y tokens.

```bash
python3 docs/atomos-demo/build.py   # reescribe sistema-atomos-cts.html
```

## Secciones

1. **Primitivos y roles** — paleta de `src/colors.ts`, primitivos nuevos y tabla de roles (claro / oscuro).
2. **Controles** — botones, íconos, campos, selección, switch, swatches, enlaces y un formulario de acceso.
3. **Navegación y capas flotantes** — rail, pestañas, menús, tooltips, diálogos, migas y composiciones (barra de vistas, selector de estado).
4. **Datos y retroalimentación** — chips, estados, badges, tablas, grilla, alertas, progreso, avatares y estadísticas.

## Cómo leer las marcas

- **Aviso amarillo «Sin decidir»**: el átomo tiene decisiones D1–D23 abiertas en `ATOMOS.md`. Lista el D-número y qué falta decidir. Nada de lo marcado está codificado.
- **Franja amarilla y etiqueta «⚠ sin valor»**: el estado no tiene valor en cts-manager. Se dibuja el valor que pone MUI, indicado en la caption.
- **Caption bajo cada celda**: el valor literal (hex, rgba, px) y su fuente. «[M]» = medido en navegador; «MUI» = calculado por MUI, no literal en el código.
- **`T:131`**: `theme/ctsTheme.ts` línea 131 de cts-manager. Las demás rutas son relativas a `cts-manager/frontend/src`.

## Estado

Borrador para revisión, paso 1 de `feat/atoms`.

Verificación: una lectura independiente contra cts-manager corrigió valores y
citas. Quedan sin verificar los valores marcados [M] (medidos en navegador) y
algunos de MUI que la demo no reproduce exactamente.

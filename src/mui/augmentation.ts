/**
 * Augmentación del tema de MUI: expone los tokens CTS como `theme.cts`.
 *
 * Existe porque el sistema se escribe con el prop `sx` (hoja «Portada»:
 * *React + MUI · createTheme + sx*). Sin esto cada componente tendría que
 * importar los tokens por separado y el tema sería solo decorativo; con esto
 * un `sx` puede leerlos del tema, que es la vía que MUI garantiza:
 *
 * ```tsx
 * <Box sx={(t) => ({ height: t.cts.density.navItem, borderRadius: `${t.cts.radii.control}px` })} />
 * ```
 *
 * La ruta `@mui/material/styles` es estable en MUI 6, 7 y 9, así que esta
 * augmentación vale para los tres majors del rango de `peerDependencies`.
 *
 * Es un módulo de solo tipos: no emite runtime. Importarlo por efecto
 * secundario (`import './mui/augmentation'`) o dejar que lo arrastre el
 * barrel de `src/index.ts`.
 */
import type { CtsTokens } from '../tokens'

declare module '@mui/material/styles' {
  interface Theme {
    /** Tokens del Sistema de Diseño CTS. Ver `src/tokens.ts`. */
    cts: CtsTokens
  }
  interface ThemeOptions {
    cts?: CtsTokens
  }
}

export {}

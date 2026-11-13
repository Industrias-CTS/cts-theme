/**
 * Canal de estado entre `AppShell` y sus slots.
 *
 * El rail, el header, los flotantes o cualquier vista dentro de `<AppShell>`
 * leen y cambian el estado del rail con `useAppShell()`, sin pasar props por
 * la cadena de componentes. Ver `docs/App-Shell.md` §3.
 *
 * Este módulo no emite estilos: solo estado. Por eso no está en la raíz
 * `src/index.ts`, que debe seguir libre de React.
 */
import { createContext, useContext } from 'react'

/** Modo efectivo del rail. `auto` se resuelve a uno de estos tres. */
export type ShellLayout = 'push' | 'overlay' | 'temporary'

/** Qué queda visible del rail cerrado: solo iconos (64) u oculto (0 + reapertura). */
export type RailCollapse = 'icons' | 'hidden'

export interface AppShellContextValue {
  railOpen: boolean
  setRailOpen: (open: boolean) => void
  toggleRail: () => void
  /** Modo resuelto (nunca `auto`). */
  layout: ShellLayout
  collapsedRail: RailCollapse
  /** ms que tarda el rail en cerrarse en el modo actual */
  closeMs: number
}

export const AppShellContext = createContext<AppShellContextValue | null>(null)

/**
 * Devuelve el estado del `<AppShell>` más cercano.
 *
 * Lanza error si se usa fuera de `<AppShell>`: sin proveedor no hay estado
 * que leer y el fallo debe verse en desarrollo, no en silencio.
 */
export const useAppShell = (): AppShellContextValue => {
  const ctx = useContext(AppShellContext)
  if (ctx === null) {
    throw new Error('useAppShell requiere <AppShell>')
  }
  return ctx
}

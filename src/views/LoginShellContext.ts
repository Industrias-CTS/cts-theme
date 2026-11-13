/**
 * Canal de estado entre `LoginShell` y sus slots.
 *
 * El formulario (o cualquier slot) que vive dentro de `<LoginShell>` lee y
 * cambia el estado con `useLoginShell()`, sin pasar props por la cadena de
 * componentes. Los estados siguen la propuesta de `docs/Login-Shell.md` §3.
 *
 * Este módulo no emite estilos: solo estado. Por eso no está en la raíz
 * `src/index.ts`, que debe seguir libre de React.
 */
import { createContext, useContext } from 'react'

/** Estado del inicio de sesión. `idle` es el reposo inicial. */
export type LoginStatus = 'idle' | 'submitting' | 'error' | 'success'

export interface LoginShellContextValue {
  status: LoginStatus
  setStatus: (status: LoginStatus) => void
}

export const LoginShellContext = createContext<LoginShellContextValue | null>(null)

/**
 * Devuelve `status` y `setStatus` del `<LoginShell>` más cercano.
 *
 * Lanza error si se usa fuera de `<LoginShell>`: sin proveedor no hay estado
 * que leer y el fallo debe verse en desarrollo, no en silencio.
 */
export const useLoginShell = (): LoginShellContextValue => {
  const ctx = useContext(LoginShellContext)
  if (ctx === null) {
    throw new Error('useLoginShell requiere <LoginShell>')
  }
  return ctx
}

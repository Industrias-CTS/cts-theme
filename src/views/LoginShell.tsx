/**
 * `LoginShell` — cascarón de la pantalla de acceso.
 *
 * Porta el layout de `AuthPage.tsx` de cts-manager: panel de marca a la
 * izquierda (oculto bajo `md`) y panel de formulario a la derecha. Los huecos
 * (logo, wordmark, leyenda, formulario…) son slots: cada aplicación pone su
 * contenido. Ver `docs/Login-Shell.md`.
 *
 * No hay animaciones (decisión L3, opción b). El estado se expone por
 * contexto (`useLoginShell`) y por el atributo `data-status` de la raíz.
 *
 * Colores siempre en `sx`, nunca con el prop `color` de `Typography`: MUI 9
 * lo tipa como `textSecondary` y descarta `'text.secondary'` sin avisar.
 */
import type { JSX, ReactNode } from 'react'
import { useCallback, useMemo, useState } from 'react'
import { Box, Typography } from '@mui/material'
import { authAutofill } from '../colors'
import '../mui/augmentation'
import { LoginShellContext } from './LoginShellContext'
import type { LoginShellContextValue, LoginStatus } from './LoginShellContext'

export interface LoginShellProps {
  /** Slot del logo (panel de marca). */
  logo?: ReactNode
  /** Wordmark del panel de marca. */
  brandName?: ReactNode
  /** Descriptor bajo el wordmark. */
  tagline?: ReactNode
  /** Leyenda al pie del panel de marca. */
  legend?: ReactNode
  /** Título sobre el formulario. */
  title?: ReactNode
  subtitle?: ReactNode
  /** Pie bajo el formulario. */
  footer?: ReactNode
  /** Slot del formulario. */
  children: ReactNode
  /** Estado controlado. */
  status?: LoginStatus
  /** Estado inicial no controlado. Por defecto `'idle'`. */
  defaultStatus?: LoginStatus
  onStatusChange?: (status: LoginStatus) => void
}

/** Un slot cuenta como presente salvo que sea vacío, nulo o booleano. */
const present = (node: ReactNode): boolean =>
  node !== undefined && node !== null && node !== false && node !== ''

/**
 * Autocompletado de Chrome en campos con `-webkit-autofill`.
 * AuthPage.tsx:18-24. La cadena es una receta CSS, no un color del tema.
 */
const autofillRule = {
  '& input:-webkit-autofill, & input:-webkit-autofill:hover, & input:-webkit-autofill:focus': {
    WebkitBoxShadow: '0 0 0 100px var(--autofill-bg) inset !important',
    WebkitTextFillColor: 'var(--autofill-text) !important',
    caretColor: 'var(--autofill-text) !important',
  },
}

export const LoginShell = ({
  logo,
  brandName,
  tagline,
  legend,
  title,
  subtitle,
  footer,
  children,
  status: statusProp,
  defaultStatus,
  onStatusChange,
}: LoginShellProps): JSX.Element => {
  const [internalStatus, setInternalStatus] = useState<LoginStatus>(defaultStatus ?? 'idle')
  const isControlled = statusProp !== undefined
  const status: LoginStatus = statusProp ?? internalStatus

  const setStatus = useCallback(
    (next: LoginStatus) => {
      if (!isControlled) setInternalStatus(next)
      onStatusChange?.(next)
    },
    [isControlled, onStatusChange],
  )

  const contextValue = useMemo<LoginShellContextValue>(
    () => ({ status, setStatus }),
    [status, setStatus],
  )

  const hasHeader = present(title) || present(subtitle)

  return (
    <LoginShellContext.Provider value={contextValue}>
      {/* AuthPage.tsx:60-68 — raíz: alto de viewport, fondo de aplicación y
          variables del autocompletado según el modo. */}
      <Box
        data-status={status}
        sx={(t) => {
          const autofill = authAutofill[t.palette.mode === 'dark' ? 'dark' : 'light']
          return {
            minHeight: '100vh',
            display: 'flex',
            bgcolor: 'background.default',
            '--autofill-bg': autofill.bg,
            '--autofill-text': autofill.text,
            ...autofillRule,
          }
        }}
      >
        {/* AuthPage.tsx:71-125 — panel de marca, oculto bajo md. */}
        <Box
          component="aside"
          sx={(t) => ({
            display: { xs: 'none', md: 'flex' },
            flex: `0 0 ${t.cts.login.brandPanelBasis}`,
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            bgcolor: t.palette.mode === 'dark' ? 'background.paper' : 'primary.main',
            color: 'primary.contrastText',
            p: 6,
            position: 'relative',
            overflow: 'hidden',
          })}
        >
          <Box sx={{ position: 'relative', textAlign: 'center' }}>
            {present(logo) && (
              <Box sx={{ mb: 3, display: 'flex', justifyContent: 'center' }}>{logo}</Box>
            )}

            {present(brandName) && (
              <Typography
                sx={(t) => ({
                  fontWeight: t.cts.fontWeight.black,
                  fontSize: t.cts.login.wordmarkSize,
                  letterSpacing: t.cts.login.wordmarkTracking,
                  lineHeight: 1,
                  mb: 1,
                })}
              >
                {brandName}
              </Typography>
            )}

            {present(tagline) && (
              <Typography
                sx={(t) => ({
                  fontSize: t.cts.login.taglineSize,
                  opacity: t.cts.login.taglineOpacity,
                  letterSpacing: t.cts.login.taglineTracking,
                  textTransform: 'uppercase',
                  mb: 5,
                })}
              >
                {tagline}
              </Typography>
            )}

            {present(legend) && (
              <Typography
                sx={(t) => ({
                  fontSize: t.cts.login.legendSize,
                  opacity: t.cts.login.legendOpacity,
                  mt: 5,
                  fontStyle: 'italic',
                })}
              >
                {legend}
              </Typography>
            )}
          </Box>
        </Box>

        {/* AuthPage.tsx:129-290 — panel de formulario. */}
        <Box
          component="main"
          sx={{
            flex: 1,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            p: { xs: 3, md: 6 },
          }}
        >
          {/* AuthPage.tsx:140 — columna del formulario, maxWidth 420. */}
          <Box
            sx={(t) => ({
              width: '100%',
              maxWidth: t.cts.login.formMaxWidth,
            })}
          >
            {hasHeader && (
              <Box sx={{ mb: 4 }}>
                {present(title) && (
                  <Typography
                    variant="h4"
                    component="h1"
                    sx={(t) => ({
                      fontWeight: t.cts.fontWeight.bold,
                      //? L4: `primary.main` sobre `background.default` oscuro da 2.1:1 (D14).
                      color: t.palette.mode === 'dark' ? 'text.primary' : 'primary.main',
                      mb: 0.5,
                    })}
                  >
                    {title}
                  </Typography>
                )}
                {present(subtitle) && (
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    {subtitle}
                  </Typography>
                )}
              </Box>
            )}

            {children}

            {/* L4: `text.disabled` da 2.65:1 en claro y 4.37:1 en oscuro; `text.secondary` pasa en ambos. */}
            {present(footer) && (
              <Typography
                variant="caption"
                sx={{ display: 'block', textAlign: 'center', mt: 5, color: 'text.secondary' }}
              >
                {footer}
              </Typography>
            )}
          </Box>
        </Box>
      </Box>
    </LoginShellContext.Provider>
  )
}

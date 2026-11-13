import type { JSX } from 'react'
import { Box } from '@mui/material'
import { useLoginShell } from '../src/views'

/**
 * Logo de ejemplo. Demuestra que un slot del consumidor puede reaccionar al
 * `status` compartido del shell: aquí pulsa solo mientras se envía el formulario.
 */
export function MockLogo(): JSX.Element {
  const { status } = useLoginShell()
  const submitting = status === 'submitting'

  return (
    <Box
      sx={{
        display: 'inline-flex',
        color: 'inherit',
        ...(submitting && {
          animation: 'mockPulse 1.2s ease-in-out infinite',
          '@media (prefers-reduced-motion: reduce)': { animation: 'none' },
        }),
        '@keyframes mockPulse': {
          '0%, 100%': { transform: 'scale(1)', opacity: 1 },
          '50%': { transform: 'scale(1.08)', opacity: 0.7 },
        },
      }}
    >
      <svg
        width={72}
        height={72}
        viewBox="0 0 72 72"
        role="img"
        aria-label="Logo de ejemplo"
      >
        <rect
          x={4}
          y={4}
          width={64}
          height={64}
          rx={16}
          fill="none"
          stroke="currentColor"
          strokeWidth={4}
        />
        <path
          d="M22 52 V24 L36 40 L50 24 V52"
          fill="none"
          stroke="currentColor"
          strokeWidth={5}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </Box>
  )
}

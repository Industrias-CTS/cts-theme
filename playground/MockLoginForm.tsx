import { useState } from 'react'
import type { FormEvent, JSX } from 'react'
import {
  Alert,
  Button,
  CircularProgress,
  IconButton,
  InputAdornment,
  TextField,
  Typography,
} from '@mui/material'
import EmailIcon from '@mui/icons-material/EmailOutlined'
import LockIcon from '@mui/icons-material/LockOutlined'
import VisibilityIcon from '@mui/icons-material/Visibility'
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff'
import { useLoginShell } from '../src/views'

const MOCK_FAIL_PASSWORD = 'error'
const MOCK_DELAY_MS = 1200

const wait = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms))

export function MockLoginForm(): JSX.Element {
  const { status, setStatus } = useLoginShell()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)

  const submitting = status === 'submitting'

  // Editar un campo limpia el error previo, como en el formulario real.
  const clearError = () => {
    if (status === 'error') setStatus('idle')
  }

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (submitting) return
    setStatus('submitting')
    await wait(MOCK_DELAY_MS)
    setStatus(password === MOCK_FAIL_PASSWORD ? 'error' : 'success')
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        {status === 'error' && (
          <Alert severity="error" sx={{ mb: 2.5, borderRadius: 2 }}>
            Credenciales incorrectas (mock). Usa cualquier otra contraseña.
          </Alert>
        )}
        {status === 'success' && (
          <Alert severity="success" sx={{ mb: 2.5, borderRadius: 2 }}>
            Sesión iniciada (mock).
          </Alert>
        )}

        <TextField
          label="Correo electrónico"
          type="email"
          fullWidth
          value={email}
          onChange={(e) => {
            setEmail(e.target.value)
            clearError()
          }}
          required
          autoComplete="email"
          sx={{ mb: 2 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <EmailIcon sx={{ fontSize: 18, color: 'text.secondary' }} />
                </InputAdornment>
              ),
            },
          }}
        />

        <TextField
          label="Contraseña"
          type={showPass ? 'text' : 'password'}
          fullWidth
          value={password}
          onChange={(e) => {
            setPassword(e.target.value)
            clearError()
          }}
          required
          autoComplete="current-password"
          sx={{ mb: 3 }}
          slotProps={{
            input: {
              startAdornment: (
                <InputAdornment position="start">
                  <LockIcon sx={{ fontSize: 18, color: 'text.secondary' }} />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    size="small"
                    edge="end"
                    aria-label={showPass ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                    onClick={() => setShowPass((v) => !v)}
                  >
                    {showPass ? (
                      <VisibilityOffIcon sx={{ fontSize: 18 }} />
                    ) : (
                      <VisibilityIcon sx={{ fontSize: 18 }} />
                    )}
                  </IconButton>
                </InputAdornment>
              ),
            },
          }}
        />

        <Button
          type="submit"
          variant="contained"
          fullWidth
          size="large"
          disabled={submitting}
          sx={(t) => ({ py: 1.4, fontSize: t.cts.fontSize.body, mb: 2 })}
        >
          {submitting ? <CircularProgress size={22} color="inherit" /> : 'Ingresar'}
        </Button>
      </form>

      <Typography variant="body2" sx={{ textAlign: 'center', color: 'text.secondary' }}>
        Mock: la contraseña «{MOCK_FAIL_PASSWORD}» simula un fallo.
      </Typography>
    </>
  )
}

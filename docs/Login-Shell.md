# `LoginShell` — propuesta

> **Estado:** L1 y L2 aprobadas (recomendadas). L3 pendiente: se implementa la
> opción (b), solo canal de estado sin animaciones por defecto.
> **Fuente:** `cts-manager/frontend/src/features/auth/AuthPage.tsx`
> (rama `production`, commit `7181d5d7`).

Primer componente compuesto de la librería. Es el cascarón de la pantalla de
acceso: aporta la estructura, el estilado y los patrones de `AuthPage`, y deja
huecos (*slots*) para lo que cambia entre aplicaciones: logo, leyenda y
formulario.

Nota: `Atomos.md` § «Fuera de alcance» deja los compuestos (login incluido)
para después de aprobar los átomos. Este componente se adelanta por pedido
explícito; no incluye overrides de átomos (botón, input). El formulario de
ejemplo usa MUI por defecto + el tema CTS.

---

## 1. Anatomía

```
┌──────── marca 45% (oculto < md) ────────┬────────── panel de formulario (flex 1) ──────┐
│  fondo primary.main / oscuro: #253662   │  fondo default / oscuro: #2A3547             │
│           [slot: logo]                  │      ┌─ maxWidth 420 ─────────┐              │
│           brandName (900, ls 4)         │      │ title (h4 700 primary) │              │
│           TAGLINE (13, α .7, ls 1)      │      │ subtitle (body2 muted) │              │
│                                         │      │ [slot: children]       │              │
│           [slot: legend] (12, α .45)    │      │ footer (caption)       │              │
│                                         │      └────────────────────────┘              │
└─────────────────────────────────────────┴──────────────────────────────────────────────┘
```

| Zona | Valor en AuthPage | Destino en cts-theme |
|---|---|---|
| raíz | `minHeight: 100vh`, flex | `sx` |
| panel de marca | `flex: 0 0 45%`, `p: 6`, oculto en `xs` | `tokens.login.brandPanelWidth` |
| fondo de marca | `#0065BB` / oscuro `#253662` | `primary.main` / `background.paper` |
| wordmark | 42px · 900 · ls 4 | `tokens.login.*` |
| tagline | 13px · opacidad .7 → **.85** (L4) · ls 1 | `tokens.login.*` |
| leyenda | 12px · opacidad .45 → **.85** (L4) · itálica · `mt: 5` | `tokens.login.*` |
| panel de formulario | `p: { xs: 3, md: 6 }`, oscuro `#2A3547` | `background.default` |
| columna del formulario | `maxWidth: 420` | `tokens.login.formMaxWidth` |
| título | h4 · 700 · `primary.main` (oscuro: **`text.primary`**, L4) | `typography.h4` |
| pie | caption · `text.disabled` → **`text.secondary`** (L4) · `mt: 5` | `typography.caption` |
| autocompletado | `--autofill-bg` `#e8f0fe` / `#253662`; `--autofill-text` `#1a1a1a` / `#fff` | `colors.authAutofill` |

---

## 2. API pública

```tsx
import { LoginShell, useLoginShell } from '@industriascts/cts-theme/views'

<LoginShell
  logo={<MiLogo />}                       // ReactNode
  brandName="W-Flow"                      // opcional
  tagline="Gestión de flujos de trabajo"  // opcional
  legend="Somos más, somos CTS."          // ReactNode
  title="Bienvenido"
  subtitle="Ingresa tus credenciales para continuar"
  footer={`© ${año} Industrias CTS · W-Flow`}
>
  <MiFormulario />                         // slot del formulario = children
</LoginShell>
```

El cascarón define las variables CSS `--autofill-bg` / `--autofill-text`; los
inputs del consumidor las heredan.

---

## 3. Canal de estado entre formulario y cascarón

Para que el consumidor pueda disparar animaciones dentro de `LoginShell` desde
su formulario.

**Mecanismo:** contexto provisto por `LoginShell` + prop controlado opcional
(patrón controlado/no controlado, igual que MUI).

```tsx
type LoginStatus = 'idle' | 'submitting' | 'error' | 'success'

// Dentro de MiFormulario (o del slot del logo), sin pasar props:
const { status, setStatus } = useLoginShell()
setStatus('submitting')
await login(...)          // → setStatus('success') | setStatus('error')

// O controlado desde el padre:
<LoginShell
  status={status}
  onAnimationDone={(s) => s === 'success' && navigate('/')}
>
```

### Reacción por defecto

Ninguna mientras L3 siga abierta (opción b). El cascarón solo publica el estado.

### Ganchos para animaciones propias

- `data-status` en la raíz: el `sx` del consumidor puede apuntar a
  `[data-status="error"] &`.
- Todo slot (logo, leyenda, formulario) puede leer `useLoginShell().status` y
  animarse solo. Ejemplo: un logo que late mientras se envía (lo hace el
  `MockLogo` del playground).
- Controlado: `status` + `onStatusChange`. No controlado: `defaultStatus`.

### Si L3 se aprueba como (a)

Cambio aditivo, sin romper la firma: reacción por defecto por estado
(`submitting` → pulso del logo · `error` → sacudida del formulario ·
`success` → el panel de marca se expande y cubre el formulario), prop
`animate={false}` para apagarla, `onAnimationDone(status)` para navegar al
terminar, `prefers-reduced-motion` respetado y `@keyframes` dentro de `sx`.

---

## 4. Archivos

| # | Archivo | Cambio |
|---|---|---|
| 1 | `src/tokens.ts` | grupo `login` (ancho de marca 45%, `formMaxWidth` 420, tamaños 42/13/12, opacidades .7/.45), con la línea de `AuthPage.tsx` como cita |
| 2 | `src/colors.ts` | primitivos `authAutofill` claro/oscuro; ningún literal en el componente |
| 3 | `src/views/LoginShell.tsx` | el cascarón; `sx` lee solo `theme.cts` y la paleta; retorno anotado (TS2742); sin `Grid` ni `slotProps` |
| 4 | `src/views/LoginShellContext.ts` | contexto + `useLoginShell` |
| 5 | `src/views/index.ts` | barrel de `/views` |
| 6 | `package.json` | export `./views`; script `dev`; devDeps `vite`, `@vitejs/plugin-react`, `@mui/icons-material` (solo playground) |
| 7 | `vite.config.ts` | `root: 'playground'` |
| 8 | `playground/` | `index.html`, `main.tsx` (ThemeProvider + conmutador claro/oscuro), `MockLogo.tsx` (SVG en línea), `MockLoginForm.tsx` (correo, contraseña, ojo, botón; login falso de 1.2 s: contraseña `error` → error, cualquier otra → éxito) |
| 9 | `smoke/` | prueba de `LoginShell` y `useLoginShell` para que `typecheck:matrix` los cubra en MUI 6, 7 y 9 |

**Terminado cuando:** `pnpm dev` muestra el login con logo y formulario de
ejemplo y el canal de estado en acción; `pnpm build` y `pnpm typecheck:matrix` en
verde.

---

## 5. Ejecución

Dos subagentes Haiku, revisados por el agente principal, con un máximo de 3
iteraciones:

- **A:** `LoginShell`, contexto, `tokens.login`, `authAutofill`, a partir de
  esta especificación.
- **B:** playground y formulario de ejemplo.

---

## 6. Fuera de alcance

- Decoraciones de temporada `Views.Login.emitEpoch` (`Filosofia.md`). Podrían
  usar más adelante el mismo canal de estado.
- Overrides de átomos de botón e input.
- Fondo oscuro del login `#1a1a2e` frente a `#2A3547`: decisión abierta en
  `Atomos.md`. Se usa `background.default` (`#2A3547`).

---

## 7. Decisiones pendientes

| # | Decisión | Opciones | Recomendación |
|---|---|---|---|
| L1 ✅ | Tipo de slot | (a) `ReactNode` + `children` · (b) props de tipo componente, como en `Filosofia.md` (`Form={MiForm} LogoSide={…}`) | (a): permite pasar props en línea |
| L2 ✅ | Nombre y ruta | (a) `LoginShell` desde `/views` · (b) `Views.Login` | (a) |
| L3 | Valores de animación (sacudida, pulso, expansión): no existen en cts-manager, AuthPage no anima | (a) reutilizar `motion.collapse` 0.25s y `motion.easing`, y agregar `motion.feedback` marcado «propuesto, no viene de cts-manager» · (b) sin animaciones por defecto; solo el canal y `data-status` | (a) |
| L4 ✅ | Contraste (axe, WCAG AA) de valores literales de AuthPage | (a) corregir en la librería: título en oscuro `primary.main` → `text.primary` (2.1:1, ya es D14 de `Atomos.md`); leyenda α .45 → .7 o más (2.37:1 sobre azul); tagline α .7 (3.69:1); pie `text.disabled` → `text.secondary` (2.65:1) · (b) mantener literales y documentar | (a); E-Panel arrastra el título oscuro y su e2e de accesibilidad solo corre en claro |

---

## 8. Hallazgos de la implementación

- **`Typography color="text.secondary"` no funciona en MUI 9.** Lo tipa como
  `textSecondary` y acepta cualquier `string`, así que `typecheck:matrix` no lo
  detecta y el texto sale en `text.primary`. Regla: colores siempre en `sx`
  (`sx={{ color: 'text.secondary' }}`), que vale en 6, 7 y 9.
- **Contraste.** axe sobre el playground: 1 regla (`color-contrast`) en claro
  y en oscuro, todas en valores del cascarón (ver L4). AuthPage tiene los
  mismos defectos.

## 9. E-Panel

Copia en `E-Panel/apps/web/src/shell/` (la app aún no consume el paquete):
mismo componente, tokens en `shell/tokens.ts` en lugar de `theme.cts`.
`pages/Login.tsx` lo usa con `logo`, `title`, `subtitle` y `status`
controlado (`loading` → `submitting`, error de formulario → `error`). Sin
`legend` ni `footer`: la página no los tenía y sus valores de contraste
romperían el e2e `a11y.spec.ts`. axe en `/login`: 0 violaciones en claro
(igual que antes); 1 en oscuro, el título (L4).

### L4 — aplicado (2026-11-06)

- **Leyenda y tagline:** opacidad del blanco `.45` / `.7` → **`.85`** en
  `tokens.login`. Blanco a `.83` es el mínimo que pasa sobre `#0065BB` (el
  blanco puro solo llega a 5.87:1), así que la jerarquía entre los dos sale
  del tamaño (12 / 13 px) y la itálica, no de la opacidad. Resultado:
  4.70:1 en claro, 8.99:1 en oscuro.
- **Pie:** `text.disabled` → **`text.secondary`** (4.99:1 en claro, 5.88:1 en
  oscuro). Rol existente, sin primitivos nuevos.
- **Título en oscuro:** `primary.main` → **`text.primary`** (D14 de
  `Atomos.md`). En claro sigue `primary.main` (5.4:1).
- Resultado: axe sin violaciones en el playground y en E-Panel `/login`, en
  claro y en oscuro.

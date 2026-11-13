// Lint de cts-theme con su propio preset: el paquete cumple las reglas que publica.
import tseslint from 'typescript-eslint'
import { ctsLint } from './eslint/index.js'

export default tseslint.config(
  { ignores: ['dist/**', 'docs/**', 'wireframes-epanel/**', 'node_modules/**', 'storybook-static/**'] },
  ...tseslint.configs.recommended,
  ...ctsLint(),
)

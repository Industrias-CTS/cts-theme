/**
 * Genera `dist/cts-theme.css` desde `src/css.ts`.
 *
 * Usa Vite para cargar el TypeScript tal cual (resuelve los imports sin
 * extensión), así la hoja nunca se desfasa de `colors.ts` y `tokens.ts`.
 */
import { mkdirSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createServer } from 'vite'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const out = resolve(root, 'dist/cts-theme.css')

const server = await createServer({
  root,
  configFile: false,
  logLevel: 'error',
  appType: 'custom',
  server: { middlewareMode: true, hmr: false },
  // Solo se carga un módulo en SSR: sin escaneo ni pre-bundling de dependencias.
  optimizeDeps: { noDiscovery: true, entries: [] },
})
try {
  const { cssText } = await server.ssrLoadModule('/src/css.ts')
  mkdirSync(dirname(out), { recursive: true })
  writeFileSync(out, cssText())
  console.log(`cts-theme: ${out}`)
} finally {
  await server.close()
}

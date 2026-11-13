import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import type { StorybookConfig } from '@storybook/react-vite'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')

/** Catálogo visual del Sistema de Diseño CTS. `pnpm catalogo`. */
const config: StorybookConfig = {
  framework: '@storybook/react-vite',
  stories: ['../catalogo/**/*.mdx', '../catalogo/**/*.stories.tsx'],
  addons: ['@storybook/addon-docs', '@storybook/addon-themes'],
  core: { disableTelemetry: true },
  // `vite.config.ts` apunta al playground; el catálogo usa la raíz del repo.
  viteFinal: (vite) => ({ ...vite, root }),
}

export default config

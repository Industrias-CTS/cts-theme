import type { Preview } from '@storybook/react-vite'
import { CssBaseline, ThemeProvider } from '@mui/material'
import { withThemeFromJSXProvider } from '@storybook/addon-themes'
import { createCtsTheme } from '../src/index'
import { NotificationHost } from '../src/views'

/** Los temas que puede elegir el catálogo desde la barra superior. */
const themes = {
  Claro: createCtsTheme('light'),
  Oscuro: createCtsTheme('dark'),
  'HMI oscuro': createCtsTheme('dark', { profile: 'hmi' }),
  'HMI claro': createCtsTheme('light', { profile: 'hmi' }),
}

const preview: Preview = {
  decorators: [
    // El primero queda más adentro: los avisos leen el tema.
    (Story) => (
      <NotificationHost>
        <Story />
      </NotificationHost>
    ),
    withThemeFromJSXProvider({
      themes,
      defaultTheme: 'Claro',
      Provider: ThemeProvider,
      GlobalStyles: CssBaseline,
    }),
  ],
  parameters: {
    layout: 'padded',
    controls: { expanded: true },
    options: {
      storySort: {
        order: [
          'Inicio',
          'Fundamentos',
          ['Colores', 'Tipografía', 'Forma y espacio', 'Capas y movimiento', 'Formato'],
          'Componentes MUI',
          'Componentes CTS',
        ],
      },
    },
  },
}

export default preview


Los componentes se usan directamente de la librería sin cambiar de estilos.

Los valores de colores, o sea, primitivos, solo deben definirse en un archivo `colors.ts`que pueda sobre escribir el tema si es necesario, y de forma global o local.

Los valores primitivos directos no están permitidos.
Los estilos 'in-line' no se deben usar, a no ser de que el componente no se encuentre en la librería, e incluso dado del caso, se puede proponer una inclusión en la librería o estilarlo como el siguiente puntos

Los componentes con estilos únicos, deben usar los colores a través de roles.

Los componentes (átomos) propios por proyecto no deben superar la cantidad de componentes importados.

Los componentes compuestos, permiten insertar otros componentes, a manera de _props_, en los lugares que pueden variar de aplicación a aplicación, como el logo, el estilo del formulario y sus campos.

```tsx

export const AppLogin (): React.JSX.Element => (<Views.Login Form={MyForm} LogoSide={LogoSide}>)

```

![Temporadas] Si decides utilizar decoraciones por épocas del año actívalo con: `Views.Login.emitEpoch`

### 'Features' de MUI no usadas y no recomendadas por la librería

| Prohibido | Motivo |
|---|---|
| `Grid` de MUI | renombrado en 7 (`Grid2`→`Grid`); `GridLegacy` eliminado en 9. Usar flex/grid CSS |
| `componentsProps` / `slotProps` | consolidados en 7. Exponer props propias explícitas, no reenviar slots. |
| imports profundos de 2.º nivel (`@mui/material/Button/Button`) | eliminados en 7. Importar desde la raíz. |
| `extendTheme` · `CssVarsProvider` · `theme.vars` | movidos/fusionados entre majors. Leer de `theme.cts`, no de `theme.vars`. |

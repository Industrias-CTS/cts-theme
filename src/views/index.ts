/**
 * Barrel del subpath `@industriascts/cts-theme/views`.
 *
 * Aquí vive todo lo que depende de React. La raíz `src/index.ts` no lo
 * reexporta a propósito: tokens, colores y tema deben poder usarse sin React.
 */
export { LoginShell } from './LoginShell'
export type { LoginShellProps } from './LoginShell'
export { LoginShellContext, useLoginShell } from './LoginShellContext'
export type { LoginStatus, LoginShellContextValue } from './LoginShellContext'
export { AppShell } from './AppShell'
export type { AppShellProps } from './AppShell'
export { AppShellContext, useAppShell } from './AppShellContext'
export type { AppShellContextValue, ShellLayout, RailCollapse } from './AppShellContext'

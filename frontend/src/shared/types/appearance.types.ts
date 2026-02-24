/**
 * Базовые варианты оформления
 */
export const BASE_APPEARANCES = [
  'primary',
  'secondary',
  'info',
  'success',
  'warning',
  'error',
  'light',
  'dark'
] as const
export type TypeBaseAppearance = (typeof BASE_APPEARANCES)[number]

/**
 * Базовые варианты размеров
 */
export const BASE_SIZES = ['sm', 'md', 'lg', 'xl'] as const
export type TypeBaseSize = (typeof BASE_SIZES)[number]

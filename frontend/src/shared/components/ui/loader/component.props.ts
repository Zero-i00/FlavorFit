import type { ComponentProps } from 'react'

import type { TypeBaseAppearance, TypeBaseSize } from '@/shared/types/appearance.types'

/**
 * Свойства компонента Loader
 */
export interface LoaderProps extends ComponentProps<'output'> {
  /**
   * Размер загрузчика
   *
   * @remarks
   * Определяет размер индикатора загрузки из предопределенного набора значений
   *
   * @default 'md'
   */
  size?: TypeBaseSize

  /**
   * Цветовое оформление загрузчика
   *
   * @remarks
   * Определяет цветовую схему индикатора загрузки (primary, success, warning, error и т.д.)
   *
   * @default 'primary'
   */
  appearance?: TypeBaseAppearance
}

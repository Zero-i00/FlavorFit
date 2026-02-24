import type { ComponentProps } from 'react'

import type { TypeBaseAppearance, TypeBaseSize } from '@/shared/types/appearance.types'

/**
 * Варианты стиля кнопки
 *
 * - `default` - Основной стиль с заливкой
 * - `label` - Стиль для меток и тегов
 * - `outline` - Контурный стиль без заливки
 * - `text` - Текстовый стиль без рамки и фона
 * - `icon` - Квадратная кнопка для иконок без текста
 */
type ButtonVariant = 'default' | 'outline' | 'text' | 'icon'

export interface ButtonProps extends ComponentProps<'button'> {
  /**
   * Состояние загрузки
   *
   * @remarks
   * Когда включено, кнопка становится неактивной и может отображать индикатор загрузки
   *
   * @default false
   */
  isLoading?: boolean

  /**
   * Размер кнопки
   *
   * @remarks
   * Определяет размер кнопки из предопределенного набора значений
   *
   * @default 'md'
   */
  size?: TypeBaseSize

  /**
   * Вариант стиля кнопки
   *
   * @remarks
   * Определяет визуальное оформление кнопки (заливка, контур, текст и т.д.)
   *
   * @default 'default'
   */
  variant?: ButtonVariant

  /**
   * Цветовое оформление кнопки
   *
   * @remarks
   * Определяет цветовую схему кнопки (primary, success, warning, error и т.д.)
   *
   * @default 'primary'
   */
  appearance?: TypeBaseAppearance
}

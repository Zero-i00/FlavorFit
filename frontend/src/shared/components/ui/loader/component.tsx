import styles from './component.module.css'
import type { LoaderProps } from './component.props'
import cn from 'clsx'
import { LoaderCircle } from 'lucide-react'

/**
 * Компонент индикатора загрузки
 *
 * @description
 * Компонент Loader предоставляет визуальный индикатор загрузки с анимацией.
 * Поддерживает различные размеры и цветовые схемы. Полностью доступен для screen readers
 * через ARIA атрибуты (role="status", aria-live="polite").
 *
 * @param {LoaderProps} props - Свойства компонента
 * @param {'sm' | 'md' | 'lg' | 'xl'} [props.size='md'] - Размер загрузчика
 * @param {'primary' | 'secondary' | 'info' | 'success' | 'warning' | 'error'} [props.appearance='primary'] - Цветовое оформление
 * @param {string} [props.className] - Дополнительные CSS классы
 *
 * @example
 * <Loader size="md" appearance="primary" />
 */

export function Loader({ size = 'md', appearance = 'primary', className, ...rest }: LoaderProps) {
  return (
    <output
      className={cn(styles.loader, styles[`loader--${appearance}`], styles[`loader--${size}`], className)}
      aria-live="polite"
      aria-label="Загрузка"
      {...rest}
    >
      <LoaderCircle className={styles.loader__icon} />
    </output>
  )
}

import styles from './component.module.css'
import type { InputProps } from './component.props'
import cn from 'clsx'
import { type Ref, forwardRef } from 'react'

import { Loader } from '@/shared/components/ui/loader'

/**
 * Универсальный компонент текстового поля ввода с поддержкой различных состояний
 *
 * @description
 * Компонент Input предоставляет гибкую систему для создания полей ввода с поддержкой:
 * - Состояний валидации (error, success)
 * - Иконок слева и справа от поля
 * - Состояния загрузки с индикатором
 *
 * @param {InputProps} props - Свойства компонента
 * @param {'sm' | 'md' | 'lg' | 'xl'} [props.size='md'] - Размер поля ввода
 * @param {string} [props.placeholder] - Текст placeholder
 * @param {boolean} [props.required=false] - Обязательное поле (добавляет * к placeholder)
 * @param {boolean} [props.disabled=false] - Отключенное состояние
 * @param {string} [props.error] - Текст ошибки валидации
 * @param {string} [props.success] - Текст успешной валидации
 * @param {string} [props.hint] - Подсказка под полем
 * @param {boolean} [props.isLoading=false] - Состояние загрузки
 * @param {ReactNode} [props.leftIcon] - Иконка слева
 * @param {ReactNode} [props.rightIcon] - Иконка справа
 * @param {Ref<HTMLInputElement>} ref - React ref для доступа к DOM элементу input
 *
 * @example
 * <Input
 *   type="email"
 *   placeholder="Email"
 *   required
 * />
 */
function InputInner(
  {
    id,
    type,
    hint,
    error,
    success,
    LeftComponent,
    RightComponent,
    container,
    className,
    placeholder,
    size = 'sm',
    disabled = false,
    required = false,
    isLoading = false,
    ...rest
  }: InputProps,
  ref: Ref<HTMLInputElement>
) {
  const label = required ? `${placeholder} *` : placeholder

  return (
    <div
      {...container}
      className={cn(styles.container, container?.className)}
    >
      <div
        className={cn(
          styles.input__wrapper,
          styles[`input__wrapper--${size}`],
          error && styles['input__wrapper--error'],
          success && styles['input__wrapper--success']
        )}
      >
        {LeftComponent}
        <input
          id={id}
          ref={ref}
          type={type}
          data-slot="input"
          aria-label={label}
          required={required}
          placeholder={label}
          aria-invalid={!!error}
          aria-describedby={hint}
          aria-disabled={disabled}
          disabled={disabled || isLoading}
          data-success={!!success}
          className={cn(styles.input, className)}
          {...rest}
        />
        {isLoading && <Loader size={'sm'} />}
        {!isLoading && RightComponent}
      </div>
      {hint && <p className={styles.input__hint}>{hint}</p>}
      {error && <p className={styles.input__error}>{error}</p>}
      {success && <p className={styles.input__success}>{success}</p>}
    </div>
  )
}

export const Input = forwardRef<HTMLInputElement, InputProps>(InputInner)
Input.displayName = 'Input'

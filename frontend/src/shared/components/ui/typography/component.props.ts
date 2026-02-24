import type { HTMLAttributes } from 'react'

/**
 * Тип для всех доступных вариантов типографики
 */
export type TypographyVariant =
	| 'h1'
	| 'h2'
	| 'h3'
	| 'h4'
	| 'h5'
	| 'h6'
	| 'subtitle-1'
	| 'subtitle-2'
	| 'body-1'
	| 'body-2'
	| 'caption'
	| 'overline'

/**
 * Свойства компонента Typography
 */
export interface TypographyProps extends HTMLAttributes<HTMLElement> {
	/**
	 * Вариант типографики (размер, вес шрифта, межстрочный интервал)
	 *
	 * @remarks
	 * Определяет стиль текста на основе design tokens из sizes.css
	 */
	variant: TypographyVariant
}

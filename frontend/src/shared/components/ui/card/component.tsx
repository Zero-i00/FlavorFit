import styles from './component.module.css'
import { cn } from '@/shared/utils'
import * as React from 'react'

import { Typography, type TypographyProps } from '@/shared/components/ui/typography'

function Card({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="card"
      className={cn(styles.card, className)}
      {...props}
    />
  )
}

function CardHeader({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="card-header"
      className={cn(styles['card-header'], className)}
      {...props}
    />
  )
}

function CardTitle({ variant = 'h4', ...rest }: Partial<TypographyProps>) {
  return (
    <Typography
      data-slot="card-title"
      variant={variant}
      {...rest}
    />
  )
}

function CardDescription({ variant = 'body-1', ...rest }: Partial<TypographyProps>) {
  return (
    <Typography
      data-slot="card-description"
      variant={variant}
      {...rest}
    />
  )
}

function CardAction({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="card-action"
      className={cn(styles['card-action'], className)}
      {...props}
    />
  )
}

function CardContent({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="card-content"
      className={cn(styles['card-content'], className)}
      {...props}
    />
  )
}

function CardFooter({ className, ...props }: React.ComponentProps<'div'>) {
  return (
    <div
      data-slot="card-footer"
      className={cn(styles['card-footer'], className)}
      {...props}
    />
  )
}

export { Card, CardHeader, CardFooter, CardTitle, CardAction, CardDescription, CardContent }

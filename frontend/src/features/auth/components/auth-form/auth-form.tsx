'use client'

import type { ComponentProps } from 'react'

import type { AuthFormType } from '@/features/auth/components/auth-form/auth-form.props'

interface Props extends ComponentProps<'div'> {
  type: AuthFormType
}

export function AuthForm({ type, className, ...rest }: Props) {
  return (
    <div {...rest}>
      <h1>{type === 'login' ? 'Login' : 'Register'}</h1>

      <form action="">
        <input type="email" />
        <input type="password" />
        <button type={'submit'}>Submit</button>
      </form>
    </div>
  )
}

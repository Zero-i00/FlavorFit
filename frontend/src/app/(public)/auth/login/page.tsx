import type { Metadata } from 'next'

import { LoginForm } from '@/features/auth/components/login-form'

import { NO_INDEX_PAGE } from '@/shared/constants/seo.constants'

export const metadata: Metadata = {
  title: 'Login',
  ...NO_INDEX_PAGE
}

export default function LoginPage() {
  return <LoginForm className={`min-w-1/3`} />
}

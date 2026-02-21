import type { Metadata } from 'next'

import { AuthForm } from '@/features/auth/components/auth-form'

import { NO_INDEX_PAGE } from '@/shared/constants/seo.constants'

export const metadata: Metadata = {
  title: 'Login',
  ...NO_INDEX_PAGE
}

export default function LoginPage() {
  return <AuthForm type={'login'} />
}

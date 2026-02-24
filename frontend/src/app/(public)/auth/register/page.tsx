import type { Metadata } from 'next'

import { RegisterForm } from '@/features/auth/components/register-form'

import { NO_INDEX_PAGE } from '@/shared/constants/seo.constants'

export const metadata: Metadata = {
  title: 'Register',
  ...NO_INDEX_PAGE
}

export default function RegisterPage() {
  return <RegisterForm className={`min-w-1/3`} />
}

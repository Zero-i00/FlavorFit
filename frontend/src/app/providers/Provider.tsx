'use client'

import { ApolloProvider } from '@apollo/client/react'
import type { PropsWithChildren } from 'react'
import { Toaster } from 'react-hot-toast'

import { getApolloClient } from '@/shared/api/apollo.client'

const apollo = getApolloClient()

export function Provider({ children }: PropsWithChildren) {
  return (
    <ApolloProvider client={apollo}>
      {children}
      <Toaster position={'top-right'} />
    </ApolloProvider>
  )
}

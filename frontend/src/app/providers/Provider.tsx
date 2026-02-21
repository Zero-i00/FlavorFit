'use client'

import { ApolloProvider } from '@apollo/client/react'
import type { PropsWithChildren } from 'react'

import { getApolloClient } from '@/shared/api/apollo.client'

const apollo = getApolloClient()

export function Provider({ children }: PropsWithChildren) {
  return <ApolloProvider client={apollo}>{children}</ApolloProvider>
}

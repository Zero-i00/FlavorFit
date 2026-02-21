import { ApolloClient, ApolloLink, HttpLink, InMemoryCache } from '@apollo/client'

import { GRAPHQL_SERVER_URL } from '@/shared/config/api.config'

import { IS_CLIENT } from '@/shared/constants/app.constants'

const url = new HttpLink({
  uri: GRAPHQL_SERVER_URL,
  credentials: 'include',
  fetchOptions: {
    next: {
      revalidate: 60
    }
  }
})

const apolloClient = new ApolloClient({
  link: ApolloLink.from([url]),
  devtools: {
    enabled: process.env.NODE_ENV === 'development'
  },
  cache: new InMemoryCache()
})

const apolloServer = new ApolloClient({
  ssrMode: true,
  link: ApolloLink.from([url]),
  devtools: {
    enabled: process.env.NODE_ENV === 'development'
  },
  cache: new InMemoryCache(),
  defaultOptions: {
    query: {
      fetchPolicy: 'no-cache'
    }
  }
})

export function getApolloClient() {
  return IS_CLIENT ? apolloClient : apolloServer
}

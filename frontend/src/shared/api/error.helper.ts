import { CombinedGraphQLErrors } from '@apollo/client'

export function extractError(error: Error): string[] {
  if (error instanceof CombinedGraphQLErrors) {
    return error.errors.map((e) => e.message.slice(4))
  }

  return [error.message]
}

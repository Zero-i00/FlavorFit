/* eslint-disable */
import type { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core'

export type Maybe<T> = T | null
export type InputMaybe<T> = T | null | undefined
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] }
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> }
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> }
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never }
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never }
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string }
  String: { input: string; output: string }
  Boolean: { input: boolean; output: boolean }
  Int: { input: number; output: number }
  Float: { input: number; output: number }
  /** Represents NULL values */
  Void: { input: any; output: any }
}

export const ActivityLevelEnum = {
  Active: 'ACTIVE',
  Light: 'LIGHT',
  Moderate: 'MODERATE',
  Sedentary: 'SEDENTARY',
  VeryActive: 'VERY_ACTIVE'
} as const

export type ActivityLevelEnum = (typeof ActivityLevelEnum)[keyof typeof ActivityLevelEnum]
export type AuthInput = {
  email: Scalars['String']['input']
  password: Scalars['String']['input']
}

export type AuthMutation = {
  __typename?: 'AuthMutation'
  login: AuthOutput
  logout?: Maybe<Scalars['Void']['output']>
  register: AuthOutput
}

export type AuthMutationLoginArgs = {
  data: AuthInput
}

export type AuthMutationRegisterArgs = {
  data: AuthInput
}

export type AuthOutput = {
  __typename?: 'AuthOutput'
  accessToken: Scalars['String']['output']
  tokenType: TokenType
  user: UserOutput
}

export type AuthQuery = {
  __typename?: 'AuthQuery'
  refreshToken: AuthOutput
}

export type BodyParameterInput = {
  activityLevel?: InputMaybe<ActivityLevelEnum>
  armCm?: InputMaybe<Scalars['Float']['input']>
  chestCm?: InputMaybe<Scalars['Float']['input']>
  goalWeightKg?: InputMaybe<Scalars['Float']['input']>
  heightCm?: InputMaybe<Scalars['Float']['input']>
  nutritionGoal?: InputMaybe<NutritionGoalEnum>
  thighCm?: InputMaybe<Scalars['Float']['input']>
  waistCm?: InputMaybe<Scalars['Float']['input']>
  weightKg?: InputMaybe<Scalars['Float']['input']>
}

export type BodyParameterOutput = {
  __typename?: 'BodyParameterOutput'
  activityLevel: ActivityLevelEnum
  armCm?: Maybe<Scalars['Float']['output']>
  chestCm?: Maybe<Scalars['Float']['output']>
  goalWeightKg?: Maybe<Scalars['Float']['output']>
  heightCm?: Maybe<Scalars['Float']['output']>
  id: Scalars['Int']['output']
  nutritionGoal: NutritionGoalEnum
  thighCm?: Maybe<Scalars['Float']['output']>
  userId: Scalars['Int']['output']
  waistCm?: Maybe<Scalars['Float']['output']>
  weightKg?: Maybe<Scalars['Float']['output']>
}

export type CommentInput = {
  content: Scalars['String']['input']
  recipeId: Scalars['Int']['input']
}

export type CommentMutation = {
  __typename?: 'CommentMutation'
  create: CommentOutput
  destroy: Scalars['Boolean']['output']
  update: CommentOutput
}

export type CommentMutationCreateArgs = {
  obj: CommentInput
}

export type CommentMutationDestroyArgs = {
  commentId: Scalars['Int']['input']
}

export type CommentMutationUpdateArgs = {
  commentId: Scalars['Int']['input']
  obj: CommentUpdate
}

export type CommentOutput = {
  __typename?: 'CommentOutput'
  author: UserOutput
  authorId: Scalars['Int']['output']
  content: Scalars['String']['output']
  id: Scalars['Int']['output']
  recipeId: Scalars['Int']['output']
}

export type CommentQuery = {
  __typename?: 'CommentQuery'
  list: Array<CommentOutput>
  retrieve: CommentOutput
}

export type CommentQueryRetrieveArgs = {
  commentId: Scalars['Int']['input']
}

export type CommentUpdate = {
  content?: InputMaybe<Scalars['String']['input']>
}

export type FavoriteInput = {
  recipeId: Scalars['Int']['input']
}

export type FavoriteMutation = {
  __typename?: 'FavoriteMutation'
  create: FavoriteOutput
  destroy: Scalars['Boolean']['output']
}

export type FavoriteMutationCreateArgs = {
  obj: FavoriteInput
}

export type FavoriteMutationDestroyArgs = {
  recipeId: Scalars['Int']['input']
}

export type FavoriteOutput = {
  __typename?: 'FavoriteOutput'
  author: UserOutput
  authorId: Scalars['Int']['output']
  id: Scalars['Int']['output']
  recipeId: Scalars['Int']['output']
}

export type FavoriteQuery = {
  __typename?: 'FavoriteQuery'
  list: Array<FavoriteOutput>
}

export const GenderEnum = {
  Female: 'FEMALE',
  Male: 'MALE'
} as const

export type GenderEnum = (typeof GenderEnum)[keyof typeof GenderEnum]
export type IngredientInput = {
  description: Scalars['String']['input']
  icon: Scalars['String']['input']
  initialUnit: IngredientUnitEnum
  name: Scalars['String']['input']
  price: Scalars['Float']['input']
}

export type IngredientMutation = {
  __typename?: 'IngredientMutation'
  create: IngredientOutput
  destroy: Scalars['Boolean']['output']
  update: IngredientOutput
}

export type IngredientMutationCreateArgs = {
  obj: IngredientInput
}

export type IngredientMutationDestroyArgs = {
  ingredientId: Scalars['Int']['input']
}

export type IngredientMutationUpdateArgs = {
  ingredientId: Scalars['Int']['input']
  obj: IngredientUpdate
}

export type IngredientOutput = {
  __typename?: 'IngredientOutput'
  description: Scalars['String']['output']
  icon: Scalars['String']['output']
  id: Scalars['Int']['output']
  initialUnit: IngredientUnitEnum
  name: Scalars['String']['output']
  price: Scalars['Float']['output']
}

export type IngredientQuery = {
  __typename?: 'IngredientQuery'
  list: Array<IngredientOutput>
  retrieve: IngredientOutput
}

export type IngredientQueryRetrieveArgs = {
  ingredientId: Scalars['Int']['input']
}

export const IngredientUnitEnum = {
  Cloves: 'CLOVES',
  Gram: 'GRAM',
  Milliliter: 'MILLILITER',
  Piece: 'PIECE',
  Tablespoon: 'TABLESPOON',
  Teaspoon: 'TEASPOON'
} as const

export type IngredientUnitEnum = (typeof IngredientUnitEnum)[keyof typeof IngredientUnitEnum]
export type IngredientUpdate = {
  description?: InputMaybe<Scalars['String']['input']>
  icon?: InputMaybe<Scalars['String']['input']>
  initialUnit?: InputMaybe<IngredientUnitEnum>
  name?: InputMaybe<Scalars['String']['input']>
  price?: InputMaybe<Scalars['Float']['input']>
}

export type Mutation = {
  __typename?: 'Mutation'
  auth: AuthMutation
  recipes: RecipeMutation
  users: UserMutation
}

export const NutritionGoalEnum = {
  Maintenance: 'MAINTENANCE',
  MuscleGain: 'MUSCLE_GAIN',
  WeightLoss: 'WEIGHT_LOSS'
} as const

export type NutritionGoalEnum = (typeof NutritionGoalEnum)[keyof typeof NutritionGoalEnum]
export type ProfileOutput = {
  __typename?: 'ProfileOutput'
  age?: Maybe<Scalars['Int']['output']>
  bio?: Maybe<Scalars['String']['output']>
  fullName: Scalars['String']['output']
  gender?: Maybe<GenderEnum>
  id: Scalars['Int']['output']
  userId: Scalars['Int']['output']
}

export type ProfileUpdate = {
  age?: InputMaybe<Scalars['Int']['input']>
  bio?: InputMaybe<Scalars['String']['input']>
  fullName?: InputMaybe<Scalars['String']['input']>
  gender?: InputMaybe<GenderEnum>
}

export type Query = {
  __typename?: 'Query'
  auth: AuthQuery
  recipes: RecipeQuery
  users: UserQuery
}

export type RecipeCookStepOutput = {
  __typename?: 'RecipeCookStepOutput'
  description: Scalars['String']['output']
  id: Scalars['Int']['output']
  order: Scalars['Int']['output']
  recipeId: Scalars['Int']['output']
  title: Scalars['String']['output']
}

export const RecipeDifficultyEnum = {
  Easy: 'EASY',
  Hard: 'HARD',
  Medium: 'MEDIUM'
} as const

export type RecipeDifficultyEnum = (typeof RecipeDifficultyEnum)[keyof typeof RecipeDifficultyEnum]
export type RecipeIngredientOutput = {
  __typename?: 'RecipeIngredientOutput'
  id: Scalars['Int']['output']
  ingredientId: Scalars['Int']['output']
  quantity: Scalars['Float']['output']
  recipeId: Scalars['Int']['output']
  unit: IngredientUnitEnum
}

export type RecipeMutation = {
  __typename?: 'RecipeMutation'
  comments: CommentMutation
  favorites: FavoriteMutation
  ingredients: IngredientMutation
}

export type RecipeOutput = {
  __typename?: 'RecipeOutput'
  author: UserOutput
  authorId: Scalars['Int']['output']
  calories: Scalars['Float']['output']
  carbs: Scalars['Float']['output']
  cookTime: Scalars['Int']['output']
  description: Scalars['String']['output']
  difficulty: RecipeDifficultyEnum
  fats: Scalars['Float']['output']
  id: Scalars['Int']['output']
  ingredients: Array<RecipeIngredientOutput>
  prepareTime: Scalars['Int']['output']
  proteins: Scalars['Float']['output']
  servingTime: Scalars['Int']['output']
  slug: Scalars['String']['output']
  steps: Array<RecipeCookStepOutput>
  title: Scalars['String']['output']
  type: RecipeTypeEnum
}

export type RecipeQuery = {
  __typename?: 'RecipeQuery'
  comments: CommentQuery
  favorites: FavoriteQuery
  getBySlug?: Maybe<RecipeOutput>
  ingredients: IngredientQuery
  list: Array<RecipeOutput>
  retrieve?: Maybe<RecipeOutput>
}

export type RecipeQueryGetBySlugArgs = {
  slug: Scalars['String']['input']
}

export type RecipeQueryRetrieveArgs = {
  id: Scalars['Int']['input']
}

export const RecipeTypeEnum = {
  Bakery: 'BAKERY',
  ColdAppetizers: 'COLD_APPETIZERS',
  Dessert: 'DESSERT',
  Drink: 'DRINK',
  First: 'FIRST',
  HotAppetizers: 'HOT_APPETIZERS',
  Salad: 'SALAD',
  Second: 'SECOND',
  Starter: 'STARTER'
} as const

export type RecipeTypeEnum = (typeof RecipeTypeEnum)[keyof typeof RecipeTypeEnum]
export const RoleEnum = {
  Admin: 'ADMIN',
  User: 'USER'
} as const

export type RoleEnum = (typeof RoleEnum)[keyof typeof RoleEnum]
export const TokenType = {
  Bearer: 'BEARER'
} as const

export type TokenType = (typeof TokenType)[keyof typeof TokenType]
export type UserMutation = {
  __typename?: 'UserMutation'
  update: UserOutput
}

export type UserMutationUpdateArgs = {
  obj: UserUpdate
  userId: Scalars['Int']['input']
}

export type UserOutput = {
  __typename?: 'UserOutput'
  email: Scalars['String']['output']
  id: Scalars['Int']['output']
  isActive: Scalars['Boolean']['output']
  parameters?: Maybe<BodyParameterOutput>
  profile?: Maybe<ProfileOutput>
  role: RoleEnum
}

export type UserQuery = {
  __typename?: 'UserQuery'
  comments: Array<CommentOutput>
  favorites: Array<FavoriteOutput>
  getByEmail?: Maybe<UserOutput>
  list: Array<UserOutput>
  profile: UserOutput
  recipes: Array<RecipeOutput>
  retrieve: UserOutput
}

export type UserQueryCommentsArgs = {
  userId: Scalars['Int']['input']
}

export type UserQueryGetByEmailArgs = {
  email: Scalars['String']['input']
}

export type UserQueryRecipesArgs = {
  userId: Scalars['Int']['input']
}

export type UserQueryRetrieveArgs = {
  userId: Scalars['Int']['input']
}

export type UserUpdate = {
  email?: InputMaybe<Scalars['String']['input']>
  parameters?: InputMaybe<BodyParameterInput>
  password?: InputMaybe<Scalars['String']['input']>
  profile?: InputMaybe<ProfileUpdate>
}

export type LoginMutationVariables = Exact<{
  data: AuthInput
}>

export type LoginMutation = {
  __typename?: 'Mutation'
  auth: {
    __typename?: 'AuthMutation'
    login: { __typename?: 'AuthOutput'; accessToken: string; user: { __typename?: 'UserOutput'; email: string } }
  }
}

export type RegisterMutationVariables = Exact<{
  data: AuthInput
}>

export type RegisterMutation = {
  __typename?: 'Mutation'
  auth: {
    __typename?: 'AuthMutation'
    register: { __typename?: 'AuthOutput'; accessToken: string; user: { __typename?: 'UserOutput'; email: string } }
  }
}

export const LoginDocument = {
  kind: 'Document',
  definitions: [
    {
      kind: 'OperationDefinition',
      operation: 'mutation',
      name: { kind: 'Name', value: 'Login' },
      variableDefinitions: [
        {
          kind: 'VariableDefinition',
          variable: { kind: 'Variable', name: { kind: 'Name', value: 'data' } },
          type: { kind: 'NonNullType', type: { kind: 'NamedType', name: { kind: 'Name', value: 'AuthInput' } } }
        }
      ],
      selectionSet: {
        kind: 'SelectionSet',
        selections: [
          {
            kind: 'Field',
            name: { kind: 'Name', value: 'auth' },
            selectionSet: {
              kind: 'SelectionSet',
              selections: [
                {
                  kind: 'Field',
                  name: { kind: 'Name', value: 'login' },
                  arguments: [
                    {
                      kind: 'Argument',
                      name: { kind: 'Name', value: 'data' },
                      value: { kind: 'Variable', name: { kind: 'Name', value: 'data' } }
                    }
                  ],
                  selectionSet: {
                    kind: 'SelectionSet',
                    selections: [
                      {
                        kind: 'Field',
                        name: { kind: 'Name', value: 'user' },
                        selectionSet: {
                          kind: 'SelectionSet',
                          selections: [{ kind: 'Field', name: { kind: 'Name', value: 'email' } }]
                        }
                      },
                      { kind: 'Field', name: { kind: 'Name', value: 'accessToken' } }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    }
  ]
} as unknown as DocumentNode<LoginMutation, LoginMutationVariables>
export const RegisterDocument = {
  kind: 'Document',
  definitions: [
    {
      kind: 'OperationDefinition',
      operation: 'mutation',
      name: { kind: 'Name', value: 'Register' },
      variableDefinitions: [
        {
          kind: 'VariableDefinition',
          variable: { kind: 'Variable', name: { kind: 'Name', value: 'data' } },
          type: { kind: 'NonNullType', type: { kind: 'NamedType', name: { kind: 'Name', value: 'AuthInput' } } }
        }
      ],
      selectionSet: {
        kind: 'SelectionSet',
        selections: [
          {
            kind: 'Field',
            name: { kind: 'Name', value: 'auth' },
            selectionSet: {
              kind: 'SelectionSet',
              selections: [
                {
                  kind: 'Field',
                  name: { kind: 'Name', value: 'register' },
                  arguments: [
                    {
                      kind: 'Argument',
                      name: { kind: 'Name', value: 'data' },
                      value: { kind: 'Variable', name: { kind: 'Name', value: 'data' } }
                    }
                  ],
                  selectionSet: {
                    kind: 'SelectionSet',
                    selections: [
                      {
                        kind: 'Field',
                        name: { kind: 'Name', value: 'user' },
                        selectionSet: {
                          kind: 'SelectionSet',
                          selections: [{ kind: 'Field', name: { kind: 'Name', value: 'email' } }]
                        }
                      },
                      { kind: 'Field', name: { kind: 'Name', value: 'accessToken' } }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    }
  ]
} as unknown as DocumentNode<RegisterMutation, RegisterMutationVariables>

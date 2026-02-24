'use client'

import { useMutation } from '@apollo/client/react'
import { ArrowRight, Eye, EyeClosed } from 'lucide-react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { type ComponentProps, useState, useTransition } from 'react'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'

import { Button } from '@/shared/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/components/ui/card'
import { Input } from '@/shared/components/ui/input'
import { Typography } from '@/shared/components/ui/typography'

import { DASHBOARD_PAGES, PUBLIC_PAGES } from '@/shared/config/page.config'

import {
  INVALID_EMAIL_PATTERN,
  INVALID_PASSWORD_PATTERN,
  REQUIRED_INPUT_ERROR
} from '@/shared/constants/error.constants'
import { EMAIL_PATTERN, PASSWORD_PATTERN } from '@/shared/constants/regex.constants'
import { ICON_SIZE } from '@/shared/constants/styles.constants'

import { extractError } from '@/shared/api/error.helper'

import { type AuthInput, RegisterDocument } from '@/__generated__/graphql'

type FormData = AuthInput

export function RegisterForm(props: ComponentProps<'div'>) {
  const router = useRouter()
  const [isMounting, startTransition] = useTransition()
  const [mutate, { loading: isLoading }] = useMutation(RegisterDocument)

  const [isPasswordVisible, setIsPasswordVisible] = useState(false)

  const {
    reset,
    register,
    handleSubmit,
    formState: { errors, isValid }
  } = useForm<FormData>({
    mode: 'onChange'
  })

  const submit = async (data: FormData) => {
    await mutate({
      variables: {
        data: data
      },
      onCompleted: () => {
        startTransition(() => {
          reset()
          router.replace(DASHBOARD_PAGES.HOME)
          toast.success('Registered is successfully!', { id: 'register-succuss' })
        })
      },
      onError: (error) => {
        extractError(error).map((message) => toast.error(message))
      }
    })
  }

  return (
    <Card {...props}>
      <CardHeader>
        <CardTitle>Sign Up</CardTitle>
      </CardHeader>
      <CardContent>
        <form className={`flex flex-col gap-4`}>
          <Input
            {...register('email', {
              required: REQUIRED_INPUT_ERROR,
              pattern: {
                value: EMAIL_PATTERN,
                message: INVALID_EMAIL_PATTERN
              }
            })}
            type={'email'}
            inputMode={'email'}
            placeholder="Enter email"
            error={errors?.email?.message}
          />
          <Input
            {...register('password', {
              required: REQUIRED_INPUT_ERROR,
              pattern: {
                value: PASSWORD_PATTERN,
                message: INVALID_PASSWORD_PATTERN
              }
            })}
            type={isPasswordVisible ? 'text' : 'password'}
            placeholder="Enter password"
            error={errors?.password?.message}
            RightComponent={
              <Button
                variant={'icon'}
                onClick={() => setIsPasswordVisible((prev) => !prev)}
              >
                {isPasswordVisible ? <Eye size={ICON_SIZE.SM} /> : <EyeClosed size={ICON_SIZE.SM} />}
              </Button>
            }
          />
          <div className={`flex flex-row flex-wrap items-center justify-between gap-2`}>
            <div className={`flex flex-row items-center justify-start gap-1`}>
              <Typography
                variant={'body-1'}
                className={`text-gray-500`}
              >
                Already have an account?
              </Typography>
              <Link href={PUBLIC_PAGES.LOGIN}>
                <Typography
                  variant={'body-1'}
                  className={`text-primary`}
                >
                  Sign In
                </Typography>
              </Link>
            </div>
            <Button
              type={'submit'}
              disabled={!isValid}
              className="float-end"
              onClick={handleSubmit(submit)}
              isLoading={isMounting || isLoading}
            >
              Submit
              <ArrowRight size={ICON_SIZE.SM} />
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
}

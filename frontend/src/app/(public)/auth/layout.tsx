export default function AuthLayout({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  return <div className={`flex h-screen w-full items-center justify-center bg-gray-100`}>{children}</div>
}

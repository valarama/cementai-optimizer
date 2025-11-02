import './globals.css'

export const metadata = {
  title: 'CementAI Optimizer - Industrial AI for Cement Manufacturing',
  description: 'Real-time optimization powered by Google Cloud GenAI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

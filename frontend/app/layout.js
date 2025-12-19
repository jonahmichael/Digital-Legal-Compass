import './globals.css'

export const metadata = {
  title: 'Digital Legal Compass',
  description: 'RAG-powered legal document assistant',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background antialiased">{children}</body>
    </html>
  )
}

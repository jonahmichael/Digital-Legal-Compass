'use client'

import { useState } from 'react'
import DocumentUpload from './components/DocumentUpload'
import Chat from './components/Chat'

export default function Home() {
  const [documentsUploaded, setDocumentsUploaded] = useState(false)

  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold tracking-tight mb-2">
            Digital Legal Compass
          </h1>
          <p className="text-muted-foreground text-sm">
            RAG-powered legal document assistant
          </p>
        </header>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <DocumentUpload onUploadSuccess={() => setDocumentsUploaded(true)} />
          <Chat disabled={!documentsUploaded} />
        </div>
      </div>
    </main>
  )
}

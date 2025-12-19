'use client'

import { useState } from 'react'
import axios from 'axios'
import { Upload, File, CheckCircle2, XCircle, Loader2 } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export default function DocumentUpload({ onUploadSuccess }) {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('')

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files))
    setMessage('')
    setMessageType('')
  }

  const handleUpload = async () => {
    if (files.length === 0) {
      setMessage('Please select files to upload')
      setMessageType('error')
      return
    }

    setUploading(true)
    setMessage('')
    setMessageType('')

    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })

    try {
      const response = await axios.post('/api/documents/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      
      setMessage(`Successfully uploaded ${response.data.count} document(s)`)
      setMessageType('success')
      setFiles([])
      if (onUploadSuccess) onUploadSuccess()
    } catch (error) {
      setMessage('Error uploading documents: ' + (error.response?.data?.detail || error.message))
      setMessageType('error')
    } finally {
      setUploading(false)
    }
  }

  return (
    <Card className="h-full border-border/40">
      <CardHeader className="space-y-1">
        <CardTitle className="flex items-center gap-2 text-xl">
          <Upload className="h-5 w-5" />
          Upload Documents
        </CardTitle>
        <CardDescription>
          Select legal documents to analyze
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <label
            htmlFor="file-upload"
            className="relative flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer bg-muted/20 hover:bg-muted/40 transition-colors border-border/40"
          >
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <Upload className="w-8 h-8 mb-2 text-muted-foreground" />
              <p className="mb-1 text-sm text-muted-foreground">
                <span className="font-semibold">Click to upload</span> or drag and drop
              </p>
              <p className="text-xs text-muted-foreground">PDF, TXT, or MD files</p>
            </div>
            <input
              id="file-upload"
              type="file"
              multiple
              accept=".pdf,.txt,.md"
              onChange={handleFileChange}
              className="hidden"
              disabled={uploading}
            />
          </label>
        </div>

        {files.length > 0 && (
          <div className="space-y-2">
            <p className="text-sm font-medium">Selected files:</p>
            <div className="space-y-1">
              {files.map((file, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-2 text-sm p-2 rounded-md bg-muted/40"
                >
                  <File className="h-4 w-4 text-muted-foreground" />
                  <span className="truncate">{file.name}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <Button
          onClick={handleUpload}
          disabled={uploading || files.length === 0}
          className="w-full"
        >
          {uploading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Uploading...
            </>
          ) : (
            <>
              <Upload className="mr-2 h-4 w-4" />
              Upload Documents
            </>
          )}
        </Button>

        {message && (
          <div
            className={`flex items-start gap-2 p-3 rounded-md text-sm ${
              messageType === 'success'
                ? 'bg-green-500/10 text-green-500 border border-green-500/20'
                : 'bg-destructive/10 text-destructive border border-destructive/20'
            }`}
          >
            {messageType === 'success' ? (
              <CheckCircle2 className="h-4 w-4 mt-0.5 flex-shrink-0" />
            ) : (
              <XCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
            )}
            <span>{message}</span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

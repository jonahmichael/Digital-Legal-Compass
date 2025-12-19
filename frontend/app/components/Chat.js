'use client'

import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { MessageSquare, Send, Loader2, AlertCircle } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export default function Chat({ disabled }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!input.trim() || loading) return

    const userMessage = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/documents/chat', {
        message: input,
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage = {
        role: 'error',
        content: error.response?.data?.detail || error.message,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="h-full border-border/40 flex flex-col">
      <CardHeader className="space-y-1">
        <CardTitle className="flex items-center gap-2 text-xl">
          <MessageSquare className="h-5 w-5" />
          Chat
        </CardTitle>
        <CardDescription>
          Ask questions about your documents
        </CardDescription>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col space-y-4 min-h-0">
        {disabled && (
          <div className="flex items-start gap-2 p-3 rounded-md text-sm bg-yellow-500/10 text-yellow-500 border border-yellow-500/20">
            <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
            <span>Please upload documents first to start chatting</span>
          </div>
        )}

        <div className="flex-1 overflow-y-auto space-y-4 pr-2 scrollbar-hide min-h-0">
          {messages.length === 0 && !disabled && (
            <div className="h-full flex items-center justify-center text-center text-muted-foreground text-sm">
              Ask a question about your uploaded legal documents
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] p-3 rounded-lg text-sm ${
                  msg.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : msg.role === 'error'
                    ? 'bg-destructive/10 text-destructive border border-destructive/20'
                    : 'bg-muted/60 text-foreground'
                }`}
              >
                <div className="whitespace-pre-wrap break-words">{msg.content}</div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-muted/60 text-foreground p-3 rounded-lg flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span className="text-sm">Thinking...</span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2 pt-4 border-t border-border/40">
          <Input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
            disabled={disabled || loading}
            className="flex-1"
          />
          <Button
            type="submit"
            disabled={disabled || loading || !input.trim()}
            size="icon"
          >
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}

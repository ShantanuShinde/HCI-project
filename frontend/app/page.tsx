"use client"

import { useState } from "react"
import { MessageList } from "@/components/message-list"
import { MessageInput } from "@/components/message-input"
import { Flag } from "lucide-react"

export type Message = {
  id: string
  text: string
  timestamp: Date
  status: "checking" | "approved" | "flagged"
  reported?: boolean
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])

  const handleSendMessage = async (text: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      text,
      timestamp: new Date(),
      status: "checking",
    }

    setMessages((prev) => [...prev, newMessage])

    try {
      // Call moderation API
      const response = await fetch("/api/moderate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      })

      const data = await response.json()

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === newMessage.id ? { ...msg, status: data.isAppropriate ? "approved" : "flagged" } : msg,
        ),
      )
    } catch (error) {
      console.error("Moderation check failed:", error)
      // Default to approved on error
      setMessages((prev) => prev.map((msg) => (msg.id === newMessage.id ? { ...msg, status: "approved" } : msg)))
    }
  }

  const handleReportMessage = async (messageId: string) => {
    const message = messages.find((msg) => msg.id === messageId)
    if (!message) return

    try {
      await fetch("/api/report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: message.text }),
      })

      setMessages((prev) => prev.map((msg) => (msg.id === messageId ? { ...msg, reported: true } : msg)))
    } catch (error) {
      console.error("Report failed:", error)
    }
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="border-b border-border bg-card px-6 py-4">
        <div className="mx-auto flex max-w-4xl items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary">
            <Flag className="h-5 w-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-balance">Content Moderation Tester</h1>
          </div>
        </div>
      </header>

      <main className="flex flex-1 flex-col">
        <div className="mx-auto w-full max-w-4xl flex-1 px-6 py-6">
          <MessageList messages={messages} onReport={handleReportMessage} />
        </div>

        <div className="border-t border-border bg-card px-6 py-4">
          <div className="mx-auto max-w-4xl">
            <MessageInput onSend={handleSendMessage} />
          </div>
        </div>
      </main>
    </div>
  )
}

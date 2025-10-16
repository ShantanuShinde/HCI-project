import type { Message } from "@/app/page"
import { MessageItem } from "./message-item"

interface MessageListProps {
  messages: Message[]
  onReport: (messageId: string) => void
}

export function MessageList({ messages, onReport }: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">No messages yet. Send a message to test moderation.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-4">
      {messages.map((message) => (
        <MessageItem key={message.id} message={message} onReport={onReport} />
      ))}
    </div>
  )
}

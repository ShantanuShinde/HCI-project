"use client"

import type { Message } from "@/app/page"
import { Button } from "@/components/ui/button"
import { AlertTriangle, CheckCircle2, Loader2, Flag } from "lucide-react"
import { cn } from "@/lib/utils"

interface MessageItemProps {
  message: Message
  onReport: (messageId: string) => void
}

export function MessageItem({ message, onReport }: MessageItemProps) {
  const getStatusIcon = () => {
    switch (message.status) {
      case "checking":
        return <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
      case "approved":
        return <CheckCircle2 className="h-4 w-4 text-success" />
      case "flagged":
        return <AlertTriangle className="h-4 w-4 text-destructive" />
    }
  }

  const getStatusText = () => {
    switch (message.status) {
      case "checking":
        return "Checking..."
      case "approved":
        return "Approved"
      case "flagged":
        return "Flagged"
    }
  }

  return (
    <div
      className={cn(
        "rounded-lg border p-4 transition-colors",
        message.status === "flagged" ? "border-destructive/50 bg-destructive/5" : "border-border bg-card",
      )}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 space-y-2">
          <p className="text-sm leading-relaxed text-pretty">{message.text}</p>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>{message.timestamp.toLocaleTimeString()}</span>
            <span>•</span>
            <div className="flex items-center gap-1.5">
              {getStatusIcon()}
              <span>{getStatusText()}</span>
            </div>
          </div>
        </div>

        {message.status === "approved" && !message.reported && (
          <Button variant="ghost" size="sm" onClick={() => onReport(message.id)} className="shrink-0">
            <Flag className="mr-2 h-4 w-4" />
            Report
          </Button>
        )}

        {message.reported && (
          <div className="flex items-center gap-1.5 rounded-md bg-warning/10 px-3 py-1.5 text-xs text-warning-foreground">
            <Flag className="h-3.5 w-3.5" />
            Reported
          </div>
        )}
      </div>
    </div>
  )
}

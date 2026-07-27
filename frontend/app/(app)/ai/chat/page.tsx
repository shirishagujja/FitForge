"use client";

import { Send } from "lucide-react";
import { useState, type FormEvent } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

type Message = { role: "user" | "assistant"; content: string };

export default function AiChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isSending) return;

    const nextMessages: Message[] = [...messages, { role: "user", content: trimmed }];
    setMessages(nextMessages);
    setInput("");
    setError(null);
    setIsSending(true);

    try {
      const response = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: nextMessages }),
      });
      const body = await response.json();
      if (!response.ok) {
        setError(body?.error?.message ?? "The coach is unavailable right now.");
        return;
      }
      setMessages([...nextMessages, { role: "assistant", content: body.data.message }]);
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="mx-auto flex h-[calc(100vh-8rem)] max-w-2xl flex-col gap-4">
      <h1 className="text-2xl font-bold tracking-tight">Chat with your coach</h1>

      <Card className="flex flex-1 flex-col overflow-hidden">
        <CardContent className="flex-1 space-y-3 overflow-y-auto p-4">
          {messages.length === 0 && (
            <p className="text-sm text-muted-foreground">
              Ask about training, recovery, nutrition — anything fitness related.
            </p>
          )}
          {messages.map((message, index) => (
            <div
              key={index}
              className={cn("flex", message.role === "user" ? "justify-end" : "justify-start")}
            >
              <div
                className={cn(
                  "max-w-[80%] rounded-lg px-3 py-2 text-sm",
                  message.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-foreground",
                )}
              >
                {message.content}
              </div>
            </div>
          ))}
          {isSending && <p className="text-sm text-muted-foreground">Thinking…</p>}
        </CardContent>
        {error && <p className="px-4 pb-2 text-sm font-medium text-destructive">{error}</p>}
        <form onSubmit={onSubmit} className="flex gap-2 border-t border-border p-3">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your coach…"
            disabled={isSending}
          />
          <Button type="submit" size="icon" disabled={isSending || !input.trim()}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </Card>
    </div>
  );
}

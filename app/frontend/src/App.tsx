import { useEffect, useRef, useState } from "react";
import { askFinancialAssistant } from "./api/client";
import { ChatBubble } from "./components/ChatBubble";
import { ChatComposer } from "./components/ChatComposer";
import type { ChatMessage } from "./types";

const WELCOME_MESSAGE: ChatMessage = {
  id: "welcome",
  role: "assistant",
  text: "Hi! I'm your Financial Assistant. Ask me about your accounts, spending, or the market.",
};

function createId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [isSending, setIsSending] = useState(false);
  const scrollAnchorRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollAnchorRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(text: string) {
    const userMessage: ChatMessage = { id: createId(), role: "user", text };
    const pendingId = createId();
    const pendingMessage: ChatMessage = {
      id: pendingId,
      role: "assistant",
      text: "",
      pending: true,
    };

    setMessages((prev) => [...prev, userMessage, pendingMessage]);
    setIsSending(true);

    try {
      const response = await askFinancialAssistant(text);
      setMessages((prev) =>
        prev.map((message) =>
          message.id === pendingId
            ? {
                ...message,
                pending: false,
                text: response.answer,
                sqlQuery: response.sql_query,
                chart: response.chart,
              }
            : message,
        ),
      );
    } catch {
      setMessages((prev) =>
        prev.map((message) =>
          message.id === pendingId
            ? {
                ...message,
                pending: false,
                error: true,
                text: "Sorry, I couldn't reach the assistant. Please try again.",
              }
            : message,
        ),
      );
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-avatar">$</div>
        <div>
          <h1 className="app-header-title">Financial Assistant</h1>
          <p className="app-header-subtitle">{isSending ? "typing…" : "online"}</p>
        </div>
      </header>

      <main className="chat-scroll">
        {messages.map((message) => (
          <ChatBubble key={message.id} message={message} />
        ))}
        <div ref={scrollAnchorRef} />
      </main>

      <footer className="app-footer">
        <ChatComposer onSend={handleSend} disabled={isSending} />
      </footer>
    </div>
  );
}

export default App;

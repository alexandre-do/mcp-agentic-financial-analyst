import type { ChatMessage } from "../types";

interface ChatBubbleProps {
  message: ChatMessage;
}

export function ChatBubble({ message }: ChatBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`bubble-row ${isUser ? "bubble-row--user" : "bubble-row--assistant"}`}>
      <div
        className={`bubble ${isUser ? "bubble--user" : "bubble--assistant"} ${
          message.error ? "bubble--error" : ""
        }`}
      >
        {message.pending ? (
          <span className="typing-dots" aria-label="Assistant is typing">
            <span />
            <span />
            <span />
          </span>
        ) : (
          <>
            <p className="bubble-text">{message.text}</p>
            {message.sqlQuery && (
              <pre className="bubble-code">
                <code>{message.sqlQuery}</code>
              </pre>
            )}
            {message.chart && (
              <img className="bubble-chart" src={message.chart} alt="Generated chart" />
            )}
          </>
        )}
      </div>
    </div>
  );
}

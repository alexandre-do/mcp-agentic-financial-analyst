import { useState } from "react";
import type { FormEvent } from "react";

interface ChatComposerProps {
  onSend: (text: string) => void;
  disabled?: boolean;
}

export function ChatComposer({ onSend, disabled }: ChatComposerProps) {
  const [value, setValue] = useState("");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  }

  return (
    <form className="composer" onSubmit={handleSubmit}>
      <input
        className="composer-input"
        type="text"
        inputMode="text"
        placeholder="Ask about your finances..."
        value={value}
        onChange={(event) => setValue(event.target.value)}
        disabled={disabled}
        autoComplete="off"
      />
      <button
        className="composer-send"
        type="submit"
        disabled={disabled || !value.trim()}
        aria-label="Send message"
      >
        ↑
      </button>
    </form>
  );
}

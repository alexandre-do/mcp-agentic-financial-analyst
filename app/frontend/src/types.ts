export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
  sqlQuery?: string | null;
  chart?: string | null;
  pending?: boolean;
  error?: boolean;
}

export interface QueryResponse {
  question: string;
  answer: string;
  sql_query?: string | null;
  chart?: string | null;
}

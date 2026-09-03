# Financial Assistant — Frontend

Mobile-first chat client for the Financial Assistant Bot, built with React, TypeScript, and Vite. It talks to the FastAPI backend at [`app/backend/routes.py`](../backend/routes.py) via a single `POST /query` call.

## Getting started

```bash
npm install
cp .env.example .env   # adjust VITE_API_BASE_URL if the backend isn't on localhost:8000
npm run dev
```

The dev server runs at `http://localhost:5173`. Open it in a phone-sized browser window (or your device on the same network with `npm run dev -- --host`) to see the mobile layout.

Start the backend separately from the repo root:

```bash
uv run uvicorn app.backend.routes:app --port 8000
```

## Structure

- `src/App.tsx` — chat screen: message state, sending, scroll-to-latest.
- `src/components/ChatBubble.tsx` — a single message bubble (user/assistant, typing indicator, optional SQL snippet and chart).
- `src/components/ChatComposer.tsx` — the bottom input bar.
- `src/api/client.ts` — fetch wrapper for `POST /query`.
- `src/types.ts` — shared message/response types, mirroring `app/backend/schemas.py`.
- `src/index.css` — mobile-first styling (safe-area insets, dark theme, 480px max width).

## CLI reference

Run from `app/frontend/`:

| Command | Description |
| --- | --- |
| `npm install` | Install dependencies. |
| `npm run dev` | Start the Vite dev server at `http://localhost:5173` (add `-- --host` to expose it on your LAN for testing on a phone). |
| `npm run build` | Type-check (`tsc -b`) and produce a production build in `dist/`. |
| `npm run preview` | Serve the production build from `dist/` locally. |
| `npm run lint` | Run Oxlint. |

From the repo root, prefix any of the above with `--prefix app/frontend`, e.g.:

```bash
npm --prefix app/frontend install
npm --prefix app/frontend run dev
```

## Notes

- The backend's `/query` endpoint is currently a stub (see [Notes](../../README.md#notes) in the repo README) — it echoes a placeholder answer until the orchestrator is wired in.
- CORS is enabled on the backend for `http://localhost:5173` only; update `app/backend/routes.py` if you serve the frontend from a different origin.
- This is a responsive web app, not a native app — it can be wrapped as a PWA or embedded in a native shell (e.g. Capacitor) later without changing the chat UI.

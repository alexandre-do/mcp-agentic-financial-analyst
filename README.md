# MCP Agentic Financial Analyst

This project is an agentic analytics application that can:

- interpret user queries in natural language,
- query SQL data sources (SQLite, e.g. the Chinook database),
- pull live market data from external providers (Alpha Vantage) via MCP,
- generate data visualizations (Plotly charts),
- orchestrate the above through LangChain/LangGraph agents,
- expose the tools over an MCP server and a FastAPI backend.

## Tech stack

**Agents & orchestration**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?logo=langgraph&logoColor=white)
![Anthropic Claude](https://img.shields.io/badge/Anthropic%20Claude-D97757?logo=anthropic&logoColor=white)

**Backend & protocol**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-000000?logo=modelcontextprotocol&logoColor=white)

**Data & visualization**

![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)

**Frontend**

![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)

A mobile-first chat UI for the bot, built with React/TypeScript/Vite, lives in [`app/frontend`](app/frontend). See its [README](app/frontend/README.md) for setup. It talks to the FastAPI backend's `/query` endpoint, which is still a stub.

## Architecture

```mermaid
flowchart LR
    FE["React/TS chat UI<br/>app/frontend"]
    API["FastAPI backend<br/>app/backend/routes.py"]

    subgraph Agents["LangChain / LangGraph agents · app/src/agents"]
        SQL["sql_agent"]
        INFO["info_agent"]
        VIZ["dataviz_agent"]
        CHAT["chat_agent<br/>(stub)"]
    end

    subgraph Tools["app/src/tools"]
        SQLT["sql_tools"]
        VIZT["dataviz_tools"]
        AVT["alphavantage_tools<br/>(unused)"]
    end

    DB[("SQLite<br/>e.g. Chinook.db")]
    AVMCP[["Alpha Vantage<br/>hosted MCP server"]]

    FE --> API
    API --> SQL & INFO & VIZ & CHAT

    SQL --> SQLT --> DB
    VIZ --> VIZT
    INFO -- MCP client --> AVMCP
    AVT -. not wired in .-> AVMCP
```

`sql_agent` and `dataviz_agent` are runnable today; `info_agent` talks to Alpha Vantage's hosted MCP server directly. `chat_agent` and the FastAPI `/query` endpoint are still scaffolding — the frontend chat UI is built but calls into a stub response until they're wired in — see [Notes](#notes).

## Data

### Alpha Vantage (market data)

Live market data (quotes, time series, company fundamentals, symbol search) is sourced from [Alpha Vantage](https://www.alphavantage.co/). Two integration paths exist:

- **Hosted MCP server** — [`info_agent.py`](app/src/agents/info_agent.py) connects as an MCP client to Alpha Vantage's hosted MCP server (`https://mcp.alphavantage.co/mcp`), giving the agent Alpha Vantage's full tool catalog without a local wrapper. This is the path currently wired into an agent.
- **Local REST wrapper** — [`alphavantage_tools.py`](app/src/tools/alphavantage_tools.py) calls the Alpha Vantage REST API directly (`get_stock_quote`, `get_daily_time_series`, `get_company_overview`, `search_symbol`) for graphs that shouldn't depend on the hosted MCP server. It isn't wired into an agent yet.

**Setup**

1. Get a free API key: https://www.alphavantage.co/support/#api-key (the free tier is rate-limited; the placeholder `demo` key works for limited testing).
2. Set `ALPHA_VANTAGE_API_KEY` in `.env`.

## Getting started

1. Create a virtual environment (or use `uv`, since this repo is `uv`-managed):
   ```bash
   uv sync
   ```
   or with pip:
   ```bash
   pip install -e .
   ```
2. Copy the environment template and fill in your own values (model id, API keys, path to the SQLite database, etc.):
   ```bash
   cp .example.env .env
   ```
3. Run an agent directly, e.g.:
   ```bash
   python -m app.src.agents.sql_agent
   python -m app.src.agents.dataviz_agent
   python -m app.src.agents.info_agent
   ```
4. Run the test suite:
   ```bash
   pytest
   ```
5. Run the FastAPI backend and the chat frontend together:
   ```bash
   uv run uvicorn app.backend.routes:app --port 8000
   ```
   ```bash
   cd app/frontend && npm install && npm run dev
   ```
   Open `http://localhost:5173` for the mobile chat UI. See [`app/frontend/README.md`](app/frontend/README.md) for details.

The MCP server (`app/src/mcp/server.py`) is still early scaffolding and not yet wired to the agents above, and the FastAPI backend's `/query` endpoint is a stub — the frontend is functional but not yet connected to real agent orchestration.

## Notes

This repository is under active development. Several tools and the chat agent are still stubs — replace the placeholder logic with real implementations and orchestration flow as they mature.

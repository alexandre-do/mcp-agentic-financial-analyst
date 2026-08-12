# Agentic Data Analyst

This project is a starter template for an agentic analytics application that can:

- interpret user queries in natural language,
- orchestrate tool usage,
- query SQL data sources,
- inspect metadata,
- generate visualizations,
- expose an API and Streamlit front end.

## Project structure

```text
agentic-data-analyst/
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── agent/
│   │   ├── orchestrator.py
│   │   ├── prompts.py
│   │   ├── state.py
│   │   └── guardrails.py
│   ├── mcp/
│   │   ├── server.py
│   │   └── tools/
│   │       ├── sql_tools.py
│   │       ├── metadata_tools.py
│   │       └── visualization_tools.py
│   ├── services/
│   │   ├── sql_service.py
│   │   ├── metadata_service.py
│   │   └── visualization_service.py
│   └── config.py
├── tests/
│   ├── test_sql_tools.py
│   ├── test_agent.py
│   └── test_visualization.py
├── infrastructure/
│   ├── cloudformation/
│   └── cdk/
├── frontend/
│   └── streamlit/
├── pyproject.toml
├── README.md
└── .env
```

## Getting started

1. Create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -e .
   ```
3. Copy sample environment values from `.env` and update as needed.
4. Run the API:
   ```bash
   uvicorn app.api.routes:app --reload
   ```
5. Launch the Streamlit app:
   ```bash
   streamlit run frontend/streamlit/app.py
   ```

## Notes

This repository is intentionally scaffolded for extension and experimentation. Replace the placeholder logic with your actual database connections, tool implementations, and orchestration flow.

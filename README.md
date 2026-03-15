# create-ai-tooling-app

A CLI that scaffolds Python AI tooling API projects — batteries included, minimal by design.

## Usage

```bash
uvx create-ai-tooling-app
```

Or, if working locally:

```bash
uv run create-ai-tooling-app [output-dir]
```

You'll be prompted for:
- **Project name** — used for the directory and package name
- **LLM provider** — Anthropic (Claude) or OpenAI

## What gets generated

```
my-project/
├── pyproject.toml              # uv-managed, includes fastapi, pydantic, and your chosen LLM SDK
├── .env.example                # API key placeholder
├── .gitignore
├── README.md
└── src/
│   └── my_project/
│       ├── main.py             # FastAPI app entrypoint
│       ├── models/
│       │   ├── request.py      # Pydantic input model
│       │   └── response.py     # Pydantic output model
│       ├── prompts/
│       │   └── base.py         # Prompt builder
│       ├── llm/
│       │   └── client.py       # LLM client wrapper
│       └── routes/
│           └── tool.py         # POST /run endpoint
└── tests/
    └── test_tool.py
```

The request flow:

```
POST /run
  → validate input   (Pydantic ToolRequest)
  → build prompt     (prompts/base.py)
  → call LLM         (llm/client.py)
  → validate output  (Pydantic ToolResponse)
  → return response
```

## Development

```bash
uv sync
uv run create-ai-tooling-app
```

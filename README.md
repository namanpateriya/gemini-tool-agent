# Gemini Tool Agent

Lightweight AI tool agent powered by Google Gemini.

Supports:

- Tool reasoning and orchestration
- Semantic memory retrieval
- Deterministic tool execution
- CLI and API execution
- Evaluation and optimization workflows

Inspired by:
- Google Gemini Cookbook
- Modern Google ADK agentic patterns

---

# Features

- Google Gemini-powered reasoning
- Lightweight tool orchestration
- Semantic memory using FAISS
- Deterministic calculator execution
- Safe local file reading
- Explicit orchestration layer
- Modular tool registry
- CLI execution support
- FastAPI support
- Evaluation and optimization framework
- Workflow-level testing
- Structured tool execution

---

# Why This Repository

Modern AI systems are evolving from:

```text
single-response generation
```

to:

```text
reasoning + tools + memory + orchestration
```

This repository demonstrates how to build lightweight agentic AI systems using:
- Google Gemini
- semantic retrieval
- deterministic tools
- orchestration workflows

without relying on heavy frameworks.

---

# Architecture Overview

```text
User
 ↓
Gemini Reasoning Layer
 ↓
Tool Selection
 ↓
Tool Orchestrator
 ↓
Tool Execution
 ├── Calculator Tool
 ├── Memory Tool
 └── File Reader Tool
 ↓
Tool Results
 ↓
Gemini Final Response
```

---

# Repository Structure

```text
gemini-tool-agent/
│
├── app/
│   ├── main.py
│   ├── cli.py
│   ├── orchestrator.py
│   ├── service.py
│   ├── schemas.py
│   ├── config.py
│   │
│   ├── tools/
│   │   ├── calculator.py
│   │   ├── memory.py
│   │   ├── file_reader.py
│   │   └── registry.py
│   │
│   ├── memory/
│   │   ├── embeddings.py
│   │   └── vector_store.py
│   │
│   └── utils/
│       ├── gemini_client.py
│       └── logger.py
│
├── data/
├── examples/
├── evaluation/
├── references/
│
├── ARCHITECTURE.md
├── requirements.txt
├── .env.example
└── README.md
```

---

# Setup

```bash
git clone <your_repo>
cd gemini-tool-agent

pip install -r requirements.txt
```

Create `.env` file:

```text
GEMINI_API_KEY=your_key

MODEL_NAME=gemini-1.5-flash

TOP_K=3
MEMORY_LIMIT=100
MAX_INPUT_LENGTH=2000
MAX_TOOL_ITERATIONS=5
```

---

# CLI Execution

Run:

```bash
python -m app.cli --message "Calculate 20% of 500"
```

---

# Memory Example

Store memory:

```bash
python -m app.cli --message "Remember that I like football"
```

Retrieve memory:

```bash
python -m app.cli --message "What sports do I like?"
```

---

# File Reader Example

```bash
python -m app.cli --message "Read notes.txt and summarize it"
```

---

# API Execution

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# Example API Request

```bash
curl -X POST "http://127.0.0.1:8000/chat" \
-H "Content-Type: application/json" \
-d '{"message":"Calculate 15% of 240"}'
```

---

# Tool System

The repository currently supports:

| Tool | Purpose |
|---|---|
| calculator | deterministic calculations |
| memory | semantic memory retrieval |
| file_reader | safe local file access |

---

# Semantic Memory

The repository uses:
- sentence-transformers
- FAISS vector retrieval

for lightweight semantic memory.

Memory flow:

```text
Conversation
→ embeddings
→ vector retrieval
→ contextual augmentation
```

---

# Orchestration Philosophy

The repository follows:

```text
LLM for reasoning
Tools for execution
```

Gemini:
- reasons about tasks
- selects tools
- orchestrates workflows

Tools:
- execute deterministic logic
- retrieve context
- perform calculations

This separation improves:
- reliability
- debuggability
- evaluation capability
- orchestration visibility

---

# Evaluation Framework

The repository includes a workflow-level evaluation framework.

Evaluates:
- tool selection accuracy
- memory retrieval quality
- orchestration correctness
- response grounding
- security validation

Run evaluation:

```bash
python -m evaluation.evaluator
```

Run optimizer:

```bash
python -m evaluation.optimizer
```

---

# Security Considerations

The repository intentionally avoids:
- arbitrary shell execution
- unrestricted file access
- dynamic Python execution
- unsafe filesystem traversal

File access is sandboxed to:
```text
/data
```

directory only.

---

# Google Ecosystem Alignment

This repository is intentionally aligned with modern Google AI workflows.

Built using:
- Google Gemini API
- Gemini tool-calling workflows
- Google-native agentic patterns

Inspired by:
- Google Gemini Cookbook
- Google AI Studio experimentation workflows
- modern Google ADK orchestration concepts

The repository explores lightweight implementations of:
- AI reasoning
- semantic memory
- tool orchestration
- agentic workflows

within the Google GenAI ecosystem.

---

# Use Cases

- AI copilots
- semantic memory assistants
- lightweight agentic systems
- tool-using assistants
- orchestration experimentation
- Google Gemini experimentation
- AI workflow prototyping

---

# Future Enhancements

Potential future improvements:
- persistent vector memory
- streaming responses
- multimodal tools
- browser automation
- reranking
- memory categorization
- tool confidence scoring
- MCP compatibility
- multi-agent orchestration

---

# References

See:
```text
references/README.md
```

for ecosystem references and inspiration sources.

---

# Design Philosophy

The focus is:
- architectural clarity
- modern AI orchestration
- practical agentic workflows
- lightweight engineering
- Google-aligned AI experimentation

---

Built for modern AI systems engineering using Google Gemini.

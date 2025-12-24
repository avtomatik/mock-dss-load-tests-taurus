# Mock DSS Load Tests with Taurus and Molotov

A set of load tests for the mock DSS services using Taurus and Molotov.

---

## Base Option (Debugging in VS Code)

1. Create and activate the virtual environment:

```bash
uv venv
source .venv/bin/activate
uv sync
```

2. Open **Command Palette** in VS Code (`Ctrl + Shift + P`) → **Python: Select Interpreter** → select the `.venv` interpreter.

3. Start debugging with **F5**.

---

## Extended Option (Run Full Load Test)

1. Create and activate the virtual environment:

```bash
uv venv
source .venv/bin/activate
uv sync
```

2. Run the full Taurus load test:

```bash
uv run bzt taurus.yml
```
---

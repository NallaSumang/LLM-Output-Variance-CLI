# LLM-Output-Variance-CLI

A benchmarking CLI that systematically evaluates how the `temperature` parameter affects Large Language Model output — ranging from deterministic precision to creative divergence. 

This project was built as part of the [roadmap.sh LLM/OpenAI API Track](https://roadmap.sh/projects/openai-api-python), demonstrating programmatic LLM interaction beyond the standard ChatGPT interface using the OpenAI-compatible `chat.completions` API pattern.

> **Why this matters:** Understanding temperature is foundational to every LLM application — from RAG pipelines to agentic workflows. This utility provides a side-by-side comparison framework for empirical evaluation of model creativity vs. hallucinations.

---

## Features

- **Multi-profile benchmarking** — Tests across 4 temperature settings (0.0 → 1.5) in a single run.
- **Latency & token tracking** — Measures response time and token consumption per call.
- **OpenAI-compatible API** — Uses the `chat.completions.create()` interface, making it portable across providers (OpenAI, Groq, local models).
- **Secure credential management** — API keys loaded securely from `.env` via `python-dotenv`.
- **Configurable Architecture** — Easy to swap models, add temperature profiles, or adjust system prompts.
- **Cross-Platform UI** — Clean, formatted ASCII console output that natively handles Windows/Linux encoding quirks.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/NallaSumang/LLM-Output-Variance-CLI.git
cd LLM-Output-Variance-CLI

# Setup virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables
cp .env.example .env
# Edit .env and add your API key (free at https://console.groq.com/keys)

# Run Benchmark
python openai_test.py
```

---

## Sample Output

```
============================================================
          LLM-Output-Variance-CLI
          Evaluating output diversity across temps
============================================================

Enter a creative prompt (e.g., 'Write a one-line slogan for a coffee shop'): in two short lines explain ai agentic and pipeline flows
  Running benchmark across temperature profiles...
  Profiles: ['Deterministic', 'Balanced', 'Creative', 'Experimental']

============================================================
  PROMPT: "in two short lines explain ai agentic and pipeline flows"
  MODEL:  llama-3.3-70b-versatile
============================================================

  [DETERMINISTIC | temp=0.0]
  Latency: 864.2ms | Tokens: 37
  --------------------------------------------------------
    AI Agentic flows involve autonomous decision-making and action-taking by AI systems.
    Pipeline flows, in contrast, refer to sequential processing of data through a series of AI models and tasks.
  --------------------------------------------------------

  [EXPERIMENTAL | temp=1.5]
  Latency: 383.3ms | Tokens: 24
  --------------------------------------------------------
    AI agentic refers to autonomous systems making decisions. 
    Pipeline flows manage data processing sequences for AI model training and deployment.
  --------------------------------------------------------

============================================================
  Benchmark complete - 4 temperature profiles tested.
============================================================
```

---

## How Temperature Works

| Temperature | Behavior | Best Use Case |
|:-----------:|----------|---------------|
| **0.0** | Deterministic — always picks the highest-probability token | Factual Q&A, Code generation, Data Extraction |
| **0.5** | Balanced — slight variation while staying coherent | Summarisation, Structured writing |
| **1.0** | Creative — explores diverse token choices | Brainstorming, Marketing copy, Storytelling |
| **1.5** | Experimental — maximum randomness | Pure creative writing, Extreme idea generation |

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| LLM API | OpenAI-compatible (`chat.completions`) |
| Model | Llama 3.3 70B via [Groq](https://groq.com) (free tier for high-speed inference) |
| Env Management | `python-dotenv` |

---

## Acknowledgments & Related Projects

This utility serves as a foundational evaluation tool for my larger AI systems:

| Project | Description |
|---------|-------------|
| [DISTRIBUTED-AI-RESEARCHER-](https://github.com/NallaSumang/DISTRIBUTED-AI-RESEARCHER-) | Distributed swarm of Llama 3.3 70B agents for deep research synthesis |
| [PlaceIQ-Agentic-Copilot](https://github.com/NallaSumang/PlaceIQ-Agentic-Copilot) | Multi-agent LLM orchestrator for campus placement workflows |
| [Lumina-Proposals](https://github.com/NallaSumang/Lumina-Proposals) | Enterprise RAG platform for automated RFP generation |

**Project Prompt Origin:** [roadmap.sh - OpenAI API in Python](https://roadmap.sh/projects/openai-api-python)

---

## License

MIT

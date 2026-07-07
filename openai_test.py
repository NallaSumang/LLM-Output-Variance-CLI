"""
LLM-Output-Variance-CLI
==============================
A benchmarking utility that systematically evaluates how temperature parameters
affect Large Language Model output diversity, creativity, and determinism.

Supports multiple LLM providers via OpenAI-compatible API interfaces.
"""

import os
import sys
import time

# Ensure UTF-8 output on Windows terminals
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL_ID = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = (
    "You are a creative but precise AI assistant. "
    "Answer the user query directly and concisely."
)
TEMPERATURE_PROFILES = {
    "Deterministic": 0.0,
    "Balanced": 0.5,
    "Creative": 1.0,
    "Experimental": 1.5,
}
MAX_TOKENS = 200


def create_client() -> Groq:
    """Initialise the LLM client with environment credentials."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. "
            "Create a free key at https://console.groq.com/keys "
            "and add it to your .env file."
        )
    return Groq(api_key=api_key)


def query_llm(client: Groq, prompt: str, temperature: float) -> dict:
    """
    Send a single prompt to the LLM and return the response with metadata.

    Returns:
        dict with keys: text, model, temperature, latency_ms, tokens_used
    """
    start = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=MAX_TOKENS,
        )
        latency = (time.perf_counter() - start) * 1000
        usage = response.usage
        return {
            "text": response.choices[0].message.content.strip(),
            "model": response.model,
            "temperature": temperature,
            "latency_ms": round(latency, 1),
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
        }
    except Exception as exc:
        return {"text": f"Error: {exc}", "temperature": temperature}


def run_benchmark(client: Groq, prompt: str) -> list[dict]:
    """Run the prompt across all temperature profiles and collect results."""
    results = []
    for label, temp in TEMPERATURE_PROFILES.items():
        result = query_llm(client, prompt, temp)
        result["label"] = label
        results.append(result)
    return results


def display_results(prompt: str, results: list[dict]) -> None:
    """Pretty-print benchmark results to the terminal."""
    width = 60
    print(f"\n{'=' * width}")
    print(f"  PROMPT: \"{prompt}\"")
    print(f"  MODEL:  {results[0].get('model', MODEL_ID)}")
    print(f"{'=' * width}")

    for r in results:
        label = r.get("label", "Unknown")
        temp = r["temperature"]
        text = r["text"]
        latency = r.get("latency_ms", "N/A")
        tokens = r.get("completion_tokens", "N/A")

        print(f"\n  [{label.upper()} | temp={temp}]")
        print(f"  Latency: {latency}ms | Tokens: {tokens}")
        print(f"  {'-' * (width - 4)}")
        # Indent each line of the response
        for line in text.split("\n"):
            print(f"    {line}")
        print(f"  {'-' * (width - 4)}")

    print(f"\n{'=' * width}")
    print(f"  Benchmark complete - {len(results)} temperature profiles tested.")
    print(f"{'=' * width}\n")


def main():
    """Entry point: collect user prompt and run the temperature benchmark."""
    print("\n" + "=" * 60)
    print("          LLM-Output-Variance-CLI")
    print("          Evaluating output diversity across temps")
    print("=" * 60 + "\n")

    client = create_client()

    user_prompt = input(
        "Enter a creative prompt "
        "(e.g., 'Write a one-line slogan for a coffee shop'): "
    ).strip()

    if not user_prompt:
        user_prompt = "Write a one-line slogan for a coffee shop"
        print(f"  Using default prompt: \"{user_prompt}\"")

    print("\n  Running benchmark across temperature profiles...")
    print(f"  Profiles: {list(TEMPERATURE_PROFILES.keys())}\n")

    results = run_benchmark(client, user_prompt)
    display_results(user_prompt, results)


if __name__ == "__main__":
    main()

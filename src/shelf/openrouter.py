"""Minimal OpenRouter client restricted to providers that do not train on data."""

import httpx

URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-sonnet-5.5"


def complete(
    api_key: str,
    content: list | str,
    max_tokens: int,
    temperature: float,
    response_format: dict | None = None,
) -> tuple[str, float]:
    """Returns the model's text and the cost in US dollars reported by OpenRouter."""
    body = {
        "model": MODEL,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": content}],
        "provider": {"data_collection": "deny"},
        "usage": {"include": True},
    }
    if response_format is not None:
        body["response_format"] = response_format
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/89retreat/89books",
        "X-Title": "89books shelf",
    }
    response = httpx.post(URL, json=body, headers=headers, timeout=300)
    response.raise_for_status()
    data = response.json()
    text = data["choices"][0]["message"].get("content") or ""
    return text, float(data.get("usage", {}).get("cost") or 0.0)

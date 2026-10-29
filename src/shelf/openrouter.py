"""Minimal OpenRouter client restricted to providers that do not train on data."""

import httpx

URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-sonnet-5.5"


class IncompleteResponseError(RuntimeError):
    """OpenRouter ended a completion before the requested answer was complete."""

    def __init__(self, response: str, cost: float, finish_reason: str | None):
        super().__init__(f"OpenRouter completion ended with {finish_reason or 'no finish reason'}")
        self.response = response
        self.cost = cost
        self.finish_reason = finish_reason


def complete(
    api_key: str,
    content: list | str,
    max_tokens: int,
    temperature: float | None = None,
    response_format: dict | None = None,
    reasoning: dict | None = None,
    require_complete: bool = False,
) -> tuple[str, float]:
    """Returns the model's text and the cost in US dollars reported by OpenRouter."""
    body = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": content}],
        "provider": {"data_collection": "deny"},
        "usage": {"include": True},
    }
    if temperature is not None:
        body["temperature"] = temperature
    if response_format is not None:
        body["response_format"] = response_format
    if reasoning is not None:
        body["reasoning"] = reasoning
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/89retreat/89books",
        "X-Title": "89books shelf",
    }
    response = httpx.post(URL, json=body, headers=headers, timeout=300)
    response.raise_for_status()
    data = response.json()
    choice = data["choices"][0]
    text = choice["message"].get("content") or ""
    cost = float(data.get("usage", {}).get("cost") or 0.0)
    finish_reason = choice.get("finish_reason")
    if require_complete and finish_reason != "stop":
        raise IncompleteResponseError(text, cost, finish_reason)
    return text, cost

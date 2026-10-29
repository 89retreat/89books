import httpx
import pytest

from shelf import openrouter


def test_complete_sends_optional_response_format_without_changing_other_calls(monkeypatch):
    seen = []

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "id": "gen-1",
                "choices": [{"message": {"content": '{"ok":true}'}, "finish_reason": "stop"}],
                "usage": {"cost": 0.01},
            }

    def post(url, json, headers, timeout):
        seen.append((url, json, headers, timeout))
        return Response()

    monkeypatch.setattr(httpx, "post", post)
    response_format = {"type": "json_schema", "json_schema": {"name": "result", "schema": {}}}

    text, cost = openrouter.complete(
        "sk-secret",
        "prompt",
        max_tokens=100,
        temperature=0,
        response_format=response_format,
    )

    assert text == '{"ok":true}' and cost == 0.01
    assert seen[0][1]["response_format"] == response_format
    assert seen[0][1]["provider"] == {"data_collection": "deny"}


def test_complete_omits_temperature_and_sends_reasoning_when_requested(monkeypatch):
    seen = {}

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "choices": [{"message": {"content": "done"}, "finish_reason": "stop"}],
                "usage": {"cost": 0.02},
            }

    def post(url, json, headers, timeout):
        seen.update(json)
        return Response()

    monkeypatch.setattr(httpx, "post", post)

    assert openrouter.complete(
        "sk-secret",
        "prompt",
        max_tokens=64000,
        reasoning={"effort": "high", "exclude": True},
        require_complete=True,
    ) == ("done", 0.02)
    assert "temperature" not in seen
    assert seen["reasoning"] == {"effort": "high", "exclude": True}


def test_complete_preserves_partial_response_and_cost_when_model_does_not_finish(monkeypatch):
    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "choices": [{"message": {"content": '{"lens":"cut'}, "finish_reason": "length"}],
                "usage": {"cost": 0.013},
            }

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: Response())

    with pytest.raises(openrouter.IncompleteResponseError) as failed:
        openrouter.complete(
            "sk-secret",
            "prompt",
            max_tokens=64000,
            reasoning={"effort": "high"},
            require_complete=True,
        )

    assert failed.value.response == '{"lens":"cut'
    assert failed.value.cost == 0.013
    assert failed.value.finish_reason == "length"

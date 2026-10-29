import httpx

from shelf import openrouter


def test_complete_sends_optional_response_format_without_changing_other_calls(monkeypatch):
    seen = []

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "id": "gen-1",
                "choices": [{"message": {"content": '{"ok":true}'}}],
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

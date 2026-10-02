"""Tests for ai_service.py — the AI adapter boundary.

These tests never call the real OpenRouter endpoint and never consume
company AI quota: the HTTP call is mocked in every test.
"""

import os
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import ai_service  # noqa: E402

TASK_CONTEXT = {
    "task_id": "T1",
    "department": "Finance",
    "task_name": "Reconcile payments",
    "weekly_runs": 330,
    "minutes_per_run": 18,
    "weekly_minutes": 5940,
}


def test_not_configured_without_api_key(monkeypatch):
    monkeypatch.delenv("AI_API_KEY", raising=False)
    assert ai_service.is_configured() is False


def test_configured_when_api_key_present(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    assert ai_service.is_configured() is True


def test_generate_exploration_raises_when_unconfigured(monkeypatch):
    monkeypatch.delenv("AI_API_KEY", raising=False)
    try:
        ai_service.generate_exploration(TASK_CONTEXT)
        assert False, "expected AIServiceUnavailable"
    except ai_service.AIServiceUnavailable as exc:
        assert "AI_API_KEY" in str(exc)


def _mock_openrouter_response(content: str) -> Mock:
    response = Mock()
    response.raise_for_status = Mock()
    response.json = Mock(return_value={"choices": [{"message": {"content": content}}]})
    return response


def test_empty_string_env_overrides_fall_back_to_defaults(monkeypatch):
    # A docker-compose .env file with `AI_ENDPOINT_URL=` (blank) sets the var to an
    # empty string, not unset — must still fall back to the default, not send an
    # empty URL/model.
    monkeypatch.setenv("AI_ENDPOINT_URL", "")
    monkeypatch.setenv("AI_MODEL", "")
    assert ai_service._endpoint_url() == ai_service.DEFAULT_ENDPOINT_URL
    assert ai_service._model() == ai_service.DEFAULT_MODEL


def test_generate_exploration_returns_structured_result(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    content = (
        '{"recommendation": "Explore automating the reconciliation step.", '
        '"rationale": "High frequency and consistent duration.", '
        '"verification_points": ["Check input format", "Check exception rate"]}'
    )
    with patch("app.ai_service.requests.post", return_value=_mock_openrouter_response(content)) as mock_post:
        result = ai_service.generate_exploration(TASK_CONTEXT)

    assert mock_post.called
    assert result["recommendation"] == "Explore automating the reconciliation step."
    assert result["verification_points"] == ["Check input format", "Check exception rate"]


def test_generate_exploration_raises_on_network_error(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    import requests

    with patch("app.ai_service.requests.post", side_effect=requests.ConnectionError("boom")):
        try:
            ai_service.generate_exploration(TASK_CONTEXT)
            assert False, "expected AIServiceUnavailable"
        except ai_service.AIServiceUnavailable as exc:
            assert "request failed" in str(exc)


def test_generate_exploration_strips_markdown_code_fence(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    content = (
        '```json\n{"recommendation": "x", "rationale": "y", "verification_points": ["z"]}\n```'
    )
    with patch("app.ai_service.requests.post", return_value=_mock_openrouter_response(content)):
        result = ai_service.generate_exploration(TASK_CONTEXT)
    assert result["recommendation"] == "x"
    assert result["verification_points"] == ["z"]


def test_generate_exploration_raises_on_malformed_json(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    with patch("app.ai_service.requests.post", return_value=_mock_openrouter_response("not json")):
        try:
            ai_service.generate_exploration(TASK_CONTEXT)
            assert False, "expected AIServiceUnavailable"
        except ai_service.AIServiceUnavailable as exc:
            assert "not valid JSON" in str(exc)


def test_generate_exploration_rejects_forbidden_savings_fields(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    content = (
        '{"recommendation": "x", "rationale": "y", "verification_points": [], '
        '"estimated_savings": "80 hours"}'
    )
    with patch("app.ai_service.requests.post", return_value=_mock_openrouter_response(content)):
        try:
            ai_service.generate_exploration(TASK_CONTEXT)
            assert False, "expected AIServiceUnavailable"
        except ai_service.AIServiceUnavailable as exc:
            assert "disallowed" in str(exc)


def test_generate_exploration_rejects_roi_language_in_prose(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    content = (
        '{"recommendation": "Automate this for immediate ROI.", "rationale": "y", '
        '"verification_points": []}'
    )
    with patch("app.ai_service.requests.post", return_value=_mock_openrouter_response(content)):
        try:
            ai_service.generate_exploration(TASK_CONTEXT)
            assert False, "expected AIServiceUnavailable"
        except ai_service.AIServiceUnavailable as exc:
            assert "disallowed savings/ROI framing" in str(exc)


def test_generate_exploration_rejects_missing_required_keys(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "test-key")
    content = '{"recommendation": "x"}'
    with patch("app.ai_service.requests.post", return_value=_mock_openrouter_response(content)):
        try:
            ai_service.generate_exploration(TASK_CONTEXT)
            assert False, "expected AIServiceUnavailable"
        except ai_service.AIServiceUnavailable as exc:
            assert "missing required keys" in str(exc)

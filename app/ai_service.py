"""Company AI endpoint adapter — the only module allowed to know about the
AI provider's request/response contract.

This is the sole boundary between the web app and the company-provided AI
endpoint (docs/ADR.md ADR-004). app.py must never call the provider
directly, and must never see provider-specific request/response shapes.

CONFIGURATION STATUS: as of docs/ADR.md ADR-005, this calls OpenRouter
(https://openrouter.ai) using a time-boxed company-issued API key, as a
stand-in for the company's own AI endpoint until that is provided. The
request/response mapping below is OpenRouter's documented chat-completions
contract, not a guess.

Configuration (environment variables):
    AI_ENDPOINT_URL  default: https://openrouter.ai/api/v1/chat/completions
    AI_API_KEY       required — company-issued OpenRouter key (time-boxed; rotate before expiry)
    AI_MODEL         default: anthropic/claude-sonnet-4.6

Expected structured result, per docs/PRD.md FR-010/FR-011 and docs/DATA_MODEL.md:
    {
        "recommendation": str,
        "rationale": str,
        "verification_points": list[str],
    }

The result must never include automation_score, automation_percentage,
estimated_savings, or ROI (docs/SCOPE.md, docs/DATA_MODEL.md) — enforced both
by the system prompt below and by validating the parsed result's keys.
"""

import json
import os

import requests

DEFAULT_ENDPOINT_URL = "https://openrouter.ai/api/v1/chat/completions"
# openai/gpt-4o-mini is blocked by this account's OpenRouter guardrail/allowed-providers
# setting (confirmed via a direct API call, not a guess). anthropic/claude-sonnet-4.6 is
# on the account's allowed-providers list and was verified working end-to-end (including
# through the markdown-code-fence stripping below, since this model wraps JSON in ```json
# fences despite response_format=json_object).
DEFAULT_MODEL = "anthropic/claude-sonnet-4.6"
REQUEST_TIMEOUT_SECONDS = 30

SYSTEM_PROMPT = """You help identify automation-exploration candidates for recurring business tasks.

The only data available is: how many times per week a task runs, and how many minutes each \
run takes. There is NO data on error/exception rates, approval steps, human judgment \
requirements, system integration difficulty, or implementation cost.

Because of that, you must NEVER, anywhere in your response (including inside prose fields):
- estimate time or cost savings from automating the task
- give an automation percentage or feasibility score
- give an ROI or TCO figure, or claim "immediate ROI"
- claim the task is "definitely automatable"
- use the words "ROI", "TCO", "savings", "cost reduction", or "payback" in any field

Instead, you only:
1. recommendation: what aspect of this task is worth exploring further for automation
2. rationale: why this task is worth investigating, grounded only in its frequency and \
current weekly time spent — not in projected benefits
3. verification_points: a list of 3-6 concrete things someone must check before deciding \
to automate (e.g. input format stability, exception rate, whether human judgment or \
approval is required, source-system API/export availability)

Respond with ONLY a JSON object, no other text, matching exactly this shape:
{"recommendation": "...", "rationale": "...", "verification_points": ["...", "..."]}
"""


class AIServiceUnavailable(Exception):
    """Raised when the AI exploration cannot be generated.

    Covers: missing configuration, network/provider error, malformed
    provider response. Callers must catch this and render an "AI
    unavailable" state without affecting core analytics.
    """


def is_configured() -> bool:
    return bool(os.environ.get("AI_API_KEY"))


def _endpoint_url() -> str:
    # `or` (not `.get(..., default)`) so a present-but-empty env var (e.g. an unset
    # optional override left blank in a docker-compose .env file) also falls back to
    # the default, instead of being sent as an empty URL.
    return os.environ.get("AI_ENDPOINT_URL") or DEFAULT_ENDPOINT_URL


def _model() -> str:
    return os.environ.get("AI_MODEL") or DEFAULT_MODEL


def _build_user_prompt(task_context: dict) -> str:
    return (
        f"Task: {task_context['task_name']}\n"
        f"Department: {task_context['department']}\n"
        f"Weekly runs: {task_context['weekly_runs']}\n"
        f"Minutes per run: {task_context['minutes_per_run']}\n"
        f"Current weekly effort: {task_context['weekly_minutes']} minutes "
        f"({task_context['weekly_minutes'] / 60:.1f} hours) per week"
    )


def _strip_markdown_code_fence(text: str) -> str:
    """Some models wrap JSON in ```json ... ``` despite response_format=json_object."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[: -len("```")]
        text = text.strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()
    return text


def _parse_result(raw_content: str) -> dict:
    try:
        parsed = json.loads(_strip_markdown_code_fence(raw_content))
    except (json.JSONDecodeError, TypeError) as exc:
        raise AIServiceUnavailable(f"AI response was not valid JSON: {exc}") from exc

    required_keys = {"recommendation", "rationale", "verification_points"}
    if not required_keys.issubset(parsed.keys()):
        raise AIServiceUnavailable(
            f"AI response missing required keys {required_keys - parsed.keys()}"
        )

    forbidden_keys = {
        "automation_score",
        "automation_percentage",
        "estimated_savings",
        "roi",
    }
    present_forbidden = forbidden_keys.intersection(k.lower() for k in parsed.keys())
    if present_forbidden:
        raise AIServiceUnavailable(
            f"AI response contained disallowed field(s): {present_forbidden}"
        )

    if not isinstance(parsed["verification_points"], list):
        raise AIServiceUnavailable("AI response's verification_points was not a list")

    result = {
        "recommendation": str(parsed["recommendation"]),
        "rationale": str(parsed["rationale"]),
        "verification_points": [str(point) for point in parsed["verification_points"]],
    }

    # Defense in depth: the system prompt forbids savings/ROI framing, but prompting
    # alone isn't a guarantee. Reject the response outright rather than silently display
    # text that violates docs/CONSTRAINTS.md ("ห้ามแสดงหรืออ้างว่า weekly_time คือเวลาที่
    # Automation จะประหยัดได้จริง").
    forbidden_phrases = ["roi", "tco", "cost saving", "cost reduction", "payback", "% automatable"]
    full_text = " ".join([result["recommendation"], result["rationale"], *result["verification_points"]]).lower()
    matched_phrases = [phrase for phrase in forbidden_phrases if phrase in full_text]
    if matched_phrases:
        raise AIServiceUnavailable(
            f"AI response used disallowed savings/ROI framing: {matched_phrases}"
        )

    return result


def generate_exploration(task_context: dict) -> dict:
    """Request an exploration recommendation for a task from the configured AI endpoint.

    task_context: {"task_id", "department", "task_name", "weekly_runs",
                    "minutes_per_run", "weekly_minutes"}

    Returns {"recommendation": str, "rationale": str, "verification_points": list[str]}.
    Raises AIServiceUnavailable if the endpoint is not configured or the call fails.
    """
    api_key = os.environ.get("AI_API_KEY")
    if not api_key:
        raise AIServiceUnavailable(
            "AI endpoint is not configured (AI_API_KEY is unset). Set AI_API_KEY to a "
            "company-issued key before generating explorations."
        )

    try:
        response = requests.post(
            _endpoint_url(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": _model(),
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": _build_user_prompt(task_context)},
                ],
                "response_format": {"type": "json_object"},
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AIServiceUnavailable(f"AI endpoint request failed: {exc}") from exc

    try:
        body = response.json()
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as exc:
        raise AIServiceUnavailable(f"AI endpoint returned an unexpected response shape: {exc}") from exc

    return _parse_result(content)

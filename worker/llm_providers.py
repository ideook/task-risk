import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


class ProviderError(RuntimeError):
    pass


class ScoreProvider:
    def score(
        self,
        task_statement: str,
        prompt_template: str,
        prompt_version: str,
        model_version: str,
        schema: Optional["StructuredOutputSchema"] = None,
    ) -> Dict[str, float]:
        raise NotImplementedError


@dataclass(frozen=True)
class ProviderSpec:
    provider: str
    model: str

    @property
    def label(self) -> str:
        return f"{self.provider}:{self.model}"


@dataclass(frozen=True)
class StructuredOutputSchema:
    name: str
    schema: Dict[str, Any]


@dataclass
class MockProvider(ScoreProvider):
    model: str

    def score(
        self,
        task_statement: str,
        prompt_template: str,
        prompt_version: str,
        model_version: str,
        schema: Optional[StructuredOutputSchema] = None,
    ) -> Dict[str, float]:
        seed = f"{self.model}|{model_version}|{prompt_version}|{prompt_template}|{task_statement}"
        return _mock_scores(seed, schema)


@dataclass
class OpenAIProvider(ScoreProvider):
    model: str
    api_key_env: str = "OPENAI_API_KEY"
    base_url_env: str = "LLM_OPENAI_BASE_URL"
    client: object = field(init=False, repr=False)

    def __post_init__(self) -> None:
        try:
            from openai import OpenAI
        except Exception as exc:
            raise ProviderError("Missing dependency: openai") from exc

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise ProviderError(f"Missing API key: {self.api_key_env}")
        base_url = os.getenv(self.base_url_env, "").strip() or None
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def score(
        self,
        task_statement: str,
        prompt_template: str,
        prompt_version: str,
        model_version: str,
        schema: Optional[StructuredOutputSchema] = None,
    ) -> Dict[str, float]:
        prompt = _format_prompt(prompt_template, task_statement)
        payload = {
            "model": self.model,
            "input": prompt,
            "max_output_tokens": _max_output_tokens(schema),
        }
        text_payload: Dict[str, Any] = {}
        if schema:
            text_payload["format"] = _openai_text_format(schema)
        temperature = _float_env_optional("LLM_TEMPERATURE")
        if temperature is not None:
            payload["temperature"] = temperature
        reasoning_effort = _openai_reasoning_effort(self.model)
        if reasoning_effort:
            payload["reasoning"] = {"effort": reasoning_effort}
        verbosity = _openai_text_verbosity(self.model)
        if verbosity:
            text_payload["verbosity"] = verbosity
        if text_payload:
            payload["text"] = text_payload
        response = self.client.responses.create(**payload)
        text = _extract_openai_text(response)
        if schema:
            data = _parse_json_text(text)
            return _normalize_scores(data, schema)
        return {"ai_substitution_risk": _parse_score(text)}


@dataclass
class AnthropicProvider(ScoreProvider):
    model: str
    api_key_env: str = "ANTHROPIC_API_KEY"
    client: object = field(init=False, repr=False)

    def __post_init__(self) -> None:
        try:
            import anthropic
        except Exception as exc:
            raise ProviderError("Missing dependency: anthropic") from exc

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise ProviderError(f"Missing API key: {self.api_key_env}")
        self.client = anthropic.Anthropic(api_key=api_key)

    def score(
        self,
        task_statement: str,
        prompt_template: str,
        prompt_version: str,
        model_version: str,
        schema: Optional[StructuredOutputSchema] = None,
    ) -> Dict[str, float]:
        prompt = _format_prompt(prompt_template, task_statement)

        def _call(extra_note: Optional[str] = None):
            content = prompt
            if extra_note:
                content = f"{prompt}\n\nIMPORTANT: {extra_note}"
            payload = {
                "model": self.model,
                "max_tokens": _max_output_tokens(schema),
                "temperature": _float_env("LLM_TEMPERATURE", 0.0),
                "messages": [{"role": "user", "content": content}],
            }
            if schema:
                payload["system"] = (
                    "You must call the tool and include every required field. "
                    "If a field is unknown, set it to 0 and set confidence to 0."
                )
                payload["tools"] = [
                    {
                        "name": schema.name,
                        "description": "Return task risk scores as structured JSON.",
                        "input_schema": schema.schema,
                    }
                ]
                payload["tool_choice"] = {"type": "tool", "name": schema.name}
            return self.client.messages.create(**payload)

        message = _call()
        if schema:
            tool_input = _extract_anthropic_tool_input(message, schema.name)
            if tool_input is None:
                text = _extract_anthropic_text(message)
                data = _parse_json_text(text)
            else:
                data = tool_input
            missing = _missing_required_fields(data, schema)
            if missing:
                message = _call(
                    "Return ALL required fields. Missing fields: " + ", ".join(missing)
                )
                tool_input = _extract_anthropic_tool_input(message, schema.name)
                if tool_input is None:
                    text = _extract_anthropic_text(message)
                    data = _parse_json_text(text)
                else:
                    data = tool_input
            data = _fill_missing_scores(data, schema)
            return _normalize_scores(data, schema)
        text = _extract_anthropic_text(message)
        return {"ai_substitution_risk": _parse_score(text)}


@dataclass
class LocalOpenAIProvider(ScoreProvider):
    model: str
    base_url_env: str = "LLM_LOCAL_BASE_URL"
    api_key_env: str = "LLM_LOCAL_API_KEY"
    client: object = field(init=False, repr=False)

    def __post_init__(self) -> None:
        try:
            from openai import OpenAI
        except Exception as exc:
            raise ProviderError("Missing dependency: openai") from exc

        base_url = os.getenv(self.base_url_env, "").strip()
        if not base_url:
            raise ProviderError(f"Missing base URL: {self.base_url_env}")
        api_key = os.getenv(self.api_key_env, "").strip() or "local"
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def score(
        self,
        task_statement: str,
        prompt_template: str,
        prompt_version: str,
        model_version: str,
        schema: Optional[StructuredOutputSchema] = None,
    ) -> Dict[str, float]:
        prompt = _format_prompt(prompt_template, task_statement)
        payload = {
            "model": self.model,
            "input": prompt,
            "max_output_tokens": _max_output_tokens(schema),
        }
        text_payload: Dict[str, Any] = {}
        if schema:
            text_payload["format"] = _openai_text_format(schema)
        temperature = _float_env_optional("LLM_TEMPERATURE")
        if temperature is not None:
            payload["temperature"] = temperature
        reasoning_effort = _openai_reasoning_effort(self.model)
        if reasoning_effort:
            payload["reasoning"] = {"effort": reasoning_effort}
        verbosity = _openai_text_verbosity(self.model)
        if verbosity:
            text_payload["verbosity"] = verbosity
        if text_payload:
            payload["text"] = text_payload
        response = self.client.responses.create(**payload)
        text = _extract_openai_text(response)
        if schema:
            data = _parse_json_text(text)
            return _normalize_scores(data, schema)
        return {"ai_substitution_risk": _parse_score(text)}


_PROVIDER_ALIASES = {
    "claude": "anthropic",
}

_DEFAULT_MODEL_ENV = {
    "openai": "LLM_OPENAI_MODEL",
    "anthropic": "LLM_ANTHROPIC_MODEL",
    "local": "LLM_LOCAL_MODEL",
}

_DEFAULT_MODEL_FALLBACK = {
    "openai": "gpt-5-nano",
    "anthropic": "claude-haiku-4-5",
}

_PROVIDER_CLASSES = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "local": LocalOpenAIProvider,
}

_SCORE_RE = re.compile(r"-?\d+(?:\.\d+)?")


def normalize_provider(name: str) -> str:
    key = name.strip().lower()
    return _PROVIDER_ALIASES.get(key, key)


def parse_model_spec(value: str) -> ProviderSpec:
    raw = value.strip()
    if not raw:
        raise ProviderError("Empty model spec")
    if ":" in raw:
        provider_raw, model = raw.split(":", 1)
    else:
        provider_raw, model = raw, ""
    provider = normalize_provider(provider_raw)
    if not model:
        model = _default_model_for(provider)
    if not model:
        raise ProviderError(f"Missing model for provider: {provider}")
    return ProviderSpec(provider=provider, model=model)


def _default_model_for(provider: str) -> str:
    env_key = _DEFAULT_MODEL_ENV.get(provider)
    if env_key:
        value = os.getenv(env_key, "").strip()
        if value:
            return value
    return _DEFAULT_MODEL_FALLBACK.get(provider, "")


def get_enabled_providers() -> set:
    raw = os.getenv("LLM_PROVIDERS_ENABLED", "").strip()
    if not raw:
        return set()
    return {normalize_provider(item) for item in raw.split(",") if item.strip()}


def is_provider_enabled(provider: str, enabled: Iterable[str]) -> bool:
    enabled_set = set(enabled)
    return not enabled_set or provider in enabled_set


def get_provider(spec: ProviderSpec, use_mock: bool) -> ScoreProvider:
    if use_mock:
        return MockProvider(model=spec.label)
    provider = spec.provider
    provider_class = _PROVIDER_CLASSES.get(provider)
    if not provider_class:
        raise ProviderError(f"Unknown provider: {provider}")
    return provider_class(model=spec.model)


def env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "y"}


def _format_prompt(template: str, task_statement: str) -> str:
    try:
        return template.format(task_statement=task_statement)
    except KeyError:
        return template.replace("{task_statement}", task_statement)


def _parse_score(text: Optional[str]) -> float:
    if not text:
        raise ProviderError("Empty response")
    match = _SCORE_RE.search(text.strip())
    if not match:
        raise ProviderError(f"Could not parse score from: {text}")
    score = float(match.group(0))
    if score < 0:
        score = 0.0
    if score > 100:
        score = 100.0
    return score


def _openai_text_format(schema: StructuredOutputSchema) -> Dict[str, Any]:
    return {
        "type": "json_schema",
        "name": schema.name,
        "schema": schema.schema,
        "strict": True,
    }


def _parse_json_text(text: Optional[str]) -> Dict[str, Any]:
    if not text:
        raise ProviderError("Empty response")
    value = text.strip()
    try:
        parsed = json.loads(value)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    start = value.find("{")
    end = value.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            parsed = json.loads(value[start : end + 1])
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    raise ProviderError(f"Could not parse JSON from: {value[:200]}")


def _normalize_scores(data: Dict[str, Any], schema: StructuredOutputSchema) -> Dict[str, float]:
    properties = schema.schema.get("properties", {})
    required = schema.schema.get("required") or list(properties.keys())
    scores: Dict[str, float] = {}
    for key in required:
        if key not in data:
            raise ProviderError(f"Missing field: {key}")
        value = data.get(key)
        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise ProviderError(f"Invalid value for {key}: {value}") from exc
        rules = properties.get(key, {})
        minimum = rules.get("minimum")
        maximum = rules.get("maximum")
        if minimum is not None:
            number = max(number, float(minimum))
        if maximum is not None:
            number = min(number, float(maximum))
        scores[key] = round(number, 2)
    return scores


def _missing_required_fields(data: Dict[str, Any], schema: StructuredOutputSchema) -> List[str]:
    properties = schema.schema.get("properties", {})
    required = schema.schema.get("required") or list(properties.keys())
    return [key for key in required if key not in data]


def _fill_missing_scores(data: Dict[str, Any], schema: StructuredOutputSchema) -> Dict[str, Any]:
    properties = schema.schema.get("properties", {})
    required = schema.schema.get("required") or list(properties.keys())
    filled = dict(data or {})
    for key in required:
        value = filled.get(key)
        if value is None:
            filled[key] = 0
    if "confidence" in required:
        filled["confidence"] = 0 if _missing_required_fields(data, schema) else filled.get("confidence", 0)
    return filled


def _mock_scores(seed: str, schema: Optional[StructuredOutputSchema]) -> Dict[str, float]:
    if not schema:
        digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
        return {"ai_substitution_risk": float(int(digest[:8], 16) % 101)}
    properties = schema.schema.get("properties", {})
    required = schema.schema.get("required") or list(properties.keys())
    scores: Dict[str, float] = {}
    for key in required:
        digest = hashlib.sha256(f"{seed}|{key}".encode("utf-8")).hexdigest()
        raw = int(digest[:8], 16) / 0xFFFFFFFF
        rules = properties.get(key, {})
        minimum = float(rules.get("minimum", 0.0))
        maximum = float(rules.get("maximum", 100.0))
        value = minimum + (maximum - minimum) * raw
        scores[key] = round(value, 2)
    return scores


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name, "")
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _max_output_tokens(schema: Optional[StructuredOutputSchema]) -> int:
    base = _int_env("LLM_MAX_OUTPUT_TOKENS", 16)
    if schema:
        return max(base, 128)
    return base


def _float_env(name: str, default: float) -> float:
    value = os.getenv(name, "")
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _float_env_optional(name: str) -> Optional[float]:
    value = os.getenv(name, "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _openai_reasoning_effort(model: str) -> Optional[str]:
    value = os.getenv("LLM_OPENAI_REASONING_EFFORT") or os.getenv("LLM_REASONING_EFFORT")
    if value:
        return value.strip()
    if model.startswith("gpt-5"):
        return "minimal"
    return None


def _openai_text_verbosity(model: str) -> Optional[str]:
    value = os.getenv("LLM_OPENAI_TEXT_VERBOSITY") or os.getenv("LLM_TEXT_VERBOSITY")
    if value:
        return value.strip()
    if model.startswith("gpt-5"):
        return "low"
    return None


def _get_attr(obj, name: str):
    if hasattr(obj, name):
        return getattr(obj, name)
    if isinstance(obj, dict):
        return obj.get(name)
    return None


def _extract_openai_text(response) -> str:
    text = _get_attr(response, "output_text")
    if text:
        return text
    output = _get_attr(response, "output") or []
    chunks = []
    for item in output:
        content = _get_attr(item, "content") or []
        for part in content:
            if _get_attr(part, "type") == "output_text":
                chunk = _get_attr(part, "text")
                if chunk:
                    chunks.append(str(chunk))
    return "\n".join(chunks)


def _extract_anthropic_text(message) -> str:
    content = _get_attr(message, "content") or []
    chunks = []
    for part in content:
        text = _get_attr(part, "text")
        if text:
            chunks.append(str(text))
    return "\n".join(chunks)


def _extract_anthropic_tool_input(message, tool_name: str) -> Optional[Dict[str, Any]]:
    content = _get_attr(message, "content") or []
    for part in content:
        if _get_attr(part, "type") != "tool_use":
            continue
        if _get_attr(part, "name") != tool_name:
            continue
        tool_input = _get_attr(part, "input")
        if isinstance(tool_input, dict):
            return tool_input
        if tool_input is None:
            continue
        return dict(tool_input)
    return None

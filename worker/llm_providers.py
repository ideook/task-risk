import hashlib
import os
import re
from dataclasses import dataclass, field
from typing import Iterable, Optional


class ProviderError(RuntimeError):
    pass


class ScoreProvider:
    def score(
        self,
        task_statement: str,
        prompt_template: str,
        prompt_version: str,
        model_version: str,
    ) -> float:
        raise NotImplementedError


@dataclass(frozen=True)
class ProviderSpec:
    provider: str
    model: str

    @property
    def label(self) -> str:
        return f"{self.provider}:{self.model}"


@dataclass
class MockProvider(ScoreProvider):
    model: str

    def score(
        self,
        task_statement: str,
        prompt_template: str,
        prompt_version: str,
        model_version: str,
    ) -> float:
        seed = f"{self.model}|{model_version}|{prompt_version}|{prompt_template}|{task_statement}"
        digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
        return float(int(digest[:8], 16) % 101)


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
    ) -> float:
        prompt = _format_prompt(prompt_template, task_statement)
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            max_output_tokens=_int_env("LLM_MAX_OUTPUT_TOKENS", 16),
            temperature=_float_env("LLM_TEMPERATURE", 0.0),
        )
        text = _extract_openai_text(response)
        return _parse_score(text)


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
    ) -> float:
        prompt = _format_prompt(prompt_template, task_statement)
        message = self.client.messages.create(
            model=self.model,
            max_tokens=_int_env("LLM_MAX_OUTPUT_TOKENS", 16),
            temperature=_float_env("LLM_TEMPERATURE", 0.0),
            messages=[{"role": "user", "content": prompt}],
        )
        text = _extract_anthropic_text(message)
        return _parse_score(text)


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
    ) -> float:
        prompt = _format_prompt(prompt_template, task_statement)
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            max_output_tokens=_int_env("LLM_MAX_OUTPUT_TOKENS", 16),
            temperature=_float_env("LLM_TEMPERATURE", 0.0),
        )
        text = _extract_openai_text(response)
        return _parse_score(text)


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


def _int_env(name: str, default: int) -> int:
    value = os.getenv(name, "")
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _float_env(name: str, default: float) -> float:
    value = os.getenv(name, "")
    if not value:
        return default
    try:
        return float(value)
    except ValueError:
        return default


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

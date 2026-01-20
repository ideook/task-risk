import hashlib
import os
from dataclasses import dataclass


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
class ExternalProvider(ScoreProvider):
    model: str
    api_key_env: str

    def score(
        self,
        task_statement: str,
        prompt_template: str,
        prompt_version: str,
        model_version: str,
    ) -> float:
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise ProviderError(f"Missing API key: {self.api_key_env}")
        raise ProviderError(f"Provider for {self.model} not implemented")


_PROVIDER_CONFIG = {
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "grok": "GROK_API_KEY",
}


def get_provider(model: str, use_mock: bool) -> ScoreProvider:
    model_key = model.strip().lower()
    if use_mock:
        return MockProvider(model=model_key)
    if model_key not in _PROVIDER_CONFIG:
        raise ProviderError(f"Unknown provider: {model}")
    return ExternalProvider(model=model_key, api_key_env=_PROVIDER_CONFIG[model_key])


def env_flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "y"}

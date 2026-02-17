import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock

import google.api_core.exceptions
import pytest

from bot import utils


class DummyLimiter:
    async def acquire(self):
        return None


class DummyModel:
    def __init__(self, model_name: str, text: str = "ok", raise_exhausted: bool = False):
        self.model_name = model_name
        self.text = text
        self.raise_exhausted = raise_exhausted
        self.calls = 0

    async def generate_content_async(self, *_args, **_kwargs):
        self.calls += 1
        if self.raise_exhausted:
            raise google.api_core.exceptions.ResourceExhausted("rate limit")
        usage = SimpleNamespace(prompt_token_count=1, candidates_token_count=2)
        return SimpleNamespace(text=self.text, usage_metadata=usage, prompt_feedback=None)


@pytest.mark.asyncio
async def test_analysis_task_uses_analysis_model(monkeypatch):
    analysis = DummyModel("analysis-model", text="analysis")
    transcription = DummyModel("transcription-model", text="transcription")

    utils.set_gemini_model(analysis, t_model=transcription, a_model=analysis)
    utils.model_rate_limiters = {
        utils.MODEL_KEY_ANALYSIS: DummyLimiter(),
        utils.MODEL_KEY_TRANSCRIPTION: DummyLimiter(),
    }
    monkeypatch.setattr(utils, "increment_token_usage", AsyncMock())

    text, _ = await utils.generate_gemini_response(["hello"], task_type="analysis")

    assert text == "analysis"
    assert analysis.calls == 1
    assert transcription.calls == 0


@pytest.mark.asyncio
async def test_ocr_task_uses_transcription_model(monkeypatch):
    analysis = DummyModel("analysis-model", text="analysis")
    transcription = DummyModel("transcription-model", text="ocr")

    utils.set_gemini_model(analysis, t_model=transcription, a_model=analysis)
    utils.model_rate_limiters = {
        utils.MODEL_KEY_ANALYSIS: DummyLimiter(),
        utils.MODEL_KEY_TRANSCRIPTION: DummyLimiter(),
    }
    monkeypatch.setattr(utils, "increment_token_usage", AsyncMock())

    text, _ = await utils.generate_gemini_response(["image prompt"], task_type="ocr")

    assert text == "ocr"
    assert transcription.calls == 1
    assert analysis.calls == 0


@pytest.mark.asyncio
async def test_ocr_falls_back_to_analysis_on_rate_limit(monkeypatch):
    analysis = DummyModel("analysis-model", text="fallback-analysis")
    transcription = DummyModel("transcription-model", raise_exhausted=True)

    utils.set_gemini_model(analysis, t_model=transcription, a_model=analysis)
    utils.model_rate_limiters = {
        utils.MODEL_KEY_ANALYSIS: DummyLimiter(),
        utils.MODEL_KEY_TRANSCRIPTION: DummyLimiter(),
    }
    monkeypatch.setattr(utils, "increment_token_usage", AsyncMock())
    monkeypatch.setattr(asyncio, "sleep", AsyncMock())

    text, _ = await utils.generate_gemini_response(["image prompt"], task_type="ocr")

    assert text == "fallback-analysis"
    assert transcription.calls == 6
    assert analysis.calls == 1


@pytest.mark.asyncio
async def test_json_mode_request_skips_incompatible_analysis_model(monkeypatch):
    analysis = DummyModel("analysis-model", text="analysis")
    transcription = DummyModel("transcription-model", text="json-result")

    utils.set_gemini_model(analysis, t_model=transcription, a_model=analysis)
    utils.model_rate_limiters = {
        utils.MODEL_KEY_ANALYSIS: DummyLimiter(),
        utils.MODEL_KEY_TRANSCRIPTION: DummyLimiter(),
    }
    monkeypatch.setattr(utils, "increment_token_usage", AsyncMock())

    text, _ = await utils.generate_gemini_response(
        ["json prompt"],
        task_type="analysis",
        generation_config={"response_mime_type": "application/json"},
    )

    assert text == "json-result"
    assert transcription.calls == 1
    assert analysis.calls == 0

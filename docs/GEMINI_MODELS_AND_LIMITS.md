# Gemini Models and Free-Tier Limits

Updated: 2026-02-17  
Reference: Gemini API Console screenshot (`docs/Gemini Model Rate  Limit Free Tier 17Feb.png`)

## Implemented Dual-Model Strategy

The codebase now uses a dual-model approach:

- Analysis model: `gemma-3-27b-it`
- Transcription/OCR model: `gemini-2.5-flash-lite`

Routing is task-based in `bot/utils.py` and call-site driven in `bot/handlers.py`:

- `task_type=analysis|chat|mind_map|analytics|punctuation` -> analysis model
- `task_type=ocr|transcription` -> transcription model

If the primary model is exhausted, the router retries with exponential backoff and then attempts fallback to another available model.

## Limits Used in Code

Configured from `bot/core.py` via env vars (defaults shown):

- `GEMINI_ANALYSIS_RPM=30`
- `GEMINI_ANALYSIS_RPD=1440`
- `GEMINI_TRANSCRIPTION_RPM=10`
- `GEMINI_TRANSCRIPTION_RPD=20`

These defaults are aligned with the rate limits shown in the 17 Feb console screenshot for:

- `Gemma 3 27B` (30 RPM, 1.44K RPD)
- `Gemini 2.5 Flash Lite` (10 RPM, 20 RPD)

## Operational Notes

- Token usage is logged with the actual model name used on each call.
- Feature usage is logged as `mode:task_type` to support per-task analysis.
- Rate limiting is per model bucket, not a single global bucket.

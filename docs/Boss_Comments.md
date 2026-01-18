# Boss Comments / Action Items

This document tracks high-level architectural feedback and "Boss Mode" directives. Developers should inspect this file to prioritize refactoring and feature improvements.

## Action Items

### 1. Refactor Mind Map Generation to JSON-First
*   **Date Added:** 2026-01-05
*   **Status:** [x] Dropped (Current DOT generation is stable enough)
*   **Severity:** Low (Optimizing existing flow instead)
*   **Context:**
    Currently, the app relies on the LLM to generate raw Graphviz DOT code (`handlers.py` -> `prompts.py`). This is fragile; syntax errors (missing brackets, quotes) cause the entire visualization to fail. The regex extraction is also brittle.
*   **Actionable Steps:**
    1.  **Modify Prompt (`prompts.py`)**: Update `THERAPIST_ANALYSIS_PROMPT` to request a structured JSON response (e.g., `{ "root": "topic", "nodes": [...] }`) instead of raw DOT code.
    2.  **Create Renderer (`utils.py`)**: Implement a new Python function that accepts this JSON and programmatically builds the Graphviz DOT string. This ensures 100% valid syntax every time.
    3.  **Enhance Styling**: Use the deterministic renderer to apply consistent color schemes based on sentiment (e.g., Positive=Green, Negative=Red) which are currently inconsistent in the LLM output.
    4.  **Update Handler (`handlers.py`)**: Switch the logic to parse JSON instead of regex-matching DOT markers.

---

### 2. Harden Categorization with Structured Output (JSON)
*   **Date Added:** 2026-01-05
*   **Status:** [ ] Not Started
*   **Severity:** Medium (Data Integrity)
*   **Context:**
    `CATEGORIZATION_PROMPT` relies on the model following a custom text format ("Sentiment: ..."). If the model chats (e.g., "Sure, here is the analysis: Sentiment: ..."), the regex in `handlers.py` may fail or capture unwanted text.
*   **Actionable Steps:**
    1.  **Use JSON Mode**: Request `{ "sentiment": "...", "topics": [...], "categories": [...] }`.
    2.  **Schema Enforcement**: Since using Gemini 2.5 Flash, pass the `response_schema` parameter for strict type safety.

### 3. Decouple Analysis from Visualization
*   **Date Added:** 2026-01-05
*   **Status:** [ ] Not Started
*   **Severity:** Medium (Quality Assurance)
*   **Context:**
    `THERAPIST_ANALYSIS_PROMPT` asks the model to be a "thoughtful therapist" AND a "graphviz coder" in the same breath. This context switching dilutes the quality of both the therapy depth and the code syntax.
*   **Actionable Steps:**
    1.  **Chain Calls**: Split into two distinct prompts/calls.
        *   Call 1: `Therapist Analysis` (Pure Text/JSON). Focus on empathy and insight.
        *   Call 2: `Visualization Generator` (JSON). Pass the analysis from Call 1 and ask for the mind map structure.

### 4. Enrich Audio Transcription Context
*   **Date Added:** 2026-01-05
*   **Status:** [ ] Not Started
*   **Severity:** Low (Feature Quality)
*   **Context:**
    `AUDIO_TRANSCRIPTION_PROMPT` is extremely basic ("Transcribe... accurately."). It misses opportunities for speaker identification, timestamping, or formatting specifically for a journal (e.g., "Format as a diary entry").
*   **Actionable Steps:**
    1.  **Expand Prompt**: Add instructions for distinct speakers (if applicable) or to ignore background noise.
    2.  **Format Hint**: "Transcribe this as a personal journal entry, capturing the emotional tone..."

---

### 5. Implementation of Productivity & Memory MCPs (FREE)
*   **Date Added:** 2026-01-06
*   **Status:** [ ] Not Started
*   **Severity:** Medium (Feature Growth)
*   **Context:**
    To transform the bot into an active partner, we will integrate several free MCPs. These are vetted for being 100% free for personal developer use.
*   **Actionable Items:**
    1.  **Google Calendar MCP**: Automatically schedule events based on "Goals" extracted from journal entries. Use standard Google Cloud personal quota.
    2.  **Deep Recall (Vector Search)**: Implement local RAG using **ChromaDB** and Gemini's free embedding model. This allows the bot to remember context from months ago, not just the last session.
    3.  **Task Master (Todoist)**: Route "small to-dos" from the journal directly to Todoist's free tier. Keeps the journal focused on reflection and the task list on action.
    4.  **Health Connect Sync**: (Note: Google Fit is deprecated in 2026). Use **Health Connect** (Android) or similar open proxies to pull sleep/step data. This provides physical context for emotional low/high points.

---

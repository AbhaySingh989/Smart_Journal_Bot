# Gemini API Models & Free Tier Limits

> **Refreshed on**: 2026-01-05
> **Source**: Official Google Gemini API Documentation & Release Notes

This document maps the official Google Gemini API free tier limits for relevant models and analyzes the model selection for the **Smart Journal Bot** project.

## Free Tier Limits Map

The following limits are based on Google's official documentation for the Gemini API Free Tier as of Jan 2026.

| Model | RPM (Requests Per Minute) | TPM (Tokens Per Minute) | RPD (Requests Per Day) | Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 3.0 Pro** | *Paid Tier Only* | *Paid Tier Only* | N/A | Highest reasoning, complex coding, multimodal mastery. |
| **Gemini 3.0 Flash** | *Limited Preview / Waitlist* | *Varies* | *Varies* | Next-gen speed and efficiency. Currently limited availability for API. |
| **Gemini 2.5 Pro** | 2 - 5 RPM | ~32k - 250k TPM | **50 - 100 RPD** | Complex reasoning, creative writing, deep context analysis. **Highest Quality Free Tier.** |
| **Gemini 2.5 Flash** | 10 - 15 RPM | ~1 Million TPM | **250 - 1,500 RPD** | Fast responses, chat interactions, high frequency usage. **Best Balanced Free Tier.** |
| **Gemini 2.5 Flash-Lite**| 15+ RPM | ~1 Million+ TPM | **~1,500+ RPD** | Extremely lightweight tasks, cost/latency optimization. **Highest Throughput.** |
| **Gemini 2.0 Flash-Lite**| (Legacy) | Similar to Flash | ~1,500 RPD | *Currently implemented in `bot/core.py`.* |

> **Note**: "RPM" = Requests Per Minute, "TPM" = Tokens Per Minute, "RPD" = Requests Per Day.
> Free tier data usage may be used to improve Google products.

---

## Project Context & Model Selection

### 1. Current Configuration Conflict
There is currently a discrepancy between the project's documentation and its codebase:

*   **Documentation (`Gemini.md` - Section 4.5)**:
    > *"The Gemini CLI will always use **Gemini 2.5 pro** model even if there's a latency..."*
*   **Codebase (`bot/core.py` - Line 58)**:
    ```python
    GEMINI_MODEL_NAME = 'gemini-2.0-flash-lite'
    ```

### 2. Analysis
*   **Gemini 3.0 Series**: While powerful, 3.0 Pro is paid-only for API, and 3.0 Flash API access is currently restricted/preview. Not recommended for a stable specific free-tier project yet.
*   **Gemini 2.5 Pro**: Offers the superior intelligence required for a "Smart" journal, capable of nuanced reflection and complex search/analytics. However, the **50-100 RPD limit** is very restrictive. If you chat with your journal more than 50 times a day, the bot will stop working.
*   **Gemini 2.0/2.5 Flash-Lite**: Offers high throughput (1500+ RPD) and low latency, ensuring the bot almost never hits limits. However, it may lack the depth for complex "Smart" insights compared to Pro.

### 3. Decision Framework
To resolve the conflict, a decision must be made based on expected usage:

*   **Scenario A: Quality First (Low Volume)**
    *   **Goal**: Deepest insights, most "human-like" journal partner.
    *   **Action**: Change `bot/core.py` to use `'gemini-2.5-pro'`.
    *   **Risk**: Bot stops responding after ~50 messages/day.

*   **Scenario B: Availability First (High Volume)**
    *   **Goal**: Always available, fast responses for quick logging.
    *   **Action**: Update `Gemini.md` to allow Flash/Lite models. Update `bot/core.py` to `'gemini-2.5-flash'` (Balanced) or `'gemini-2.5-flash-lite'` (Speed).

### 4. Recommendation
For a *Journal Bot* that likely involves multiple back-and-forth interactions per session (logging, reflecting, searching), **Gemini 2.5 Flash** is often the sweet spot (250-1,500 RPD) if using the Free Tier, as 50 RPD (Pro) is easily exhausted in 1-2 intense sessions.

However, if strict adherence to the **Mission Statement** in `Gemini.md` is required, the code must be updated to **Gemini 2.5 Pro**.

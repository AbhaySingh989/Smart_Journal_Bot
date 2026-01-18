# -*- coding: utf-8 -*-

# --- AI PROMPTS ---

# Prompt for adding punctuation to raw text
PUNCTUATION_PROMPT = """Please meticulously review the following raw text. Your task is to add appropriate punctuation (periods, commas, question marks, etc.), capitalization (for sentence beginnings and proper nouns), and sentence breaks to transform it into well-formatted, grammatically correct, and naturally flowing prose.
It is crucial that you preserve the original words and the core meaning of the text. Do not add or remove information.

If the input text contains lists or bullet points, ensure they are structured and formatted appropriately within the output, maintaining their original intent and hierarchy.

    Raw Text: "{raw_text}"

    Formatted Text:"""

# Prompt for transcribing audio
AUDIO_TRANSCRIPTION_PROMPT = "Transcribe the following audio file accurately."

# Prompt for categorizing journal entries
CATEGORIZATION_PROMPT = """Analyze the following journal entry:\n---\n{text}\n---\nProvide the following details based on the text:\n1. Sentiment: (Choose one: Positive, Negative, Neutral)\n2. Topics: (List 1-3 brief, comma-separated topics discussed)\n3. Categories: (Choose one or more from the list: [{categories_list}])\nFormat your response ONLY as follows, with each item on a new line:\nSentiment: [Your calculated sentiment]\nTopics: [Your calculated topics]\nCategories: [Your calculated categories]"""

# Prompt for JSON-based categorization
JSON_CATEGORIZATION_PROMPT = """Analyze the following journal entry:\n---\n{text}\n---\nProvide the sentiment (Positive, Negative, Neutral), 1-3 brief topics, and select categories from the following list: [{categories_list}].\nYour response MUST be a valid JSON object matching the requested schema."""

# Prompt for therapist-like analysis of journal entries
THERAPIST_INSIGHT_PROMPT = """Act as a thoughtful and reflective therapist. Your goal is to help {{username}} understand their own thoughts and feelings.

Analyze {{username}}'s most recent journal entry in the context of their previous entries.
- Identify recurring themes, emotional patterns, and any notable changes or progress.
- Provide structured insights and observations.
- Pose gentle, open-ended questions to encourage deeper self-reflection.
- Maintain a supportive and non-judgmental tone.
- **Do not give medical advice.**
- **Be concise**: Keep your analysis focused and avoid unnecessary verbosity.
- **Personal Touch**: Address {{username}} directly and warmly.

Here is the user's data:
{{current_entry_summary}}
{{history_context}}

**Analysis:**"""

# Prompt for generating a mind map from the analysis
MIND_MAP_GENERATOR_PROMPT = """Based on the following journal entry and therapeutic analysis, generate a mind map using Graphviz DOT language.

Your goal is to visualize the core themes, emotions, and connections identified in the analysis.

Ensure the DOT code is valid and follows the existing visual style:
- Use `rankdir=LR`.
- Use rounded boxes for nodes.
- Keep the font simple (Helvetica).

**Journal Entry:**
{{text}}

**Therapeutic Analysis:**
{{analysis}}

--- DOT START ---
digraph JournalMap {{
    rankdir=LR;
    node [shape=box, style=rounded, fontname="Helvetica", fontsize=10];
    edge [fontname="Helvetica", fontsize=9];

    /* Add your DOT code for the mind map here */
}}
--- DOT END ---
"""

# Prompt for OCR (Optical Character Recognition)
OCR_PROMPT = "Extract text accurately from this image, preserving line breaks if possible."

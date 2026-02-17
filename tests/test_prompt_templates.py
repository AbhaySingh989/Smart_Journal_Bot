from bot import prompts


def test_prompt_placeholders_are_format_ready():
    assert "{username}" in prompts.CONSOLIDATED_ANALYSIS_PROMPT
    assert "{current_entry_summary}" in prompts.CONSOLIDATED_ANALYSIS_PROMPT
    assert "{history_context}" in prompts.CONSOLIDATED_ANALYSIS_PROMPT
    assert "{text}" in prompts.MIND_MAP_GENERATOR_PROMPT
    assert "{analysis}" in prompts.MIND_MAP_GENERATOR_PROMPT

    # Guard against accidental double-brace placeholders that bypass .format()
    assert "{{username}}" not in prompts.CONSOLIDATED_ANALYSIS_PROMPT
    assert "{{current_entry_summary}}" not in prompts.CONSOLIDATED_ANALYSIS_PROMPT
    assert "{{history_context}}" not in prompts.CONSOLIDATED_ANALYSIS_PROMPT
    assert "{{text}}" not in prompts.MIND_MAP_GENERATOR_PROMPT
    assert "{{analysis}}" not in prompts.MIND_MAP_GENERATOR_PROMPT

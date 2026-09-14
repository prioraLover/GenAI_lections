# =====================================================================
# ИНТЕГРАЦИОННЫЕ ТЕСТЫ (Запускают реальную Ollama / API)
# =====================================================================
# Маркируем как 'integration', чтобы их можно было отключать
# при быстрой проверке.
# =====================================================================

@pytest.mark.integration
def test_wikipedia_russian_live():
    """
    Интеграционный тест:
    реальная Ollama → LLMAgent → WikipediaTool → Wikipedia API.
    """

    from llm_agent.core import LLMAgent

    agent = LLMAgent(
        local=True,
        ollama_model="qwen3:0.6b"
    )

    query = "Кто такой Альберт Эйнштейн?"
    response = agent.process_query(query)

    assert isinstance(response, str)
    assert len(response) > 0

    assert (
        "Эйнштейн" in response
        or "Альберт" in response
        or "Einstein" in response
    )


@pytest.mark.integration
def test_wikipedia_english_live():
    """
    Интеграционный тест:
    реальная Ollama → LLMAgent → WikipediaTool → Wikipedia API.
    """

    from llm_agent.core import LLMAgent

    agent = LLMAgent(
        local=True,
        ollama_model="qwen3:0.6b"
    )

    query = "Find information about Albert Einstein using Wikipedia."
    response = agent.process_query(query)

    assert isinstance(response, str)
    assert len(response) > 0

    assert (
        "Einstein" in response
        or "Эйнштейн" in response
        or "Альберт" in response
    )

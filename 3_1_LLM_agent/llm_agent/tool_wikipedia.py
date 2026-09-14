import requests


class WikipediaTool:
    """Инструмент для поиска и извлечения кратких выдержек из Wikipedia."""

    name = "wikipedia"
    description = (
        "Ищет информацию в Wikipedia на русском или английском языке "
        "и возвращает краткую выдержку из найденной статьи."
    )

    def use(self, query: str, language: str = "ru") -> str:
        """
        Ищет статью в Wikipedia и возвращает её краткую выдержку.

        Args:
            query: Поисковый запрос или название статьи.
            language: Язык Wikipedia: 'ru' или 'en'.

        Returns:
            Краткая выдержка из статьи или сообщение об ошибке.
        """
        try:
            if language not in ("ru", "en"):
                return (
                    "Ошибка: поддерживаются только языки "
                    "'ru' (русский) и 'en' (английский)."
                )

            print(
                f"> Выполняю поиск в Wikipedia ({language}) "
                f"по запросу: '{query}'"
            )

            # API нужной языковой версии Wikipedia
            api_url = f"https://{language}.wikipedia.org/w/api.php"

            # Сначала ищем наиболее подходящую статью
            search_params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srlimit": 1,
                "format": "json",
                "utf8": 1,
            }

            response = requests.get(
                api_url,
                params=search_params,
                timeout=10,
            )
            response.raise_for_status()

            search_data = response.json()
            search_results = search_data.get("query", {}).get("search", [])

            if not search_results:
                return (
                    f"В Wikipedia ({language}) ничего не найдено "
                    f"по запросу '{query}'."
                )

            page_title = search_results[0]["title"]

            print(f"> Найдена статья: {page_title}")

            # Получаем краткую выдержку из статьи
            extract_params = {
                "action": "query",
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
                "exchars": 1200,
                "titles": page_title,
                "format": "json",
                "utf8": 1,
            }

            response = requests.get(
                api_url,
                params=extract_params,
                timeout=10,
            )
            response.raise_for_status()

            extract_data = response.json()
            pages = extract_data.get("query", {}).get("pages", {})

            page = next(iter(pages.values()), {})
            extract = page.get("extract", "").strip()

            if not extract:
                return (
                    f"Статья '{page_title}' найдена, "
                    "но краткая выдержка отсутствует."
                )

            # Ограничиваем длину текста
            if len(extract) > 1200:
                extract = extract[:1200] + "..."

            result = (
                f"Статья Wikipedia: {page_title}\n"
                f"Язык: {language}\n\n"
                f"{extract}"
            )

            print("> Выдержка успешно получена.")

            return result

        except requests.exceptions.Timeout:
            print("> Ошибка: превышено время ожидания запроса.")
            return "Ошибка: Wikipedia не ответила вовремя."

        except requests.exceptions.RequestException as e:
            print(f"> Ошибка HTTP при обращении к Wikipedia: {e}")
            return f"Ошибка при обращении к Wikipedia: {e}"

        except Exception as e:
            print(f"> Ошибка при выполнении поиска: {e}")
            return (
                f"Произошла ошибка при поиске в Wikipedia "
                f"по запросу '{query}': {e}"
            )

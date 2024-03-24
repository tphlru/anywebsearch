from .tools import merge_results, Settings

from .engines import google_search
from .engines import qwant_search
from .engines import duck_search

possible_engines = {
    'google': google_search,
    'qwant': qwant_search,
    'duck': duck_search,  # duck is DuckDuckGo (bing engine)
}


def multi_search(query, settings: Settings = Settings()):
    for e in settings.engines:
        if e not in possible_engines.keys():
            raise ValueError(f"Invalid search engine name: {e}")

    results_lists = []
    for e in settings.engines:
        results_lists.append(possible_engines[e](query=query, lang=settings.language, settings=settings))
    if settings.merge is True:
        return merge_results(results_lists)
    return results_lists

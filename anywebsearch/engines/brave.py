from anywebsearch.tools import SearchResult, Settings, normalise_url, merge_results
from brave import Brave
import time


def brave_search(query, lang: str = None, reverse=None, offset=0, settings: Settings = Settings()):
    # Brave search API
    if lang is None:
        lang = settings.language
    try:
        brave_key = str(settings.extra.get('brave_key'))
    except KeyError:
        raise KeyError("Specify the brave_key in the settings class")
    try:
        brave = Brave(brave_key)
        sr = brave.search(
            q=query,
            count=settings.num_results,
            offset=offset if reverse else 0,
            search_lang=lang,
            result_filter='web',
            text_decorations=False,
            country=lang
        )
    except AttributeError as e:
        raise RuntimeError("Bad response! You probably provided an invalid brave_key", e)
    sr = [*sr][3][1].results  # unpack result -> WEB results field -> skip type (0) -> extract results
    sr = [
        SearchResult(result.title, result.description, normalise_url(result.url))
        for result in sr
    ]
    if not reverse and len(sr) < settings.num_results:
        i = 0
        while len(sr) < settings.num_results:
            i += 1
            sr = [*sr, *brave_search(query=query, lang=lang, reverse=sr, offset=i, settings=settings)]
            if settings.del_dups is True:
                sr = merge_results([sr])  # don't merge anything, just del dups
        sr = sr[:settings.num_results]
    return sr

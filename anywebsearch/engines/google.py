import googlesearch as gs

from anywebsearch.tools import SearchResult, Settings, normalise_url, merge_results


def google_search(query, lang: str = None, settings: Settings = Settings()):
    # Google search
    if lang is None:
        lang = settings.language
    sr = gs.search(
        query,
        advanced=True,
        num_results=(
            settings.num_results + int(settings.num_results / 4)
            if settings.del_dups is True
            else settings.num_results
        ),
        # +10 in case of duplicates, and the excess will be trimmed
        lang=lang
    )
    sr = [
        SearchResult(result.title, result.description, normalise_url(result.url))
        for result in sr
    ]
    if settings.del_dups is True:
        sr = merge_results([sr])  # don't merge anything, just del dups
    sr = sr[:settings.num_results]
    return sr

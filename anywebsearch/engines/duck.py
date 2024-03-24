from duckduckgo_search import DDGS

from anywebsearch.tools import SearchResult, Settings, normalise_url, merge_results


def duck_search(query, lang: str = None, settings: Settings = Settings()):
    # ddg search API call
    lang_codes = {
        "AR": "xa-ar",
        "AU": "au-en",
        "AT": "at-de",
        "BE": "be-fr",
        "BR": "br-pt",
        "CA": "ca-en",
        "CL": "cl-es",
        "DK": "dk-da",
        "FI": "fi-fi",
        "FR": "fr-fr",
        "DE": "de-de",
        "HK": "hk-tzh",
        "IN": "in-en",
        "ID": "id-id",
        "IT": "it-it",
        "JP": "jp-jp",
        "KR": "kr-kr",
        "MY": "my-ms",
        "MX": "mx-es",
        "NL": "nl-nl",
        "NZ": "nz-en",
        "NO": "no-no",
        "CN": "cn-zh",
        "PL": "pl-pl",
        "PT": "pt-pt",
        "PH": "ph-en",
        "RU": "ru-ru",
        "SA": "za-en",
        "ZA": None,
        "ES": "es-es",
        "SE": "se-sv",
        "CH": "ch-de",
        "TW": "tw-tzh",
        "TR": "tr-tr",
        "GB": "uk-en",
        "US": "us-en",
        "ALL": "wt-wt",
    }
    if lang is None:
        lang = settings.language
    lang = lang_codes[lang.upper()] if lang.upper() in lang_codes.keys() else "us-en"
    sr = DDGS().text(
        query,
        region=lang,
        max_results=(
            settings.num_results + int(settings.num_results / 4)
            if settings.del_dups is True
            else settings.num_results
        )
        # +25% in case of duplicates, and the excess will be trimmed
    )
    sr = [
        SearchResult(result['title'], result['body'], normalise_url(result['href']))
        for result in sr
    ]
    if settings.del_dups is True:
        sr = merge_results([sr])  # don't merge anything, just del dups
    sr = sr[:settings.num_results]
    return sr

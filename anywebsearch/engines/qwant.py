import requests

from anywebsearch.tools import SearchResult, Settings, normalise_url, random_agent, merge_results


def qwant_search(query, lang: str = None, reverse=None, offset=0, settings: Settings = Settings()):
    lang_codes = {
        "AR": None,
        "AU": "en_au",
        "AT": "de_at",
        "BE": "fr_be",
        "BR": "br_fr",
        "CA": "en_ca",
        "CL": "es_cl",
        "DK": "da_dk",
        "FI": "fi_fi",
        "FR": "fr_fr",
        "DE": "de_de",
        "HK": "zh_hk",
        "IN": None,
        "ID": None,
        "IT": "it_it",
        "JP": None,
        "KR": "ko_kr",
        "MY": "en_my",
        "MX": "es_mx",
        "NL": "nl_nl",
        "NZ": "en_nz",
        "NO": "nb_no",
        "CN": "zh_cn",
        "PL": "pl_pl",
        "PT": "pt_pt",
        "PH": None,
        "RU": None,
        "SA": None,
        "ZA": None,
        "ES": "es_es",
        "SE": "sv_se",
        "CH": "de_ch",
        "TW": "zh_tw",
        "TR": None,
        "GB": "en_gb",
        "US": "en_us",
        "ALL": None,
    }
    headers = {'User-Agent': random_agent()}
    if lang is None:
        lang = settings.language
    rlang = lang
    lang = (
        lang_codes[lang.upper()]
        if lang.upper() in lang_codes.keys() and lang_codes[lang.upper()]
        else 'ALL'
    )
    # print("Qwant used lang", lang)
    params = {
        'q': query,
        'offset': offset if reverse else 0,
        # &count is always 10
    }
    if lang != "ALL":
        params['locale'] = lang
    url = 'https://api.qwant.com/v3/search/web'  # ?q=elon%20musk&locale=de_de&offset=0
    raw_sr = requests.get(url, params=params, headers=headers)
    raw_sr.raise_for_status()
    sr = raw_sr.json()  # convert to json
    sr = sr['data']['result']['items']['mainline']  # extract results field from this complex json
    sr = [item for item in sr if item['type'] == 'web']  # extract only web results (there are also videos, ads, images)
    restructed_sr = []
    # There might be a few web blocks with items
    for block in sr:
        for item in block['items']:
            restructed_sr.append(item)
    sr = [
        SearchResult(result['title'], result['desc'], normalise_url(result['url']))
        for result in restructed_sr
    ]
    if not reverse and len(sr) < settings.num_results:
        i = 0
        while len(sr) < settings.num_results:
            i += 10
            sr = [*sr, *qwant_search(query, rlang, reverse=sr, offset=i, settings=settings)]
            if settings.del_dups is True:
                sr = merge_results([sr])  # don't merge anything, just del dups
        sr = sr[:settings.num_results]
    return sr

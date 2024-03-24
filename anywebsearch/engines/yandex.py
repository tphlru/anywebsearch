from anywebsearch.tools import SearchResult, Settings, normalise_url, merge_results, random_agent

import xmltodict
import requests


#   _      __  ____    ___    __ __        ____   _  __        ___    ___   ____   _____   ___    ____   ____   ____
#  | | /| / / / __ \  / _ \  / //_/       /  _/  / |/ /       / _ \  / _ \ / __ \ / ___/  / _ \  / __/  / __/  / __/
#  | |/ |/ / / /_/ / / , _/ / ,<         _/ /   /    /       / ___/ / , _// /_/ // (_ /  / , _/ / _/   _\ \   _\ \  
#  |__/|__/  \____/ /_/|_| /_/|_|       /___/  /_/|_/       /_/    /_/|_| \____/ \___/  /_/|_| /___/  /___/  /___/  
#                                                                                                                   

def yandex_search(query, lang: str = None, reverse=None, offset=0, settings: Settings = Settings()):
    if lang is None:
        lang = settings.language
        if lang != "ru":
            lang = "en"

    url = f"https://yandex.com/search/xml?folderid={settings.extra.get('ya_fldid')}&filter=moderate&lr=225&l10n={lang}"
    payload = """<?xml version="1.0" encoding="UTF-8"?>
    <request>
        <query>
            {query}
        </query>
        <groupings>
            <groupby attr="" mode="flat" groups-on-page="10" docs-in-group="1" />
        </groupings>
        <maxpassages>5</maxpassages>
        <page>{offset}</page>
    </request>
    """.format(query=query, offset=offset)
    print(payload)
    headers = {
        'Content-Type': 'application/xml',
        'User-Agent': random_agent(),
        'Authorization': f'Api-Key {settings.extra.get("ya_key")}'
    }
    response = requests.request("POST", url, data=payload, headers=headers, timeout=8)
    response.raise_for_status()
    sr = xmltodict.parse(response.content)

    try:
        sr = sr['yandexsearch']['response']['results']['grouping']['group']
    except KeyError as e:
        if sr['yandexsearch']['response']['error']['@code'] == '31':
            raise RuntimeError("Incorrect yandex API key or folder id")
        raise RuntimeError(e)

    sr = [group['doc'] for group in sr]
    # TODO
    sr = [
        SearchResult(
            result['title']['#text'] if type(result['title']) is dict else result['title'],
            result['passages']['passage']['#text'] if 'passages' in result and type(
                result['passages']['passage']) is dict else "no text",
            normalise_url(result['url'])
        )
        for result in sr
        if (not all(v is None for v in result))
    ]

    if not reverse and len(sr) < settings.num_results:
        i = 0
        while len(sr) < settings.num_results:
            i += 1
            sr = [*sr, *yandex_search(query, lang, reverse=sr, offset=i, settings=settings)]
        sr = sr[:settings.num_results]

    print(sr)

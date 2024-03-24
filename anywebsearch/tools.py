import re
import urllib.parse
import w3lib.url
import random


class Settings:
    def __init__(
            self,
            language: str = 'en',
            num_results: int = 20,
            merge: bool = True,
            engines: list = None,
            **kwargs
    ):
        """
        For settings only.
        When merge set True, dups will be deleted, and for multi search it will merge results as well.
        engines is a mandatory parameter for multi search - list of engines to use.
        You can set additionall settings in kwargs, like api keys (brave, yandex)
        possible:
            brave_key - brave api key
            ya_key - yandex cloud api key
            ya_fldid - yandex cloud folder id 
        """
        extra_keys = [
            'brave_key', 'ya_key', 'ya_fldid'
        ]
        # TODO: add check for possible lang codes # languages = ['en', ...]
        for k in kwargs:
            if k not in extra_keys:
                raise KeyError("Unexpected key given:", k)

        self.language = language
        self.num_results = num_results
        self.del_dups = merge  # for single search
        self.merge = merge  # for multi search
        self.engines = engines
        self.extra = kwargs


class SearchResult:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


def random_agent():
    return random.choice([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6; en-US) Gecko/20100101 Firefox/45.4',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows; U; Windows NT 6.0; x64 Trident/4.0)'
        'Mozilla/5.0 (Linux i563 x86_64; en-US) Gecko/20100101 Firefox/55.0',
        'Mozilla/5.0 (Linux i573 x86_64; en-US) Gecko/20100101 Firefox/56.9',
        'Mozilla/5.0 (Linux; Linux x86_64) Gecko/20100101 Firefox/67.2',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_2) Gecko/20130401 Firefox/68.1',
        'Mozilla/5.0 (U; Linux x86_64; en-US) Gecko/20100101 Firefox/69.5',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 9_3_8; en-US) Gecko/20100101 Firefox/68.8',

    ])


def normalise_url(url):
    url = str(url)
    # Remove the scheme (http(s)://)
    url = re.sub(r'^https?://', '', url)
    # Remove the "www" if it exists
    url = re.sub(r'^www\.', '', url)
    # add slush to the end
    url = (url + "/") if not url.endswith("/") else url
    # decode if needed 
    url = urllib.parse.unquote(url)
    # Canonicalise url
    url = w3lib.url.canonicalize_url(url)
    return url


def merge_results(res_lists: list):
    """
        Merge results from diffirent engines by unique url
    """
    merged = []
    uniq_urls = []

    for lst in res_lists:
        # print("Engine results num =", len(lst))
        for item in lst:
            if item.url not in uniq_urls:
                merged.append(item)
                uniq_urls.append(item.url)

    # print("Total num =", len(merged))
    return merged

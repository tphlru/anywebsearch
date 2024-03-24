from anywebsearch.engines import google_search
from anywebsearch import Settings
from anywebsearch import multi_search

sett = Settings(num_results=30, language='ru', engines=['yandex'], merge=True,
                ya_key="AQVNzCh0OBoUltdwxSsAdKvjpKVzziCHp6XWfLuS", ya_fldid="b1gd3a1fipj0pq2l1f8a")

t = multi_search(query="Elon Musk", settings=sett)
for i in t:
    print(i)

print(len(t))

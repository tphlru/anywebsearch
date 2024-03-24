from anywebsearch.engines import google_search
from anywebsearch import Settings
from anywebsearch import multi_search

sett = Settings(num_results=30, language='ru', engines=['qwant', 'google', 'duck'], merge=True)

t = multi_search(query="Elon Musk", settings=sett)
for i in t:
    print(i)
print(len(t))

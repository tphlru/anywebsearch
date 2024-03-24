from anywebsearch.engines import google_search
from anywebsearch import Settings

sett = Settings(num_results=30, language='ru')

for i in (google_search(query="Elon Musk", settings=sett)):
    print(vars(i))

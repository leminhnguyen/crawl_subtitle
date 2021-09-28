#%%
import bs4
import requests
import pandas as pd

# %%
def get_score_and_download_link(url):
    page_source = requests.get(url)
    soup = bs4.BeautifulSoup(page_source.text)
    try:
        sub_score = soup.find("li", class_="clearfix").a.div.span.text
    except AttributeError:
        sub_score = 0

    sub_download_link = soup.find("div", class_="download").a["href"]
    return {
        "score": int(sub_score),
        "download_link": "https://subscene.com" + sub_download_link
    }

# %%
from tqdm import tqdm

df = pd.read_csv("../assets/films_and_vietsub_links.csv")
update_infos = []

for idx in tqdm(range(len(df))):
    item = dict(df.iloc[idx])
    sub_links = eval(item["sub_links"])
    if len(sub_links) == 0:
        item["best_vietsub_link"] = ""
    else:
        sc_and_dls = []
        for link in sub_links:
            link = link["sub_link"]
            sc_and_dls.append(
                get_score_and_download_link(link)
            )
        best_vietsub_link = sorted(sc_and_dls, key=lambda x: x["score"])[-1]
        item["best_vietsub_link"] = best_vietsub_link
    update_infos.append(item)

# %%
update_infos
# %%

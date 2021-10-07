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

def get_best_link_by_score(item):
    sub_links = eval(item["sub_links"])
    if len(sub_links) == 0:
        item["best_vietsub_link"] = ""
    else:
        sc_and_dls = []
        for link in sub_links:
            sc_and_dls.append(
                {
                    **link,
                    **get_score_and_download_link(link["sub_link"])
                }
                
                
            )
        best_vietsub_link = sorted(sc_and_dls, key=lambda x: x["score"])[-1]
        item["best_vietsub_link"] = best_vietsub_link
    return item

# %%
from p_tqdm import p_map

df = pd.read_csv("../assets/films_and_vietsub_links.csv")
items = [dict(df.iloc[idx]) for idx in range(len(df))]
update_infos = p_map(get_best_link_by_score, items, num_cpus=10)

# %%
import pandas as pd
pd.DataFrame(update_infos).to_csv("../assets/final_films_and_best_vietsub_links.csv")

# %%
import requests
import os
import pandas as pd
from p_tqdm import p_map

df = pd.read_csv("../assets/final_films_and_best_vietsub_links.csv")
items = [dict(df.iloc[idx]) for idx in range(len(df))]

out_sub_dir = "/home2/nguyenlm/Projects/TTS/preprocessing/crawl_subtitle/assets/vietsub"

def download_subtitle(item):
    genre, film_name = item["type"], item["film_name"]
    genre = "_".join(genre.replace("&", "").split())
    film_name = "_".join(film_name.replace("&", "").split())
    os.makedirs(
        "{}/{}".format(out_sub_dir, genre),
        exist_ok=True
    )
    try:
        download_link = eval(item["best_vietsub_link"])["download_link"]
    except TypeError:
        item["vietsub_path"] = ""
    else:
        response = requests.get(download_link)
        if response.status_code == 200:
            out_path = "{}/{}/{}_vietsub.zip".format(out_sub_dir, genre, film_name)
            with open(out_path, "wb") as f:
                f.write(response.content)
            item["vietsub_path"] = out_path

    return item

os.system(f"rm -r {out_sub_dir}/*")
updated_items = p_map(download_subtitle, items, num_cpus=10)
updated_df = pd.DataFrame(updated_items)
# updated_df.drop(["Unnamed: 0.1.1"], axis=1, inplace=True)

# %%
updated_df.to_csv("../assets/final_films_and_best_vietsub_links.csv", index=False)

# %%

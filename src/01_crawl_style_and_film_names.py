#%%
import requests
import bs4

root_url = "https://www.rottentomatoes.com"
genre_url = "{}/top".format(root_url)
page_source = requests.get(genre_url)

# %%
## crawl all styles of film ####
document = bs4.BeautifulSoup(page_source.text)
genre_elems = document.find("ul", class_="genrelist").find_all("li")
genres = [ {"type": elem.a.div.text.strip(), "url": "{}{}".format(root_url, elem.a["href"])} for elem in genre_elems ]
genres
# %%
def extract_top_100_elements(url):
    best_100_html = requests.get(url).text
    best_100_doc = bs4.BeautifulSoup(best_100_html)
    items = list(best_100_doc.find("table", class_="table").children)
    top_100_films = []
    for item in items:
        try:
            item.strip()
        except TypeError:
            top_100_films.append(item)

    extract_100_infos = []
    for film_elem in top_100_films[1:16]:
        infos = film_elem.find_all("td")
        item = {
            "review_rating": infos[1].span.find("span", class_="tMeterScore").text.replace("\xa0", ""),
            "film_name": infos[2].a.text.strip(),
            "no_of_reviewer": infos[3].text.strip()
        }
        extract_100_infos.append(item)

    return extract_100_infos

# %%
from tqdm import tqdm
for tyle in tqdm(genres):
    url = tyle["url"]
    infos = extract_top_100_elements(url)
    tyle["films"] = infos
# %%
import pandas as pd

flatten_data = []
for item in genres:
    for film in item["films"]:
        flatten_data.append({
            "type": item["type"],
            "url": item["url"],
            **film
        })

pd.DataFrame(flatten_data).to_csv("../assets/genres_and_15_best_of_films.csv")

# %%
len(flatten_data)
# %%

#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('../assets/chromedriver/chromedriver.exe')
driver.get("https://subscene.com/")

# %%
films_df = pd.read_csv("../assets/genres_and_15_best_of_films.csv")
films_df

# %%
import requests
import bs4

def filter_good_vietsubs_v1():
    good_sub_table = driver.find_elements_by_class_name("content.clearfix")[0].find_elements_by_tag_name("table")[0]
    all_subs = good_sub_table.find_elements_by_tag_name("tbody > tr > td.a1 > a")
    vietsub_links = []
    for sub_elem in all_subs:
        sub_rate = sub_elem.find_elements_by_tag_name("span")[0].get_attribute("class")
        if "positive" in sub_rate:
            sub_link = sub_elem.get_attribute("href")
            if "vietnamese" in sub_link.lower():
                vietsub_links.append(sub_link)
    return vietsub_links

def filter_good_vietsubs_v2(list_link_url):
    page_source = requests.get(list_link_url).text
    soup = bs4.BeautifulSoup(page_source)
    sub_rows = soup.find("div", class_="content clearfix").table.tbody.find_all("tr")
    vietsub_links = []
    for sub_row in sub_rows[1:]: # ignore null first row in body
        try:
            td_tags = sub_row.find_all("td")
            sub_rate = td_tags[0].a.span["class"]
            if "positive-icon" in sub_rate: 
                sub_link = td_tags[0].a["href"]
                if "vietnamese" in sub_link.lower():
                    language = td_tags[0].a.span.text.strip()
                    author = td_tags[3].a.text.strip()
                    vietsub_links.append({
                        "sub_link": "{}{}".format("https://subscene.com/", sub_link),
                        "language": language,
                        "author": author
                    })
        except:
            pass
    return vietsub_links

def crawl_vietsub_sub_urls(film_name):
    search_bar = driver.find_element_by_id("query")
    search_bar.clear()
    search_bar.send_keys(film_name)
    search_bar.send_keys(Keys.RETURN)
    search_result = driver.find_element_by_css_selector("#left > div > div")
    ### ul and il tag in html ###
    ul_elems = search_result.find_elements_by_tag_name("ul")
    li_elems = ul_elems[0].find_elements_by_tag_name("li")
    ### the web has already sort the order of searched film by the most of subtitles, so we just need the first one ###
    sub_link = li_elems[0].find_element_by_tag_name("a").get_attribute("href")
    return filter_good_vietsubs_v2(sub_link)


# %%
### uls (ul tag in html) can be ['Exact', 'TV-Series', 'Close', 'Popular'] 
# crawl_vietsub_sub_urls(film_name="Black Panther (2018)")
from tqdm import tqdm
import time

update_film_infos = []
for idx in tqdm(range(len(films_df[:1]))):
    film_dict = dict(films_df.iloc[idx])
    print("crawling film: {}".format(film_dict["film_name"]))
    film_name = " ".join(film_dict["film_name"].split()[:-1])
    sub_links = crawl_vietsub_sub_urls(film_name=film_name)
    film_dict["sub_links"] = sub_links
    del film_dict["Unnamed: 0"]
    update_film_infos.append(film_dict)
    time.sleep(3)

# %%
pd.DataFrame(update_film_infos).to_csv("../assets/films_and_vietsub_links.csv")

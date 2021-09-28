#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# %%
driver = webdriver.Chrome('./chromedriver.exe')

# %%
driver.get("https://subscene.com/")
# %%
search_bar = driver.find_element_by_id("query")
# %%

search_bar.clear()
search_bar.send_keys("avatar")
search_bar.send_keys(Keys.RETURN)
# %%
search_result = driver.find_element_by_css_selector("#left > div > div")
# %%
uls = search_result.find_elements_by_tag_name("ul")
# %%
lis = uls[0].find_elements_by_tag_name("li")

# %%
sub_link = lis[0].find_element_by_tag_name("a")

# %%
link = sub_link.get_attribute("href")
# %%
driver.get(link)
# %%
good_sub_table = driver.find_elements_by_class_name("content.clearfix")[0].find_elements_by_tag_name("table")[0]
# %%
all_subs = good_sub_table.find_elements_by_tag_name("tbody > tr > td.a1 > a")
# %%
vietsub_links = []
for sub_elem in all_subs:
    sub_rate = sub_elem.find_elements_by_tag_name("span")[0].get_attribute("class")
    if "positive" in sub_rate:
        sub_link = sub_elem.get_attribute("href")
        if "vietnamese" in sub_link.lower():
            vietsub_links.append(sub_link)
# %%
len(vietsub_links)
# %%
driver.get(vietsub_links[0])
# %%
driver.find_element_by_id("downloadButton").get_attribute("href")
# %%

# %%
page_source = driver.page_source
# %%
page_source.find_elements_by_tag_name("clearfix")
# %%
import requests
import bs4

soup = bs4.BeautifulSoup(page_source)
# %%
download_info = soup.find("li", class_="clearfix")
download_info.a.div.span.text
# %%
download_info.find("div", class_="download").a["href"]
# %%

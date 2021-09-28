<h3 align="left">
    <p> The code for crawling the best vietnamese subtitle</p>
</h3>

## Installation

```sh
pip install -r requirements.txt
```

## Crawling Steps

### 1. Crawl the genre and popular films from [rottentomatoes](https://www.rottentomatoes.com)

```sh
python src/01_crawl_style_and_film_names.py
```

### 2. Crawl the good vietsub links for each film from [subscene](https://subscene.com/)

```sh
python src/02_crawl_best_vietsub_url.py
```

### 3. Choose the best subtitle (by score) and download with wget 

```sh
python src/03_download_best_vietsub.py
```

## Author
- [nguyenlm](https://github.com/leminhnguyen) (a passionate R&D engineer) 
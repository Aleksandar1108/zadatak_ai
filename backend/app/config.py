from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"

NAME_BASICS = DATA_DIR / "name.basics.tsv.gz"
TITLE_BASICS = DATA_DIR / "title.basics.tsv.gz"
TITLE_PRINCIPALS = DATA_DIR / "title.principals.tsv.gz"
TITLE_RATINGS = DATA_DIR / "title.ratings.tsv.gz"
MANGA_CSV = DATA_DIR / "data-manga.csv"
WALMART_CSV = DATA_DIR / "Walmart.csv"

KEANU_NCONST = "nm0000206"
TRAIN_START = "05-02-2010"
TRAIN_END = "15-02-2012"
TOP_PERCENT = 0.2
SEARCH_TERM = "svemirski vampiri"
TOP_RELATED_COUNT = 50

CACHE_FILE = CACHE_DIR / "keanu_top_movies.json"
SPACE_VAMPIRES_CACHE = CACHE_DIR / "space_vampires_matches.json"
WALMART_CACHE = CACHE_DIR / "walmart_regression.json"

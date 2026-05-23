from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"

NAME_BASICS = DATA_DIR / "name.basics.tsv.gz"
TITLE_BASICS = DATA_DIR / "title.basics.tsv.gz"
TITLE_PRINCIPALS = DATA_DIR / "title.principals.tsv.gz"
TITLE_RATINGS = DATA_DIR / "title.ratings.tsv.gz"

KEANU_NCONST = "nm0000206"
TOP_PERCENT = 0.2

CACHE_FILE = CACHE_DIR / "keanu_top_movies.json"

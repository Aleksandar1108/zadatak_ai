import csv
import gzip
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from app.config import (
    CACHE_FILE,
    KEANU_NCONST,
    TITLE_BASICS,
    TITLE_PRINCIPALS,
    TITLE_RATINGS,
    TOP_PERCENT,
)


@dataclass
class Movie:
    title: str
    tconst: str
    average_rating: float
    num_votes: int
    start_year: str | None = None


def _load_keanu_movie_ids() -> set[str]:
    movie_ids: set[str] = set()
    with gzip.open(TITLE_PRINCIPALS, "rt", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if row.get("nconst") != KEANU_NCONST:
                continue
            if row.get("category") not in {"actor", "actress", "self"}:
                continue
            movie_ids.add(row["tconst"])
    return movie_ids


def _load_ratings() -> dict[str, tuple[float, int]]:
    ratings: dict[str, tuple[float, int]] = {}
    with gzip.open(TITLE_RATINGS, "rt", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            try:
                ratings[row["tconst"]] = (
                    float(row["averageRating"]),
                    int(row["numVotes"]),
                )
            except (KeyError, ValueError):
                continue
    return ratings


def _load_keanu_movies() -> list[Movie]:
    keanu_ids = _load_keanu_movie_ids()
    ratings = _load_ratings()
    movies: list[Movie] = []

    with gzip.open(TITLE_BASICS, "rt", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            tconst = row.get("tconst", "")
            if tconst not in keanu_ids:
                continue
            if row.get("titleType") != "movie":
                continue
            if tconst not in ratings:
                continue

            start_year = row.get("startYear")
            if start_year == r"\N":
                start_year = None

            rating, votes = ratings[tconst]
            movies.append(
                Movie(
                    title=row["primaryTitle"],
                    tconst=tconst,
                    average_rating=rating,
                    num_votes=votes,
                    start_year=start_year,
                )
            )

    movies.sort(key=lambda movie: (-movie.average_rating, -movie.num_votes, movie.title))
    return movies


def _save_cache(payload: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_cache() -> dict | None:
    if not CACHE_FILE.exists():
        return None
    return json.loads(CACHE_FILE.read_text(encoding="utf-8"))


def get_top_keanu_movies(*, refresh: bool = False) -> dict:
    if not refresh:
        cached = _load_cache()
        if cached is not None:
            return cached

    all_movies = _load_keanu_movies()
    total = len(all_movies)
    top_count = max(1, math.ceil(total * TOP_PERCENT)) if total else 0
    top_movies = all_movies[:top_count]

    payload = {
        "actor": "Keanu Reeves",
        "actor_id": KEANU_NCONST,
        "total_movies": total,
        "top_percent": TOP_PERCENT,
        "top_count": top_count,
        "movies": [asdict(movie) for movie in top_movies],
    }
    _save_cache(payload)
    return payload

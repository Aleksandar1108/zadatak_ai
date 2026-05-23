import csv
import json
from dataclasses import asdict, dataclass

from app.config import MANGA_CSV, SEARCH_TERM, SPACE_VAMPIRES_CACHE, TOP_RELATED_COUNT

PREFILTER_COUNT = 800
MAX_TEXT_LENGTH = 400


@dataclass
class MangaMatch:
    title: str
    description: str
    similarity: float


def _load_manga_entries() -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    with MANGA_CSV.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            title = (row.get("title") or "").strip()
            description = (row.get("description") or "").strip()
            if not title or not description:
                continue
            entries.append((title, description))
    return entries


def _build_document(title: str, description: str) -> str:
    text = f"{title}. {description}"
    return text[:MAX_TEXT_LENGTH]


def _prefilter_candidates(entries: list[tuple[str, str]]) -> list[int]:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    documents = [_build_document(title, description) for title, description in entries]
    query = f"{SEARCH_TERM} space vampires cosmic vampires outer space sci-fi vampire"
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_df=0.95)
    matrix = vectorizer.fit_transform([query, *documents])
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
    ranked = scores.argsort()[::-1][:PREFILTER_COUNT]
    return ranked.tolist()


def _compute_matches() -> list[MangaMatch]:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    entries = _load_manga_entries()
    if not entries:
        return []

    candidate_indices = _prefilter_candidates(entries)
    candidate_entries = [entries[index] for index in candidate_indices]
    documents = [_build_document(title, description) for title, description in candidate_entries]

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    query_embedding = model.encode([SEARCH_TERM], normalize_embeddings=True)
    document_embeddings = model.encode(
        documents,
        normalize_embeddings=True,
        batch_size=64,
        show_progress_bar=False,
    )

    scores = cosine_similarity(query_embedding, document_embeddings)[0]
    ranked_indices = scores.argsort()[::-1][:TOP_RELATED_COUNT]

    matches: list[MangaMatch] = []
    for index in ranked_indices:
        title, description = candidate_entries[index]
        matches.append(
            MangaMatch(
                title=title,
                description=description,
                similarity=round(float(scores[index]), 4),
            )
        )
    return matches


def _save_cache(payload: dict) -> None:
    SPACE_VAMPIRES_CACHE.parent.mkdir(parents=True, exist_ok=True)
    SPACE_VAMPIRES_CACHE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _load_cache() -> dict | None:
    if not SPACE_VAMPIRES_CACHE.exists():
        return None
    return json.loads(SPACE_VAMPIRES_CACHE.read_text(encoding="utf-8"))


def get_space_vampire_matches(*, refresh: bool = False) -> dict:
    if not refresh:
        cached = _load_cache()
        if cached is not None:
            return cached

    entries = _load_manga_entries()
    matches = _compute_matches()
    payload = {
        "query": SEARCH_TERM,
        "source_file": MANGA_CSV.name,
        "total_scanned": len(entries),
        "result_count": len(matches),
        "results": [asdict(match) for match in matches],
    }
    _save_cache(payload)
    return payload

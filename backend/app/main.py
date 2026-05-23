from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import DATA_DIR, MANGA_CSV, TITLE_BASICS, TITLE_PRINCIPALS, TITLE_RATINGS, WALMART_CSV
from app.service import get_top_keanu_movies
from app.space_vampires_service import get_space_vampire_matches
from app.walmart_regression_service import run_walmart_regression

app = FastAPI(title="Internship Tasks API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ensure_keanu_files() -> None:
    missing = [
        path.name
        for path in (TITLE_BASICS, TITLE_PRINCIPALS, TITLE_RATINGS)
        if not path.exists()
    ]
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Missing data files in {DATA_DIR}: {', '.join(missing)}",
        )


def _ensure_manga_file() -> None:
    if not MANGA_CSV.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Missing data file in {DATA_DIR}: {MANGA_CSV.name}",
        )


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/keanu-reeves/top-movies")
def top_keanu_movies(refresh: bool = Query(False)):
    _ensure_keanu_files()
    return get_top_keanu_movies(refresh=refresh)


@app.get("/api/space-vampires/related")
def space_vampires_related(refresh: bool = Query(False)):
    _ensure_manga_file()
    return get_space_vampire_matches(refresh=refresh)


def _ensure_walmart_file() -> None:
    if not WALMART_CSV.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Missing data file in {DATA_DIR}: {WALMART_CSV.name}",
        )


@app.get("/api/walmart/regression")
def walmart_regression(refresh: bool = Query(False)):
    _ensure_walmart_file()
    return run_walmart_regression(refresh=refresh)

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import DATA_DIR, TITLE_BASICS, TITLE_PRINCIPALS, TITLE_RATINGS
from app.service import get_top_keanu_movies

app = FastAPI(title="Keanu Reeves Movies API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ensure_data_files() -> None:
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


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/keanu-reeves/top-movies")
def top_keanu_movies(refresh: bool = Query(False)):
    _ensure_data_files()
    return get_top_keanu_movies(refresh=refresh)

# Keanu Reeves — Top 20% Movies

Python program + API + React UI for the internship task.

## Task

Extract titles of the **top 20% best-rated movies** starring **Keanu Reeves** from IMDb dataset files.

## Data files (in `backend/data/`)

- `title.principals.tsv.gz` — finds Keanu's movies (`nm0000206`)
- `title.basics.tsv.gz` — movie titles and years
- `title.ratings.tsv.gz` — ratings and vote counts

## Python program (standalone)

```bash
cd backend
pip install -r requirements.txt
python run_analysis.py
```

Prints the top 20% list to the terminal. Result is also cached in `backend/cache/keanu_top_movies.json`.

## Backend API

```bash
cd backend
uvicorn app.main:app --reload
```

Endpoint:

- `GET /api/keanu-reeves/top-movies`
- `GET /api/keanu-reeves/top-movies?refresh=true` — recompute from raw files

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173

## Logic

1. Find all movies where Keanu Reeves is listed as actor in `title.principals.tsv.gz`
2. Keep only `titleType = movie` with a rating
3. Sort by `averageRating` (desc), then votes
4. Return top `ceil(total * 0.20)` movies

First run scans large `.tsv.gz` files and may take 1–2 minutes. Later requests use cache.

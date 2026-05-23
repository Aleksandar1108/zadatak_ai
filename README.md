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

## Task 2 — Svemirski vampiri (semantic search)

Extract **50 titles and descriptions** most semantically related to `"svemirski vampiri"` from `data-manga.csv`.

```bash
cd backend
python run_space_vampires.py
```

API: `GET /api/space-vampires/related`

Uses multilingual sentence embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) and cosine similarity.

First run downloads the model and may take several minutes. Results cached in `backend/cache/space_vampires_matches.json`.

## Task 3 — Walmart regression

Predict `Weekly_Sales` using: `mesec`, `Holiday_Flag`, `Temperature`, `Fuel_Price`, `CPI`, `Unemployment`, `srednja_zarada`.

- Train: `05-02-2010` to `15-02-2012`
- Test: all other rows
- Metric: MSE on test set
- Includes correlation table of all parameters

```bash
cd backend
python run_walmart_regression.py
```

API: `GET /api/walmart/regression`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173

## Komentar — najzanimljiviji deo zadatka

Za mene je bio najzahtevniji **drugi deo zadatka (semantička pretraga za „svemirski vampiri“)**.

Glavni problem je bio što `data-manga.csv` ima preko 48 hiljada redova, a svaki opis može biti dosta dugačak. Ako bih odmah pustio embedding model na celu bazu, prvi run bi trajao jako dugo i API bi praktično bio neupotrebljiv dok se ne završi računanje. Zato sam odlučio da prvo uradim **brzi TF-IDF prefilter** — izvučem nekoliko stotina kandidata koji bar u tekstualnom smislu imaju neku vezu sa temom (space, vampire, sci-fi itd.), pa tek onda na tom manjem skupu radim **semantičko rangiranje** pomoću `paraphrase-multilingual-MiniLM-L12-v2`.

Izabrao sam baš taj model jer upit dolazi na srpskom („svemirski vampiri“), a opisi u datasetu su uglavnom na engleskom — multilingual model mi deluje prirodniji izbor od običnog TF-IDF-a sam po sebi, koji ne hvata baš dobro semantiku između jezika.

Još jedna važna odluka bila je **keširanje rezultata** u `backend/cache/`. Podaci se ne menjaju svaki dan, pa nema smisla da svaki put kad neko otvori frontend ponovo računamo isto. Dug proces ostaje za prvi run ili kad korisnik eksplicitno klikne „Recompute from files“.

Kod **Task 3** sam pazio da `srednja_zarada` bude računata **samo iz train perioda**, da ne bih slučajno „procureo“ test podatke u feature engineering. To mi deluje kao mala ali bitna stvar — lako je napraviti model koji izgleda dobro, ali zapravo vara jer koristi informacije koje u realnosti ne bi imao unapred.

## Logic

1. Find all movies where Keanu Reeves is listed as actor in `title.principals.tsv.gz`
2. Keep only `titleType = movie` with a rating
3. Sort by `averageRating` (desc), then votes
4. Return top `ceil(total * 0.20)` movies

First run scans large `.tsv.gz` files and may take 1–2 minutes. Later requests use cache.

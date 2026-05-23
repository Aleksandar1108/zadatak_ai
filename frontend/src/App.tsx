import { useEffect, useState } from "react";
import { fetchTopKeanuMovies, TopMoviesResponse } from "./api";

export default function App() {
  const [data, setData] = useState<TopMoviesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load(refresh = false) {
    setLoading(true);
    setError(null);
    try {
      setData(await fetchTopKeanuMovies(refresh));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <div className="app">
      <header>
        <p className="eyebrow">Internship task</p>
        <h1>Keanu Reeves — top 20% movies</h1>
      </header>

      <div className="toolbar">
        <button type="button" onClick={() => load(false)} disabled={loading}>
          Reload
        </button>
        <button type="button" onClick={() => load(true)} disabled={loading}>
          Recompute from files
        </button>
      </div>

      {loading && <p className="status">Loading data... first run can take 1-2 minutes.</p>}
      {error && <p className="error">{error}</p>}

      {data && !loading && (
        <section className="panel">
          <div className="stats">
            <div>
              <span>Actor</span>
              <strong>{data.actor}</strong>
            </div>
            <div>
              <span>Total movies</span>
              <strong>{data.total_movies}</strong>
            </div>
            <div>
              <span>Top 20% count</span>
              <strong>{data.top_count}</strong>
            </div>
          </div>

          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Title</th>
                <th>Year</th>
                <th>Rating</th>
                <th>Votes</th>
              </tr>
            </thead>
            <tbody>
              {data.movies.map((movie, index) => (
                <tr key={movie.tconst}>
                  <td>{index + 1}</td>
                  <td>{movie.title}</td>
                  <td>{movie.start_year ?? "N/A"}</td>
                  <td>{movie.average_rating.toFixed(1)}</td>
                  <td>{movie.num_votes.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </div>
  );
}

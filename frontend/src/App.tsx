import { useEffect, useState } from "react";
import {
  fetchSpaceVampires,
  fetchTopKeanuMovies,
  fetchWalmartRegression,
  SpaceVampiresResponse,
  TopMoviesResponse,
  WalmartRegressionResponse,
} from "./api";

type Tab = "keanu" | "vampires" | "walmart";

const TAB_TITLES: Record<Tab, string> = {
  keanu: "Keanu Reeves — top 20% movies",
  vampires: "Svemirski vampiri",
  walmart: "Walmart — regresija prodaje",
};

export default function App() {
  const [tab, setTab] = useState<Tab>("keanu");
  const [keanuData, setKeanuData] = useState<TopMoviesResponse | null>(null);
  const [vampireData, setVampireData] = useState<SpaceVampiresResponse | null>(null);
  const [walmartData, setWalmartData] = useState<WalmartRegressionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadKeanu(refresh = false) {
    setLoading(true);
    setError(null);
    try {
      setKeanuData(await fetchTopKeanuMovies(refresh));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  async function loadVampires(refresh = false) {
    setLoading(true);
    setError(null);
    try {
      setVampireData(await fetchSpaceVampires(refresh));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  async function loadWalmart(refresh = false) {
    setLoading(true);
    setError(null);
    try {
      setWalmartData(await fetchWalmartRegression(refresh));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  function reload(refresh = false) {
    if (tab === "keanu") return loadKeanu(refresh);
    if (tab === "vampires") return loadVampires(refresh);
    return loadWalmart(refresh);
  }

  useEffect(() => {
    if (tab === "keanu") void loadKeanu();
    else if (tab === "vampires") void loadVampires();
    else void loadWalmart();
  }, [tab]);

  const correlationColumns =
    walmartData?.correlation_table[0]
      ? Object.keys(walmartData.correlation_table[0]).filter((key) => key !== "parameter")
      : [];

  return (
    <div className="app">
      <header>
        <p className="eyebrow">Internship task</p>
        <h1>{TAB_TITLES[tab]}</h1>
      </header>

      <div className="tabs">
        <button type="button" className={tab === "keanu" ? "tab active" : "tab"} onClick={() => setTab("keanu")}>
          Task 1
        </button>
        <button type="button" className={tab === "vampires" ? "tab active" : "tab"} onClick={() => setTab("vampires")}>
          Task 2
        </button>
        <button type="button" className={tab === "walmart" ? "tab active" : "tab"} onClick={() => setTab("walmart")}>
          Task 3
        </button>
      </div>

      <div className="toolbar">
        <button type="button" onClick={() => reload(false)} disabled={loading}>
          Reload
        </button>
        <button type="button" onClick={() => reload(true)} disabled={loading}>
          Recompute from files
        </button>
      </div>

      {loading && (
        <p className="status">
          Loading...
          {tab === "vampires" && " first run can take a few minutes."}
        </p>
      )}
      {error && <p className="error">{error}</p>}

      {tab === "keanu" && keanuData && !loading && (
        <section className="panel">
          <div className="stats">
            <div><span>Actor</span><strong>{keanuData.actor}</strong></div>
            <div><span>Total movies</span><strong>{keanuData.total_movies}</strong></div>
            <div><span>Top 20%</span><strong>{keanuData.top_count}</strong></div>
          </div>
          <table>
            <thead>
              <tr><th>#</th><th>Title</th><th>Year</th><th>Rating</th><th>Votes</th></tr>
            </thead>
            <tbody>
              {keanuData.movies.map((movie, index) => (
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

      {tab === "vampires" && vampireData && !loading && (
        <section className="panel wide">
          <div className="stats">
            <div><span>Query</span><strong>{vampireData.query}</strong></div>
            <div><span>Scanned</span><strong>{vampireData.total_scanned.toLocaleString()}</strong></div>
            <div><span>Results</span><strong>{vampireData.result_count}</strong></div>
          </div>
          <table>
            <thead>
              <tr><th>#</th><th>Title</th><th>Similarity</th><th>Description</th></tr>
            </thead>
            <tbody>
              {vampireData.results.map((item, index) => (
                <tr key={`${item.title}-${index}`}>
                  <td>{index + 1}</td>
                  <td className="title-cell">{item.title}</td>
                  <td>{item.similarity.toFixed(4)}</td>
                  <td className="description-cell">{item.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

      {tab === "walmart" && walmartData && !loading && (
        <>
          <section className="panel">
            <div className="stats">
              <div>
                <span>Train period</span>
                <strong>{walmartData.train_period.from} – {walmartData.train_period.to}</strong>
              </div>
              <div><span>Train rows</span><strong>{walmartData.train_rows}</strong></div>
              <div><span>Test rows</span><strong>{walmartData.test_rows}</strong></div>
            </div>
            <p className="mse">
              MSE (test): <strong>{walmartData.mse_test.toLocaleString()}</strong>
            </p>
            <h3>Model coefficients</h3>
            <table>
              <thead>
                <tr><th>Feature</th><th>Coefficient</th></tr>
              </thead>
              <tbody>
                {walmartData.coefficients.map((row) => (
                  <tr key={row.feature}>
                    <td>{row.feature}</td>
                    <td>{row.coefficient.toLocaleString()}</td>
                  </tr>
                ))}
                <tr>
                  <td>intercept</td>
                  <td>{walmartData.intercept.toLocaleString()}</td>
                </tr>
              </tbody>
            </table>
          </section>

          <section className="panel wide">
            <h3>Correlation table</h3>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Parameter</th>
                    {correlationColumns.map((col) => (
                      <th key={col}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {walmartData.correlation_table.map((row) => (
                    <tr key={row.parameter}>
                      <td>{row.parameter}</td>
                      {correlationColumns.map((col) => (
                        <td key={col}>{Number(row[col]).toFixed(4)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="panel wide">
            <h3>Sample test predictions</h3>
            <table>
              <thead>
                <tr>
                  <th>Store</th>
                  <th>Date</th>
                  <th>Actual</th>
                  <th>Predicted</th>
                </tr>
              </thead>
              <tbody>
                {walmartData.sample_predictions.map((row) => (
                  <tr key={`${row.store}-${row.date}`}>
                    <td>{row.store}</td>
                    <td>{row.date}</td>
                    <td>{row.actual_weekly_sales.toLocaleString()}</td>
                    <td>{row.predicted_weekly_sales.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </>
      )}
    </div>
  );
}

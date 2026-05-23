export interface Movie {
  title: string;
  tconst: string;
  average_rating: number;
  num_votes: number;
  start_year: string | null;
}

export interface TopMoviesResponse {
  actor: string;
  actor_id: string;
  total_movies: number;
  top_percent: number;
  top_count: number;
  movies: Movie[];
}

export interface MangaMatch {
  title: string;
  description: string;
  similarity: number;
}

export interface SpaceVampiresResponse {
  query: string;
  source_file: string;
  total_scanned: number;
  result_count: number;
  results: MangaMatch[];
}

export interface WalmartCoefficient {
  feature: string;
  coefficient: number;
}

export interface WalmartCorrelationRow {
  parameter: string;
  [key: string]: string | number;
}

export interface WalmartSamplePrediction {
  store: number;
  date: string;
  actual_weekly_sales: number;
  predicted_weekly_sales: number;
}

export interface WalmartRegressionResponse {
  source_file: string;
  train_period: { from: string; to: string };
  train_rows: number;
  test_rows: number;
  features: string[];
  target: string;
  mse_test: number;
  intercept: number;
  coefficients: WalmartCoefficient[];
  correlation_table: WalmartCorrelationRow[];
  sample_predictions: WalmartSamplePrediction[];
}

async function fetchApi<T>(path: string, refresh: boolean): Promise<T> {
  const query = refresh ? "?refresh=true" : "";
  const response = await fetch(`${path}${query}`);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? "Request failed");
  }
  return response.json();
}

export function fetchTopKeanuMovies(refresh = false) {
  return fetchApi<TopMoviesResponse>("/api/keanu-reeves/top-movies", refresh);
}

export function fetchSpaceVampires(refresh = false) {
  return fetchApi<SpaceVampiresResponse>("/api/space-vampires/related", refresh);
}

export function fetchWalmartRegression(refresh = false) {
  return fetchApi<WalmartRegressionResponse>("/api/walmart/regression", refresh);
}

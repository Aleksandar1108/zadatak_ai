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

export async function fetchTopKeanuMovies(refresh = false): Promise<TopMoviesResponse> {
  const query = refresh ? "?refresh=true" : "";
  const response = await fetch(`/api/keanu-reeves/top-movies${query}`);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? "Failed to load movies");
  }
  return response.json();
}

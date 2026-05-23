"""Python program: top 20% best-rated Keanu Reeves movies."""

from app.service import get_top_keanu_movies


def main() -> None:
    result = get_top_keanu_movies(refresh=True)
    print(f"Actor: {result['actor']}")
    print(f"Total movies with rating: {result['total_movies']}")
    print(f"Top {int(result['top_percent'] * 100)}% count: {result['top_count']}")
    print("-" * 60)
    for index, movie in enumerate(result["movies"], start=1):
        year = movie.get("start_year") or "N/A"
        print(
            f"{index:2}. {movie['title']} ({year}) "
            f"- rating {movie['average_rating']} ({movie['num_votes']} votes)"
        )


if __name__ == "__main__":
    main()

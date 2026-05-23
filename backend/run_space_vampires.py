"""Python program: 50 titles/descriptions most related to 'svemirski vampiri'."""

from app.space_vampires_service import get_space_vampire_matches


def main() -> None:
    result = get_space_vampire_matches(refresh=True)
    print(f"Query: {result['query']}")
    print(f"Scanned entries: {result['total_scanned']}")
    print(f"Returned: {result['result_count']}")
    print("-" * 80)
    for index, item in enumerate(result["results"], start=1):
        print(f"{index:2}. [{item['similarity']:.4f}] {item['title']}")
        print(f"    {item['description'][:220]}{'...' if len(item['description']) > 220 else ''}")
        print()


if __name__ == "__main__":
    main()

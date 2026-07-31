from search.search_engine import SearchEngine


def main():

    print("ArgusNel Search Engine")
    print("Type 'exit' to quit\n")

    engine = SearchEngine()

    while True:

        query = input("Enter query: ")

        if query.lower() == "exit":
            break

        results = engine.search(query)

        if not results:
            print("No results found\n")
            continue

        print("\nTop Results:\n")

        for i, result in enumerate(results, start=1):
            print(f"{i}. {result['title']}")
            print(result["url"])
            print(result["snippet"])
            print()


if __name__ == "__main__":
    main()
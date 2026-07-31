from search.search_engine import SearchEngine

def main():
    engine = SearchEngine()

    while True:
        query = input("Enter query: ").strip()

        if query.lower() in {"exit", "quit"}:
            print("Exiting search.")
            break

        results = engine.search(query)

        if not results:
            print("\nNo results found\n")
            continue

        print("\nTop Results:\n")

        for i, result in enumerate(results, start=1):
            print(f"{i}. {result['title']}")
            print(result["url"])
            
            if "snippet" in result:
                print(result["snippet"])
            print()

if __name__ == "__main__":
    main()
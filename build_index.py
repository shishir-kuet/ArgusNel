from indexer.index_builder import IndexBuilder
from indexer.index_storage import IndexStorage


def main():

    print("Starting index building...")

    # create index builder
    builder = IndexBuilder()

    # build inverted index
    inverted_index = builder.build()

    print("Total terms indexed:", len(inverted_index))

    # save index
    storage = IndexStorage()
    storage.save(inverted_index)

    print("Index building completed.")


if __name__ == "__main__":
    main()
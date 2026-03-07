from crawler.main_crawler import MainCrawler


def main():

    start_url = "https://en.wikipedia.org/wiki/Search_engine"

    crawler = MainCrawler(start_url)

    crawler.crawl(max_pages=5)


if __name__ == "__main__":
    main()
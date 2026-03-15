from crawler.main_crawler import MainCrawler

def main():

    seed_urls = [
        "https://www.wikipedia.org",
        "https://stackoverflow.com",
        "https://github.com",
        "https://www.reddit.com",
        "https://www.bbc.com",
        "https://news.ycombinator.com",
        "https://arxiv.org",
        "https://medium.com"
    ]

    crawler = MainCrawler(seed_urls)

    crawler.crawl(max_pages=1000, workers=15)

if __name__ == "__main__":
    main()
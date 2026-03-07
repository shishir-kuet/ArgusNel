from urllib.parse import urlparse, urlunparse


class URLNormalizer:

    def normalize(self, url):

        parsed = urlparse(url)

        scheme = parsed.scheme.lower()

        netloc = parsed.netloc.lower()

        path = parsed.path

        if path.endswith("/"):
            path = path[:-1]

        normalized_url = urlunparse(
            (scheme, netloc, path, "", "", "")
        )

        return normalized_url
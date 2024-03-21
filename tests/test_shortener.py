
from src.shortener import Shortener


class TestShortener:

    long_url = "https://www.example.com/path?q=search"
    short_base_url = "http://myurlshortener.com/"
    shortener = Shortener(short_base_url)

    def test_can_initialize_shortener(self):
        assert self.shortener is not None

    def test_can_minify_url(self):
        short_url = self.shortener.minify(self.long_url)
        assert short_url == "https://sho.rt/abc123"



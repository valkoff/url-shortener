
from src.shortener import Shortener


class TestShortener:

    long_url = "https://www.example.com/path?q=searcah"
    short_base_url = "http://myurlshortener.com/"
    shortener = Shortener(short_base_url)

    def test_can_initialize_shortener(self):
        assert self.shortener is not None

    def test_can_minify_url(self):
        short_url = self.shortener.minify(self.long_url)

        assert short_url is not None
        assert short_url.startswith(self.short_base_url)




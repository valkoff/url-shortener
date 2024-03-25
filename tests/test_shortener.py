
import unittest
from src.shortener import Shortener
from unittest.mock import MagicMock

class TestShortener(unittest.TestCase):

    short_base_url = "http://myurlshortener.com/"
    long_url = "https://www.example.com/path?q=search"
    
    def setUp(self) -> None:
        self.urls_collection_mock = MagicMock()
        self.shortener = Shortener(self.short_base_url, self.urls_collection_mock)

    def test_can_initialize_shortener(self):
        self.assertIsNotNone(self.shortener)

    def test_can_minify_url(self):
        short_url = self.shortener.minify(self.long_url)

        self.assertIsNotNone(short_url)
        self.assertTrue(short_url.startswith(self.short_base_url))
        self.assertEqual(len(short_url), len(self.short_base_url) + 6)

    def test_same_url_is_minified_to_same_hash(self):
        short_url1 = self.shortener.minify(self.long_url)
        short_url2 = self.shortener.minify(self.long_url)

        self.assertEqual(short_url1, short_url2)

    def test_different_urls_are_minified_to_different_hashes(self):
        short_url1 = self.shortener.minify(self.long_url)
        short_url2 = self.shortener.minify(self.long_url + "x")

        self.assertNotEqual(short_url1, short_url2)
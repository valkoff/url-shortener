
import time
import unittest
from src.shortener import Shortener
from unittest.mock import patch

class TestShortener(unittest.TestCase):

    long_url = "https://www.example.com/path?q=searcah"
    short_base_url = "http://myurlshortener.com/"
    shortener = Shortener(short_base_url)

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

    @patch('time.sleep', return_value=None)
    def test_expired_url_can_be_shortened_again(self, patched_time_sleep):
        short_url = self.shortener.minify(self.long_url)
        time.sleep(61)
        self.assertEqual(1, patched_time_sleep.call_count)

        self.assertEqual(self.shortener.minify(self.long_url), short_url)

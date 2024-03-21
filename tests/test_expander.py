
import time
import unittest
from src.expander import Expander
from src.shortener import Shortener
from unittest.mock import patch

class TestExpander(unittest.TestCase):

    short_url = "https://myurlshortener.com/fstp4"
    short_base_url = "http://myurlshortener.com/"
    long_url = "https://www.example.com/path?q=search"
    expander = Expander(short_base_url)

    def test_can_initialize_expander(self):
        self.assertIsNotNone(self.expander)

    def test_can_expand_url(self):
        expanded_url = self.expander.expand(self.short_url)
        self.assertIsNotNone(expanded_url)
        self.assertEqual(expanded_url, self.long_url)

    @patch('time.sleep', return_value=None)
    def test_cant_expand_exipred_url(self, patched_time_sleep):
        minifier = Shortener(self.short_base_url)
        short_url = minifier.minify(self.long_url)

        time.sleep(61)
        self.assertRaises(Exception, self.expander.expand, short_url)

    def test_cant_expand_not_shortened_url(self):
        self.assertRaises(Exception, self.expander.expand, self.short_url)
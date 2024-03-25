import unittest
from unittest.mock import MagicMock
from src.expander import Expander, InvalidURLException, URLNotFoundException

class TestExpander(unittest.TestCase):

    short_base_url = "http://myurlshortener.com/"
    long_url = "https://www.example.com/path?q=search"
    
    def setUp(self):
        self.urls_collection_mock = MagicMock()
        self.expander = Expander(self.short_base_url, self.urls_collection_mock)

    def test_can_initialize_expander(self):
        self.assertIsNotNone(self.expander)

    def test_can_expand_url(self):
        self.urls_collection_mock.find_one.return_value = {
            "hash": "fstp4",
            "url": self.long_url
        }
        
        short_url = "http://myurlshortener.com/fstp4"
        expanded_url = self.expander.expand(short_url)
        
        self.assertIsNotNone(expanded_url)
        self.assertEqual(expanded_url, self.long_url)

    def test_cant_expand_not_existing_shortened_url(self):
        self.urls_collection_mock.find_one.return_value = None
        self.assertRaises(URLNotFoundException, self.expander.expand, f"{self.short_base_url}invalid")
        
    def test_expand_invalid_shortened_url(self):
        invalid_short_url = "https://invalid.com/shortened"
        self.assertRaises(InvalidURLException, self.expander.expand, invalid_short_url)
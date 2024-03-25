import unittest
from src.shortener import Shortener
from src.hash_generator import HashGenerator
from unittest.mock import MagicMock, ANY


class TestShortener(unittest.TestCase):
    short_base_url = "http://myurlshortener.com/"
    long_url = "https://www.example.com/path?q=search"

    def setUp(self) -> None:
        self.urls_collection_mock = MagicMock()
        self.urls_collection_mock.find_one.return_value = None
        hash_generator = HashGenerator()
        self.shortener = Shortener(
            self.short_base_url, self.urls_collection_mock, hash_generator
        )

    def test_can_initialize_shortener(self):
        self.assertIsNotNone(self.shortener)

    def test_can_minify_url(self):
        short_url = self.shortener.minify(self.long_url)

        self.assertIsNotNone(short_url)
        self.assertTrue(short_url.startswith(self.short_base_url))
        self.assertEqual(len(short_url), len(self.short_base_url) + 5)

    def test_same_url_is_minified_to_same_hash(self):
        short_url1 = self.shortener.minify(self.long_url)
        self.urls_collection_mock.find_one.return_value = {
            "hash": "4a040",
            "url": self.long_url,
        }
        short_url2 = self.shortener.minify(self.long_url)

        self.assertEqual(short_url1, short_url2)

    def test_different_urls_are_minified_to_different_hashes(self):
        short_url1 = self.shortener.minify(self.long_url)
        short_url2 = self.shortener.minify(self.long_url + "x")

        self.assertNotEqual(short_url1, short_url2)

    """
    Test that the Shortener class successfully avoids hash collisions.

    This test simulates the scenario where two different URLs initially generate
    the same hash (simulating a hash collision). It verifies that the Shortener
    class can resolve this collision by generating a unique hash for each URL.
    """

    def test_hash_generation_avoids_collisions(self):
        # Mock the HashGenerator to return the same hash for the first two calls
        # (simulating a collision), and then return unique hashes for subsequent calls.
        hash_generator = MagicMock()
        hash_generator.generate.side_effect = [
            "hash",
            "hash",
            "unique_hash1",
            "unique_hash2",
        ]

        # Configure the MongoDB collection mock to simulate finding an existing document
        # on the first lookup (simulating a collision), and then no documents for subsequent lookups,
        # indicating that the generated hashes are unique.
        self.urls_collection_mock.find_one.side_effect = [
            None,
            {"url": "http//example.com/1"},
            None,
        ]

        shortener = Shortener(
            self.short_base_url, self.urls_collection_mock, hash_generator
        )

        # The first call to minify with "http//example.com/1" should return the short URL
        # with "hash" since we simulate finding an existing document.
        short_url1 = shortener.minify("http//example.com/1")

        # The second call to minify with a different URL simulates an initial collision ("hash"),
        # but should then generate a new unique hash ("unique_hash1").
        short_url2 = shortener.minify("http//example.com/2")

        # Verify that the final short URLs are different, indicating that the collision was resolved.
        self.assertNotEqual(short_url1, short_url2)

        # Verify that the HashGenerator mock was called the expected number of times.
        self.assertEqual(hash_generator.generate.call_count, 3)

        # Verify that the final documents inserted into the database have unique hashes.
        self.urls_collection_mock.insert_one.assert_any_call(
            {"hash": "hash", "url": "http//example.com/1", "createdAt": ANY}
        )
        self.urls_collection_mock.insert_one.assert_any_call(
            {"hash": "unique_hash1", "url": "http//example.com/2", "createdAt": ANY}
        )

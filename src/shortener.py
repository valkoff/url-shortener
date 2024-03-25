"""
Shortener class to generate short URLs for long URLs.
"""
from datetime import datetime, timezone
from pymongo import collection
from src.hash_generator import HashGenerator


class CannotGenerateUniqueHashException(Exception):  # pylint: disable=R0903
    """
    Exception raised when a unique hash cannot be generated for a URL.
    """


class Shortener:  # pylint: disable=R0903
    """
    A class that represents a URL shortener.

    Attributes:
        expire_after (int): The expiration time for the short URL in seconds.
        max_attempts (int): The maximum number of attempts to generate a unique hash.

    Methods:
        __init__: Initializes a Shortener instance.
        minify: Generates a short URL for a given long URL.
    """

    expire_after = 60  # 1 minute
    max_attempts = 10

    def __init__(
        self,
        base_url: str,
        urls_collection: collection.Collection,
        hash_generator: HashGenerator,
    ):
        """
        Initializes a Shortener instance.

        Args:
            base_url (str): The base URL for the short URLs.
            urls_collection (collection.Collection): The collection to store the URLs.
            hash_generator (HashGenerator): The hash generator to generate unique hashes.
        """
        self.base_url: str = base_url
        self.urls: collection.Collection = urls_collection
        self.hash_generator: HashGenerator = hash_generator

    def minify(self, url) -> str:
        """
        Generates a short URL for a given long URL.

        Args:
            url (str): The long URL to be shortened.

        Returns:
            str: The generated short URL.

        Raises:
            CannotGenerateUniqueHashException: If a unique hash cannot be generated after the
            maximum number of attempts.
        """
        # Generate a unique hash for the URL
        attempt = 0
        while attempt < self.max_attempts:
            # Generate a hash for the URL
            url_hash = self.hash_generator.generate(url, str(attempt))
            # Check if the hash already exists in the database
            document = self.urls.find_one({"hash": url_hash})
            # Hash is unique, create a new document
            if document is None:
                self._make_document(url_hash, url)
                return self._make_short_url(url_hash)
            # Hash exists and the URL is the same, return the short URL
            if document["url"] == url:
                return self._make_short_url(url_hash)

            # Hash exists but the URL is different, try again
            attempt += 1

        # Failed to generate a unique hash after the maximum number of attempts
        raise CannotGenerateUniqueHashException(
            "Cannot generate a unique hash for the URL"
        )

    def _existing_document(self, url_hash: str, url: str) -> dict:
        document = self.urls.find_one({"hash": url_hash})
        if document is not None and document["url"] == url:
            return document
        return None

    def _make_document(self, url_hash: str, url: str) -> None:
        document = {
            "hash": url_hash,
            "url": url,
            "createdAt": datetime.now(timezone.utc),
        }
        self.urls.insert_one(document)

    def _make_short_url(self, url_hash) -> str:
        return f"{self.base_url}{url_hash}"

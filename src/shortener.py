from pymongo import collection
from datetime import datetime, timezone
from .hash_generator import HashGenerator


class CannotGenerateUniqueHashException(Exception):
    pass


class Shortener:
    expire_after = 60  # 1 minute
    max_attempts = 10

    def __init__(
        self,
        base_url: str,
        urls_collection: collection.Collection,
        hash_generator: HashGenerator,
    ):
        self.base_url: str = base_url
        self.urls: collection.Collection = urls_collection
        self.hash_generator: HashGenerator = hash_generator

    def minify(self, url) -> str:
        # Generate a unique hash for the URL
        attempt = 0
        while attempt < self.max_attempts:
            # Generate a hash for the URL
            hash = self.hash_generator.generate(url, str(attempt))
            # Check if the hash already exists in the database
            document = self.urls.find_one({"hash": hash})
            # Hash is unique, create a new document
            if document is None:
                self._make_document(hash, url)
                return self._make_short_url(hash)
            # Hash exists and the URL is the same, return the short URL
            if document["url"] == url:
                return self._make_short_url(hash)

            # Hash exists but the URL is different, try again
            attempt += 1

        # Failed to generate a unique hash after the maximum number of attempts
        raise CannotGenerateUniqueHashException(
            "Cannot generate a unique hash for the URL"
        )

    def _existing_document(self, hash: str, url: str) -> dict:
        document = self.urls.find_one({"hash": hash})
        if document is not None and document["url"] == url:
            return document
        return None

    def _make_document(self, hash: str, url: str) -> None:
        document = {"hash": hash, "url": url, "createdAt": datetime.now(timezone.utc)}
        self.urls.insert_one(document)

    def _make_short_url(self, hash) -> str:
        return f"{self.base_url}{hash}"

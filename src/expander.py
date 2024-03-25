"""
Expander class for expanding shortened URLs.
"""
from pymongo import collection


class InvalidURLException(Exception):  # pylint: disable=R0903
    """
    Exception raised when an invalid URL is provided.
    """


class URLNotFoundException(Exception):  # pylint: disable=R0903
    """
    Exception raised when a URL is not found.
    """


class Expander:  # pylint: disable=R0903
    """
    Expander class is responsible for expanding shortened URLs.

    Args:
        short_base_url (str): The base URL used for shortening the URLs.
        urls_collection (collection.Collection): The collection of URLs.

    Attributes:
        short_base_url (str): The base URL used for shortening the URLs.
        urls (collection.Collection): The collection of URLs.

    Methods:
        expand(short_url: str) -> str: Expands the provided shortened URL.
        _is_url_valid(short_url: str) -> bool: Checks if the provided shortened URL is valid.
        _find_url_document(short_url: str) -> dict: Finds the URL document in the collection.

    """

    def __init__(self, short_base_url: str, urls_collection: collection.Collection):
        self.short_base_url: str = short_base_url
        self.urls: collection.Collection = urls_collection

    def expand(self, short_url: str) -> str:
        """
        Expands the provided shortened URL.

        Args:
            short_url (str): The shortened URL to be expanded.

        Returns:
            str: The expanded URL.

        Raises:
            InvalidURLException: If the provided shortened URL is not valid.
            URLNotFoundException: If the provided shortened URL does not exist.

        """
        if not self._is_url_valid(short_url):
            raise InvalidURLException("Provided shortened URL is not valid")

        url_document = self._find_url_document(short_url)
        if url_document is None:
            raise URLNotFoundException("Provided shortened URL does not exist")

        return url_document["url"]

    def _is_url_valid(self, short_url: str) -> bool:
        """
        Checks if the provided shortened URL is valid.

        Args:
            short_url (str): The shortened URL to be checked.

        Returns:
            bool: True if the shortened URL is valid, False otherwise.

        """
        return (
            short_url.startswith(self.short_base_url)
            and len(short_url) > len(self.short_base_url) + 1
        )

    def _find_url_document(self, short_url: str) -> dict:
        """
        Finds the URL document in the collection.

        Args:
            short_url (str): The shortened URL to be searched.

        Returns:
            dict: The URL document if found, None otherwise.

        """
        url_hash: str = short_url.split("/")[-1]
        return self.urls.find_one({"hash": url_hash})

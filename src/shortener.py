import os
import time
from pymongo import MongoClient
import hashlib

class Shortener:

    hash_length = 6

    def __init__(self, base_url):
        self.base_url = base_url
        self.client = MongoClient("mongodb://root:example@localhost:27017/")
        self.db = self.client["url_shortener"]
        self.urls = self.db["urls"]

    def minify(self, url):
        """
        Generate a short URL for the given URL and store the mapping in MongoDB.
        """

        # Generate a unique hash for the URL      
        hash = self._generate_hash(url)

        # Return the short URL
        return f"{self.base_url}{hash}"


    def _generate_hash(self, url):
        """
        Generate a unique hash for the given URL
        """
        return hashlib.sha256(url.encode()).hexdigest()[:self.hash_length]

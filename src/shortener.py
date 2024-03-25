from pymongo import collection
import hashlib
from datetime import datetime, timezone

class Shortener:

    hash_length = 6
    expire_after = 60 # 1 minute

    def __init__(self, base_url: str, urls_collection: collection.Collection):
        self.base_url: str = base_url
        self.urls: collection.Collection = urls_collection

    def minify(self, url) -> str:
        # Generate a unique hash for the URL      
        hash = self._generate_hash(url)
        short_url = self._make_short_url(hash)
          
        # Check if the hash already exists
        if self._shortened_url_exists(hash):
            return short_url
        
        # Store the mapping in MongoDB
        self._make_document(hash, url)

        # Return the short URL
        return short_url

    def _generate_hash(self, url):
        """
        Generate a unique hash for the given URL
        """
        return hashlib.sha256(url.encode()).hexdigest()[:self.hash_length]
    
    def _shortened_url_exists(self, hash):
        """
        Check if the short URL already exists in the database
        """
        return self.urls.find_one({"hash": hash}) is not None
    
    def _make_document(self, hash, url):
        """
        Store the document in MongoDB
        """
        document = {"hash": hash, "url": url, "createdAt": datetime.now(timezone.utc)} 
        self.urls.insert_one(document)
        
    def _make_short_url(self, hash):
        return f"{self.base_url}{hash}"
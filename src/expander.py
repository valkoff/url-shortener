from pymongo import collection

class InvalidURLException(Exception):
    pass

class URLNotFoundException(Exception):
    pass

class Expander:

    def __init__(self, short_base_url: str, urls_collection: collection.Collection):
        self.short_base_url: str = short_base_url
        self.urls: collection.Collection = urls_collection

    def expand(self, short_url: str) -> str:
        if not self._is_url_valid(short_url):
            raise InvalidURLException("Provided shortened URL is not valid")
        
        url_document = self._find_url_document(short_url)             
        if url_document is None:
            raise URLNotFoundException("Provided shortened URL does not exist")
                
        return url_document["url"]

    def _is_url_valid(self, short_url: str) -> bool:
        return short_url.startswith(self.short_base_url) and len(short_url) > len(self.short_base_url) + 1
    
    def _find_url_document(self, short_url: str) -> dict:
        hash: str = short_url.split('/')[-1]
        return self.urls.find_one({"hash": hash})
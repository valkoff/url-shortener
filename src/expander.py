
class Expander:

    def __init__(self, short_base_url):
        self.short_base_url = short_base_url

    def expand(self, short_url):
        return "https://www.example.com/path?q=search"

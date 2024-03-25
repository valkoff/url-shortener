import argparse
from shortener import Shortener
from expander import Expander
from pymongo import MongoClient

def main():
    parser = argparse.ArgumentParser(description="CLI URL Shortener Tool")
    parser.add_argument('--minify', '-m', help='Minify a URL', type=str)
    parser.add_argument('--expand', '-e', help='Expand a short URL', type=str)
    parser.add_argument('--base_url', '-b', default='http://short.url/', help='Base URL for the shortening service', type=str)

    args = parser.parse_args()

    # Istanzia il tuo Shortener con la base URL
    
    mongo_client = MongoClient("mongodb://root:example@localhost:27017/")
    db = mongo_client["url_shortener"]
    urls = db["urls"]

    # Logica per gestire i comandi
    if args.minify:
        shortener = Shortener(args.base_url, urls)
        print("Short URL:", shortener.minify(args.minify))
    elif args.expand:
        expander = Expander(args.base_url, urls)
        print("Original URL:", expander.expand(args.expand))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

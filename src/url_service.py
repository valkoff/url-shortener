"""
Description: CLI tool for URL shortening and expanding using a MongoDB database.

Returns:
    None
"""

import argparse
import os
from pymongo import MongoClient, collection
from src.shortener import Shortener
from src.expander import Expander
from src.hash_generator import HashGenerator


def main():
    """
    Parses command line arguments and executes URL shortening or expanding operations.
    """
    parser = argparse.ArgumentParser(description="CLI URL Shortener Tool")
    args = _get_args(parser)
    urls = _init_db()
    hash_generator = HashGenerator()

    if args.minify:
        shortener = Shortener(args.base_url, urls, hash_generator)
        print("Short URL:", shortener.minify(args.minify))
    elif args.expand:
        expander = Expander(args.base_url, urls)
        print("Original URL:", expander.expand(args.expand))
    else:
        parser.print_help()


def _get_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    parser.add_argument("--minify", "-m", help="Minify a URL", type=str)
    parser.add_argument("--expand", "-e", help="Expand a short URL", type=str)
    parser.add_argument(
        "--base_url",
        "-b",
        default="http://myurlshortener.com/",
        help="Base URL for the shortening service",
        type=str,
    )

    return parser.parse_args()


def _init_db() -> collection.Collection:
    mongo_username = os.getenv("MONGO_INITDB_ROOT_USERNAME", "root")
    mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "example")
    mongo_hostname = os.getenv("MONGO_HOSTNAME", "mongo")
    mongo_port = os.getenv("MONGO_PORT", "27017")
    mongo_dbname = os.getenv("MONGO_DBNAME", "url_shortener")

    url_time_to_live = int(os.getenv("URL_TIME_TO_LIVE", "60"))

    mongo_uri = (
        f"mongodb://{mongo_username}:{mongo_password}@{mongo_hostname}:{mongo_port}/"
    )
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[mongo_dbname]
    urls = db["urls"]
    urls.create_index("hash", unique=True)
    urls.create_index("createdAt", expireAfterSeconds=url_time_to_live)

    return urls


if __name__ == "__main__":
    main()

import json
import logging
import os
from datetime import datetime

import tweepy

logging.basicConfig(level=logging.INFO, format="%(message)s")


def create_api():
    if (
        "TWITTER_API_KEY" in os.environ
        and "TWITTER_API_SECRET_KEY" in os.environ
        and "TWITTER_ACCESS_TOKEN" in os.environ
        and "TWITTER_ACCESS_TOKEN_SECRET" in os.environ
    ):
        auth_data = {}
        auth_data["api_key"] = os.environ["TWITTER_API_KEY"]
        auth_data["api_secret_key"] = os.environ["TWITTER_API_SECRET_KEY"]
        auth_data["access_token"] = os.environ["TWITTER_ACCESS_TOKEN"]
        auth_data["access_token_secret"] = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
    elif os.path.isfile("auth.json"):
        with open("auth.json") as f:
            auth_data = json.load(f)
    else:
        raise OSError("Environment variables not present and auth.json not found")

    auth = tweepy.OAuthHandler(auth_data["api_key"], auth_data["api_secret_key"])
    auth.set_access_token(auth_data["access_token"], auth_data["access_token_secret"])

    return tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        retry_count=3,
        retry_delay=5,
        retry_errors=set([401, 404, 500, 503]),
    )


def delete_tweets(api, favorite_threshold=20, days=62, dry_run=True):
    n_deleted = 0
    for status in tweepy.Cursor(api.user_timeline).items():
        logging.debug(f"Examining tweet {status.id}")

        if (datetime.utcnow() - status.created_at).days <= days:
            logging.info(f"Skipping tweet (recent) {status.id}")
            continue
        if status.favorite_count > favorite_threshold:
            logging.info(f"Skipping tweet (lots of favorites) {status.id}")
            continue
        if status.favorited:
            logging.info(f"Skipping tweet (self-favorited) {status.id}")
            continue
        if dry_run:
            logging.info(f"Skipping (dry run) {status.id}")
            continue

        logging.warning(f"Deleting tweet {status.id}")
        api.destroy_status(status.id)
        n_deleted += 1
    return n_deleted


def delete_favorites(api, days=62, dry_run=True):
    me = api.me().id
    n_deleted = 0
    for status in tweepy.Cursor(api.favorites).items():
        logging.debug(f"Examining {status.id}")

        if (datetime.utcnow() - status.created_at).days <= days:
            logging.info(f"Skipping favorite (recent) {status.id}")
            continue
        if status.user.id == me:
            logging.info(f"Skipping favorite (self-favorited) {status.id}")
            continue
        if dry_run:
            logging.info(f"Skipping favorite (dry run) {status.id}")
            continue

        logging.warning(f"Deleting favorite {status.id}")
        api.destroy_favorite(status.id)
        n_deleted += 1
    return n_deleted


def main():
    api = create_api()
    logging.info(f"Deleting tweets and favorites for @{api.me().screen_name}")
    n_tweets = delete_tweets(api, dry_run=False)
    n_favorites = delete_favorites(api, dry_run=False)
    logging.info(f"Deleted {n_tweets} tweets and {n_favorites} favorites")

# Based on https://gist.github.com/chrisalbon/b9bd4a6309c9f5f5eeab41377f27a670

import json
import logging
from datetime import datetime

import tweepy

with open("auth.json") as f:
    auth_data = json.load(f)

auth = tweepy.OAuthHandler(auth_data["api_key"], auth_data["api_secret_key"])
auth.set_access_token(auth_data["access_token"], auth_data["access_token_secret"])

api = tweepy.API(
    auth,
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True,
    retry_count=3,
    retry_delay=5,
    retry_errors=set([401, 404, 500, 503]),
)


def deletetweets(favorite_threshold=20, days=62, dry_run=True):
    for status in tweepy.Cursor(api.user_timeline).items():
        logging.info(f"Examining tweet {status.id}")

        if (datetime.utcnow() - status.created_at).days <= days:
            logging.warning(f"Skipping tweet (recent) {status.id}")
            continue
        if status.favorite_count > favorite_threshold:
            logging.warning(f"Skipping tweet (lots of favorites) {status.id}")
            continue
        if status.favorited:
            logging.warning(f"Skipping tweet (self-favorited) {status.id}")
            continue
        if dry_run:
            logging.warning(f"Skipping (dry run) {status.id}")
            continue

        logging.warning(f"Deleting tweet {status.id}")
        api.destroy_status(status.id)


def deletefavorites(days=62, dry_run=True):
    me = api.me().id
    for status in tweepy.Cursor(api.favorites).items():
        logging.info(f"Examining {status.id}")

        if (datetime.utcnow() - status.created_at).days <= days:
            logging.warning(f"Skipping favorite (recent) {status.id}")
            continue
        if status.user.id == me:
            logging.warning(f"Skipping favorite (self-favorited) {status.id}")
            continue
        if dry_run:
            logging.warning(f"Skipping favorite (dry run) {status.id}")
            continue

        logging.warning(f"Deleting favorite {status.id}")
        api.destroy_favorite(status.id)


if __name__ == "__main__":
    deletetweets(dry_run=False)
    deletefavorites(dry_run=False)

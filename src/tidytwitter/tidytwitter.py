import json
import logging
import os
from datetime import datetime

import click
import tweepy


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


@click.group()
@click.version_option()
@click.option("--verbose", "-v", is_flag=True)
@click.option("--dry-run", "-n", is_flag=True)
@click.pass_context
def cli(ctx, verbose, dry_run):
    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
    else:
        logging.basicConfig(level=logging.WARN, format="%(message)s")
    ctx.obj = create_api()
    ctx.obj.dry_run = dry_run


@cli.command()
@click.option("--days", "-d", default=62)
@click.option("--favorite-threshold", "-f", default=20)
@click.pass_context
def tweets(ctx, days, favorite_threshold):
    n_deleted = 0
    for status in tweepy.Cursor(ctx.obj.user_timeline).items():
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
        if ctx.obj.dry_run:
            logging.info(f"Skipping (dry run) {status.id}")
            n_deleted += 1
            continue

        logging.warning(f"Deleting tweet {status.id}")
        ctx.obj.destroy_status(status.id)
        n_deleted += 1
    if ctx.obj.dry_run:
        logging.warn(f"Would have deleted {n_deleted} tweets (dry-run)")
    else:
        logging.warn(f"Deleted {n_deleted} tweets")


@cli.command()
@click.option("--days", "-d", default=62)
@click.pass_context
def favorites(ctx, days):
    me = ctx.obj.me().id
    n_deleted = 0
    for status in tweepy.Cursor(ctx.obj.favorites).items():
        logging.debug(f"Examining {status.id}")

        if (datetime.utcnow() - status.created_at).days <= days:
            logging.info(f"Skipping favorite (recent) {status.id}")
            continue
        if status.user.id == me:
            logging.info(f"Skipping favorite (self-favorited) {status.id}")
            continue
        if ctx.obj.dry_run:
            logging.info(f"Skipping favorite (dry run) {status.id}")
            n_deleted += 1
            continue

        logging.warning(f"Deleting favorite {status.id}")
        ctx.obj.destroy_favorite(status.id)
        n_deleted += 1
    if ctx.obj.dry_run:
        logging.warn(f"Would have deleted {n_deleted} favorites (dry-run)")
    else:
        logging.warn(f"Deleted {n_deleted} favorites")

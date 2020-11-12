import logging
from datetime import datetime

import click
import tweepy


def create_api(auth_data):
    auth = tweepy.OAuthHandler(auth_data["api_key"], auth_data["api_secret"])
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
@click.option(
    "--verbose",
    "-v",
    help="Print all items, including those that are not deleted",
    is_flag=True,
)
@click.option(
    "--dry-run",
    "-n",
    help="Print items that would have been deleted, but don't actually delete anything",
    is_flag=True,
)
@click.option("--api-key", required=True)
@click.option("--api-secret", required=True)
@click.option("--access-token", required=True)
@click.option("--access-token-secret", required=True)
@click.pass_context
def cli(
    ctx,
    verbose,
    dry_run,
    api_key,
    api_secret,
    access_token,
    access_token_secret,
):
    """
    Delete old tweets and favorites.

    All command line options can also be set via environment variables (prepend
    "TIDYTWITTER" and replace '-' with '_'). For example,
    --api-key can be set via TIDYTWITTER_API_KEY
    """
    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
    else:
        logging.basicConfig(level=logging.WARN, format="%(message)s")
    auth_data = {
        "api_key": api_key,
        "api_secret": api_secret,
        "access_token": access_token,
        "access_token_secret": access_token_secret,
    }
    ctx.obj = create_api(auth_data)
    ctx.obj.dry_run = dry_run


def main():
    cli(auto_envvar_prefix="TIDYTWITTER")


@cli.command()
@click.option(
    "--days",
    "-d",
    help="Delete tweets older than this",
    default=60,
    show_default=True,
)
@click.option(
    "--favorite-threshold",
    "-f",
    help="Do not delete tweets with more than this number of favorites",
    default=20,
    show_default=True,
)
@click.pass_obj
def tweets(api, days, favorite_threshold):
    """
    Delete favorites older than --days unless they have more than
    --favorite-threshold favorites
    """
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
        if api.dry_run:
            logging.info(f"Skipping (dry run) {status.id}")
            n_deleted += 1
            continue
        logging.warning(f"Deleting tweet {status.id}")
        api.destroy_status(status.id)
        n_deleted += 1

    if api.dry_run:
        logging.warn(f"Would have deleted {n_deleted} tweets (dry-run)")
    else:
        logging.warn(f"Deleted {n_deleted} tweets")


@cli.command()
@click.option(
    "--days",
    "-d",
    help="Delete favorites older than this",
    default=60,
    show_default=True,
)
@click.pass_obj
def favorites(api, days):
    """
    Delete favorites older than --days
    """
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
        if api.dry_run:
            logging.info(f"Skipping favorite (dry run) {status.id}")
            n_deleted += 1
            continue
        logging.warning(f"Deleting favorite {status.id}")
        api.destroy_favorite(status.id)
        n_deleted += 1

    if api.dry_run:
        logging.warn(f"Would have deleted {n_deleted} favorites (dry-run)")
    else:
        logging.warn(f"Deleted {n_deleted} favorites")

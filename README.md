# tidytwitter

Delete your old tweets and favorites using the Twitter API.

```
tidytwitter tweets
```
will delete all of your tweets except those that:

 - are older than `--days` (default: 60), or
 - have more than `--favorite_threshold` favorites (default:20), or
 - you have favorited yourself

```
tidytwitter favorites
```
will delete all your favorites except those that:

 - are older than `--days` (default: 60), or
 - are of one of your own tweets

```
tidytwitter both
```
will delete both tweets and favorites.

See `tidytwitter --help`, `tidytwitter tweets --help` and `tidytwitter favorites
--help` for more.

The idea to preserve self-favorited tweets is stolen with thanks from [a script
by Chris
Albon](https://gist.github.com/chrisalbon/b9bd4a6309c9f5f5eeab41377f27a670).

## Installation

```
pip install git+https://github.com/mikepqr/tidytwitter.git
```

Create a Twitter developer account and get the key, secret, access token and
access token secret.

You can either export those as environment variables:

```
export TIDYTWITTER_API_KEY="your_api_key"
export TIDYTWITTER_API_SECRET="your_api_secret"
export TIDYTWITTER_ACCESS_TOKEN="your_access_token"
export TIDYTWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

or pass them as command line options (`--api-key`, etc., see `--help`).

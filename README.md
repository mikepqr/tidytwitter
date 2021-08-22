# tidytwitter

Delete your old tweets and favorites using the Twitter API.

```
tidytwitter tweets
```

deletes all of your tweets that are older than --days (default: 60) except
those that you have favorited yourself or have more than --favorite-threshold
favorites (default: 20).

```
tidytwitter favorites
```
deletes all of your favorties that are older than --days (default: 60)
except those that are of your own tweets.

```
tidytwitter both
```
deletes both tweets and favorites.

See `tidytwitter --help`, `tidytwitter tweets --help` and `tidytwitter favorites
--help` for more.

The idea to preserve self-favorited tweets is stolen with thanks from [a script
by Chris
Albon](https://gist.github.com/chrisalbon/b9bd4a6309c9f5f5eeab41377f27a670).

## Installation

```
pip install tidytwitter
```

Create a new project in your [Twitter developer
account](https://developer.twitter.com/apps) and get the key, secret, access
token and access token secret.

You can either export those as environment variables:

```
export TIDYTWITTER_API_KEY="your_api_key"
export TIDYTWITTER_API_SECRET="your_api_secret"
export TIDYTWITTER_ACCESS_TOKEN="your_access_token"
export TIDYTWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

or pass them as command line options (`--api-key`, etc., see `--help`).

### Shell completion

You can optionally enable shell completion by running the appropriate command
for your shell:

```bash
eval "$(_TIDYTWITTER_COMPLETE=bash_source tidytwitter)" >> ~/.bashrc # bash
eval "$(_TIDYTWITTER_COMPLETE=zsh_source tidytwitter)" >> ~/.zshrc  # zsh
_TIDYTWITTER_COMPLETE=fish_source foo-bar > ~/.config/fish/completions/tidytwitter.fish  # fish
```

## Automation with Github

See [tidytwitter-cron](https://github.com/mikepqr/tidytwitter-cron).

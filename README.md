# tidytwitter

Delete your old tweets and favorites using the Twitter API.

```
tidytwitter tweets
```
will delete all of your tweets except those that:

 - are older than 62 days, or
 - have more than 20 favorites, or
 - you have favorited yourself

```
tidytwitter favorites
```
delete all your favorites except those that:

 - are older than 62 days, or
 - are of one of your own tweets

See `tidytwitter --help`, `tidytwitter tweets --help` and `tidytwitter favorites
--help` for more.

The idea to preserve self-favorited tweets is stolen with thanks from [a script
by Chris
Albon](https://gist.github.com/chrisalbon/b9bd4a6309c9f5f5eeab41377f27a670).

## Installation

```
pip install git+https://github.com/williamsmj/tidytwitter.git
```

Create a Twitter developer account and get the key, secret, access token and
access token secret.

You can either export those as environment variables:

```
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

Or you can put them in a file `auth.json` in the current directory:

```
{
    "api_key": "your_api_key",
    "api_secret_key": "your_api_secret",
    "access_token": "your_access_token",
    "access_token_secret": "your_access_token_secret"
}
```

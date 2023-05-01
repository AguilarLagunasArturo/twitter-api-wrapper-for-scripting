# Twitter API V1 Wrapper for Scripting
This is a bare minimum implementation so you can just use it as is or add functionality on top of it.
## Usage
**Clone repo**
```bash
git clone https://github.com/AguilarLagunasArturo/twitter-api-wrapper-for-scripting.git
cd twitter-api-wrapper-for-scripting
```

**Write script**
You need to be inside the _twitter-api-wrapper-for-scripting_ directory.
```python
# from TwitterAPI.TwitterAPIWrapper import TwitterAPI
from TwitterAPIWrapper import TwitterAPI

api = TwitterAPI(
    username = os.environ.get('TWITTER_USERNAME'),                            # Set your own
    costumer_key = os.environ.get('TWITTER_COSTUMER_API_KEY'),                # Set your own
    costumer_key_secret = os.environ.get('TWITTER_COSTUMER_API_KEY_SECRET'),  # Set your own
    access_token = os.environ.get('TWITTER_ACCESS_TOKEN'),                    # Set your own
    access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),      # Set your own
)

# Post a text tweet
api.tweet('WIP')

# Post a tweet with a single image
api.tweet_image(
    'img.png',
    # 'some text (optional)'
)

# Post a tweet with multiple images
api.tweet_image(
    [
        'img_a.png',
        'img_b.png',
        'img_c.png',
    ],
    # 'some text (optional)'
)

# Get the most recent tweets from the user's timeline
timeline_tweets = api.get_timeline_tweets(count=5)
print(timeline_tweets)

# Search for tweets containing a specific keyword
search_results = api.search_tweets(query='Python', count=5)
print(search_results)

# Get user information
user_info = api.get_user_info()
print(user_info)

# Reply to a tweet
tweet_id = '123456789012345678'  # Replace with a valid tweet ID
api.reply_to_tweet(tweet_id, 'This is a reply to the tweet.')
```

## Demos
|File|Description|
|:-|:-|
|tweet.py|Tweets a string of text|
|tweet_image.py|Tweets a single image and a list of images|
|twitter_analizer.py|Analize your account tweets and suggests hashtags by topic|
|get_timeline.py|Query your timeline|
|get_tweets.py|Search tweets|
|get_user_info.py|Get your user profile info|

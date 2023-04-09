import os
# from TwitterAPI.TwitterAPIWrapper import TwitterAPI
from TwitterAPIWrapper import TwitterAPI

# Usage example
if __name__ == '__main__':
    api = TwitterAPI(
        username = os.environ.get('TWITTER_USERNAME'),
        costumer_key = os.environ.get('TWITTER_COSTUMER_API_KEY'),
        costumer_key_secret = os.environ.get('TWITTER_COSTUMER_API_KEY_SECRET'),
        access_token = os.environ.get('TWITTER_ACCESS_TOKEN'),
        access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
    )

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

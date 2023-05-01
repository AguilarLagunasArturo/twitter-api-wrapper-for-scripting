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

    # Post a text tweet
    info = api.get_user_info()
    print(info)

import os
import time
import requests
import urllib.parse
from dateutil import parser
from collections import Counter
from requests_oauthlib import OAuth1

class TwitterAPI:
    def __init__(self, username=None, costumer_key=None, costumer_key_secret=None, access_token=None, access_token_secret=None):
        self.twitter_username = username
        self.api_costumer_key = costumer_key
        self.api_costumer_key_secret = costumer_key_secret
        self.api_access_token = access_token
        self.api_access_token_secret = access_token_secret
        self.auth = OAuth1(
            self.api_costumer_key,
            self.api_costumer_key_secret,
            self.api_access_token,
            self.api_access_token_secret
        )
        self.__max_length = 280

    def tweet(self, text):
        if len(text) > self.__max_length:
            raise Exception(f'Max length reached: {self.__max_length}')
        url = 'https://api.twitter.com/1.1/statuses/update.json?status={}'.format(urllib.parse.quote(text))
        r = requests.post(url, auth=self.auth)
        if r.ok:
            return True
        else:
            raise Exception(f'Error while tweeting -> status code: {r.status_code}')

    def tweet_image(self, image_paths, text=''):
        if len(text) > self.__max_length:
            raise Exception(f'Max length for text reached: {self.max_length}')

        if not isinstance(image_paths, (list, tuple)):
            image_paths = [image_paths]

        url_media = 'https://upload.twitter.com/1.1/media/upload.json'
        media_ids = []

        for i, image_path in enumerate(image_paths):
            with open(image_path, 'rb') as file:
                files = {'media': file}
                r = requests.post(url_media, auth=self.auth, files=files)

            if r.ok:
                media_id = r.json()['media_id_string']
                media_ex = r.json()['expires_after_secs']
                # print(f'[+] Image {i+1} media id {media_id} expires in {media_ex}s')
                media_ids.append(media_id)
            else:
                raise Exception(f'Status code {r.status_code} for image {i+1} -> {image_path}')

        url = 'https://api.twitter.com/1.1/statuses/update.json'
        params = {'status': text, 'media_ids': ','.join(media_ids)}
        r = requests.post(url, auth=self.auth, params=params)
        if r.ok:
            return True
        else:
            raise Exception(f'Error while posting media -> status code: {r.status_code}')

    def get_timeline_tweets(self, count=20):
        url = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        params = {'count': count}
        r = requests.get(url, auth=self.auth, params=params)
        if r.ok:
            return r.json()
        else:
            raise Exception(f'Error fetching timeline tweets -> status code: {r.status_code}')

    def search_tweets(self, query, count=15, result_type='popular'):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        params = {'q': query, 'count': count, 'result_type':result_type}
        r = requests.get(url, auth=self.auth, params=params)
        if r.ok:
            return r.json()['statuses']
        else:
            raise Exception(f'Error searching tweets -> status code: {r.status_code}')

    def get_user_info(self, username=None):
        if username is None:
            username = self.twitter_username
        url = 'https://api.twitter.com/1.1/users/show.json'
        params = {'screen_name': username}
        r = requests.get(url, auth=self.auth, params=params)
        if r.ok:
            return r.json()
        else:
            raise Exception(f'Error fetching user information -> status code: {r.status_code}')

    def reply_to_tweet(self, tweet_id, text):
        if len(text) > self.max_length:
            raise Exception(f'Max length for text reached: {self.max_length}')
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        params = {'status': text, 'in_reply_to_status_id': tweet_id}
        r = requests.post(url, auth=self.auth, params=params)
        if r.ok:
            return r.json()
        else:
            raise Exception(f'Error replying to tweet -> status code: {r.status_code}')

    def extract_hashtags(self, tweet):
        return [hashtag['text'] for hashtag in tweet['entities']['hashtags']]

    def get_trending_hashtags(self, topics, count=100, result_type='popular'):
        trending_hashtags = {}

        for topic in topics:
            tweets = self.search_tweets(topic, count=count, result_type=result_type)
            hashtags = []
            for tweet in tweets:
                hashtags.extend(self.extract_hashtags(tweet))

            hashtag_counts = Counter(hashtags)
            trending_hashtags[topic] = hashtag_counts.most_common()

        return trending_hashtags

    def get_user_tweets(self, username=None, count=200):
        if username is None:
            username = self.twitter_username

        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        params = {'screen_name': username, 'count': count, 'tweet_mode': 'extended'}
        r = requests.get(url, auth=self.auth, params=params)
        if r.ok:
            return r.json()
        else:
            raise Exception(f'Error fetching user tweets -> status code: {r.status_code}')

    def analyze_tweets(self, count=200, username=None):
        if username is None:
            username = self.twitter_username

        tweets = self.get_user_tweets(username, count=count)

        tweet_reach = []
        interactions_by_hour = Counter()

        for tweet in tweets:
            reach = tweet['retweet_count'] + tweet['favorite_count']
            tweet_reach.append((tweet['id'], reach, parser.parse(tweet['created_at']).hour))

            tweet_hour = parser.parse(tweet['created_at']).hour
            interactions_by_hour[tweet_hour] += reach

        sorted_tweet_reach = sorted(tweet_reach, key=lambda x: x[1], reverse=True)

        peak_time_counter = interactions_by_hour

        return sorted_tweet_reach, peak_time_counter

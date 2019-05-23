from tweepy import API
from tweepy import OAuthHandler

import credentials

import tweepy
import numpy as np
import pandas as pd
import json
import time

# # # # TWITTER AUTHENTICATOR # # # #


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY,credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_KEY,credentials.ACCESS_SECRET)
        return auth

 # # # # # TWITTER CLIENT # # # # # #


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        # self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

class TweetAnalyzer():
    '''
    Functionality for analyzing and categorizing content from tweets.
    '''
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['hashtags'] = np.array([tweet.entities['hashtags'][0]['text'] if tweet.entities['hashtags'] else None for tweet in tweets])

        return df


if __name__ == '__main__':
    # initialize class objects
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    # create API object with authentication
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name='Neelofa')
    print(tweets)

    tweet_df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(tweet_df)
    print(dir(tweets[0]))
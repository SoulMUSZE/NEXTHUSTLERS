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
        df['hashtags'] = np.array([tweet.entities['hashtags'][0]['text'] if tweet.entities['hashtags'] else '-' for tweet in tweets])

        return df


def run_hashtag_scrap(name):
    # initialize class objects
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    # create API object with authentication
    api = twitter_client.get_twitter_client_api()

    #specify the number of pages of user_timeline to scrape for tweets 
    num_pages = 20
    user = name

    tweets_list = []
    for i in range(1, num_pages + 1):
        timeline_tweets = api.user_timeline(screen_name = user, page = i)
        tweets_list.append(timeline_tweets)

    #flatten the list of lists
    tweets = [val for sublist in tweets_list for val in sublist]
    # print(len(tweets))
    
    tweet_df = tweet_analyzer.tweets_to_data_frame(tweets)
    filtered_tweets = filter(lambda x: x[2] != '-', tweet_df.values.tolist())
   
    return [(tweet[0], tweet[1], tweet[2]) for tweet in filtered_tweets]
    
# run_hashtag_scrap('KatyPerry')

# if __name__ == '__main__':

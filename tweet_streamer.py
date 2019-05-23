'''
WARNING: THIS SCRIPT IS DEPRECATED. USE 'FOLLOWER_SCRAPER.PY' INSTEAD
'''

from flask import jsonify
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import credentials 
import numpy as np
import pandas as pd
import json

 # # # # # TWITTER CLIENT # # # # # #
class TwitterClient():
    def __init__(self, twitter_user = None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client



    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self,num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list
                
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


#####TWITTER AUTHENTICATOR ##########
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_KEY, credentials.ACCESS_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        if status == 420:
            #returning False on data method in case rate limit occurs
            return False
        print(status)

 
class TweetAnalyzer():
    '''
    Functionality for analyzing and categorizing content from tweets.
    '''
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])

        return df



class UserAnalyzer():
    '''
    Functionality to analyze user followers
    '''

    def followers_to_data_frame(self, followers):
        df = pd.DataFrame(data=[follower.id for follower in followers], columns=['id'])
        df['name'] = np.array([follower.name for follower in followers])
        df['screen_name'] = np.array([follower.screen_name for follower in followers])
        df['location'] = np.array([follower.location for follower in followers])
        df['followers_count'] = np.array([follower.followers_count for follower in followers])
        df['profile_image_url'] = np.array([follower.profile_image_url for follower in followers])

        return df



if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    # hash_tag_list = ["ramadan"]
    # fetched_tweets_filename = "tweets.txt"

    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    # twitter_client = TwitterClient('SantapanMinda')
    # twitter_client = TwitterClient()

    # print(twitter_client.get_user_timeline_tweets(1))
    # print(twitter_client.get_friend_list(50))
    # print(twitter_client.get_home_timeline_tweets(10))

    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    # tweets = api.user_timeline(screen_name='realDonaldTrump', count=20)
    


    # tweet_df = tweet_analyzer.tweets_to_data_frame(tweets)
    # print(tweet_df.head(5))

    # print(tweets[0].favorite_count)
    # print(dir(tweets[0]))

    user_analyzer = UserAnalyzer()
    f_ids = api.followers_ids(screen_name = 'BarackObama')
    # print(len(f_ids))
    legit_followers = []
    n=1
    for i in range(len(f_ids)-1):
        if i % 5 == 0:
            print(n*'#', end='\r')
            n += 1
        follower = api.get_user(f_ids[i])
        if follower.followers_count > 10000:
            legit_followers.append(follower)

        
    # followers = [api.get_user(follower_id) for follower_id in f_ids[:50]]

    legit_followers_df = user_analyzer.followers_to_data_frame(legit_followers)
    print(legit_followers_df)
    # print(dir(followers[0]))


    # print(followers_df.head(50))
    # d = followers_df.to_dict(orient='records')
    # j = json.dumps(d)

    # print(j[1])

    

    # jsonified = json.dumps(json.loads(followers_df.to_json(orient='index')), indent=2)
    # print(jsonified)




  
    # j = followers_df.to_json(orient='records')
    # jsonified = json.loads(json.dumps(j, indent=1))
    # # print (jsonified[0].name)
    # print(jsonified) 
    
    # print(followers_df.iloc[16])
    # print(dir(followers[0]))
    # print(followers[0])
    # print(followers[0].id)
    # print(followers[0].screen_name)

    # print(df.iloc[4])
    # print(df.head)
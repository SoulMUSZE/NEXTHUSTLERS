from tweepy import API
from tweepy import OAuthHandler

import credentials

import tweepy
import numpy as np
import pandas as pd
import json
import time

from tweetcrawler import db
from tweetcrawler.model import Users



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
    user_analyzer = UserAnalyzer()

    # create API object with authentication
    api = twitter_client.get_twitter_client_api()

    # obtain id's of user's followers. API call will return 5000 ids

    f_ids = api.followers_ids(screen_name='KatyPerry')
    # print(f_ids[:50]) #order of ids returned by API call has minor variations
    # print(len(f_ids)) #5000
    user_count = 0
    legit_followers = []
    n = 1  # counter for simple progress bar
    for i in range(len(f_ids)-1):
        
        # print '#' in progress bar at every 5 iteration
        if i % 5 == 0:
            print(n*'#', end='\r')
            n += 1

        try:
            # obtain follower object from API
            follower = api.get_user(f_ids[i])
            
            
            # check if follower has minimum followers count
            if follower.followers_count > 10:
                legit_followers.append(follower)

                      
                ### SAVE TO DATABASE ###

                # check if the record exists in db
                if bool(Users.query.filter_by(id=follower.id).first()):
                    print(f'User {follower.name} is already in the database')
                    pass
                else:
                    user_count += 1
                    save = Users(id=follower.id ,screen_name=follower.screen_name ,
                                full_name=follower.name, location=follower.location,
                                followers_count=follower.followers_count,
                                friends_count=follower.friends_count,
                                profile_created_at = follower.created_at,
                                protected=follower.protected)
                    db.session.add(save)
                    db.session.commit()
                    
                    print(f'{follower.name} added to database.')
                    print(f'{user_count} users matching the filters saved into database')
                

        #do nothing/move on to next iteration if API call returns an exception/error
        except tweepy.TweepError:
            pass

        # pause the script for 1s to avoid rate limit exceeded (900 API calls/15 mins)
        time.sleep(1)

    # convert array of legit followers to pandas DataFrame for better visualization (unnecessary if followers are stored into database inside the loop)
    legit_followers_df = user_analyzer.followers_to_data_frame(legit_followers)
    print('\n')
    print(legit_followers_df)

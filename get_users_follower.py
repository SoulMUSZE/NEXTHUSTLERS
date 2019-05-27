

import time
import tweepy
import csv
from credentials import *
from tweetcrawler.model import Users
from tweepy import API
from tweepy import OAuthHandler
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# # # # TWITTER AUTHENTICATOR # # # #


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.consumer_key,
                            credentials.consumer_secret)
        auth.set_access_token(credentials.access_token,
                              credentials.access_token_secret)
        return auth


# # # # # TWITTER CLIENT # # # # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(
            self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    users = tweepy.Cursor(
        api.followers, screen_name="terminator").items()


api = tweepy.API(auth)

HEADER = ['Screenname']

result = Users.query
users = result(Users.followers_count and Users.location)


def processing_loop(csvfile):
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(HEADER)

    while True:
        try:
            user = next(users)
        except tweepy.TweepError:
            time.sleep(60*20)
            user = next(users)
        except StopIteration:
            break
        csv_writer.writerow([user.followers_count])
        csvfile.flush()
        time.sleep(5)


with open('results.csv', 'w') as csvfile:
    processing_loop(csvfile)

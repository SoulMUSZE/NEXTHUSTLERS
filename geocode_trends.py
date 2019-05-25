import googlemaps
import sys
import tweepy
import json
from credentials import *

# Google Maps API
gmaps = googlemaps.Client(key=google_api)
geocode_result = gmaps.geocode('Kuala Lumpur')


latitude = (geocode_result[0]['geometry']['location']['lat'])
longitude = (geocode_result[0]['geometry']['location']['lng'])


# TWITTER API

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


closest_result = api.trends_closest(latitude, longitude)
woeid = (closest_result[0]['woeid'])

trends_result = api.trends_place(woeid)
trends = (trends_result[0]['trends'])

# ARRAY TO STORE THE TRENDS NAMES
trends_names = []

for x in trends:
    trends_names.append(x['name'])

print(trends_names)

# from models import TargetUser, Follower
from flask import Flask, render_template, request, redirect, url_for, flash
from tweetcrawler import app
import googlemaps
import sys
import tweepy
import json
from credentials import *


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/maps", methods=['GET', 'POST'])
def trends():

    # Google Maps API
    # if request.method == "POST":
    #     search = request.form["place-name"]
    #     return search
    # search = request.get["place-name"]

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

    return render_template('maps.html', hashtags=trends_names[:10], API_KEY=google_api)

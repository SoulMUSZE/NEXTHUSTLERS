# from models import TargetUser, Follower

from flask import Flask, render_template, request, redirect, url_for, flash
from tweetcrawler import app
import googlemaps
import sys
import tweepy
import json
from credentials import *


from tweetcrawler.model import Users
from flask_wtf import FlaskForm


# def autocomplete():
#     data = Locations.query.filter(Locations.name.ilike(request.form.get('keyword')))
#     return jsonify({data: data})


@app.route("/", methods=['GET'])
def index():

    followersDict = {
        '1': 50,
        '2': (50, 80),
        '3': (81, 100),
        '4': 101
    }

    city = request.args.get('city')
    followers = request.args.get('followers')
    result = Users.query

    if city:
        result = result.filter(Users.location.ilike(f"%{city}%"))

    if followers:
        if followers == '1':
            result = result.filter(Users.followers_count <= followersDict.get(followers))
        elif followers == '4':
            result = result.\
                    filter(Users.followers_count >= followersDict.get(followers))
        elif followers == '2' or followers == '3':
            result = result.\
                    filter(Users.followers_count.between(followersDict.get(followers)[0], followersDict.get(followers)[1]))
    

    page = request.args.get('page', 1, type=int)
    users = result.order_by(Users.followers_count.desc()).paginate(page=page, per_page=5)


    return render_template('home.html', users=users)
  

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

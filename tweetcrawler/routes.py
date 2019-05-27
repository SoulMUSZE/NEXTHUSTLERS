# from models import TargetUser, Follower

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
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

    if request.method == 'POST':        
    
        
        place_name = request.data.decode('utf-8').split("=")[-1]
    
        # breakpoint()
        # call twitter geocode API 
        gmaps = googlemaps.Client(key=google_api)

        geocode_result = gmaps.geocode(place_name)

        latitude = (geocode_result[0]['geometry']['location']['lat'])
        longitude = (geocode_result[0]['geometry']['location']['lng'])

        # TWITTER API

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        closest_result = api.trends_closest(latitude, longitude)
        woeid = (closest_result[0]['woeid'])

        trends_result = api.trends_place(woeid)
        trends = (trends_result[0]['trends'])

        # ARRAY TO STORE THE TRENDS NAMES
        trends_names = []

        for x in trends:
            trends_names.append(x['name'])

        # breakpoint()    
        # # return 'OK', 200
        return jsonify(trends_names), 200

    # GET request
    return render_template('maps.html', API_KEY = google_api)
        


   


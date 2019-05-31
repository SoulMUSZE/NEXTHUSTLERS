# from models import TargetUser, Follower

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from app import app
import googlemaps
import sys
import tweepy
import json
import random

from credentials import *

from model import User, Tweet
from flask_wtf import FlaskForm

from keyword_api_client import RestClient

# import io
# import csv
# from flask import Response

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
    verified = request.args.get('verified')
    result = User.query
    tweets = Tweet.query

    # Filter / Verified Accounts
    if verified:
        result = result.filter (User.verified)

    # Filter / City
    if city:
        result = result.filter(User.location.ilike(f"%{city}%"))

    # Filter / Follower count
    if followers:
        if followers == '1':
            result = result.filter(
                User.followers_count <= followersDict.get(followers))
        elif followers == '4':
            result = result.\
                filter(User.followers_count >= followersDict.get(followers))
        elif followers == '2' or followers == '3':
            result = result.\
                filter(User.followers_count.between(followersDict.get(
                    followers)[0], followersDict.get(followers)[1]))

    page = request.args.get('page', 1, type=int)
    users = result.order_by(User.followers_count.desc()
                            ).paginate(page=page, per_page=5)

    # breakpoint()
    # for user in result:
    #     for tweet in user.tweets:
    #         for hashtag in tweet.hashtags:
    #             print(hashtag)

    return render_template('home.html', users=users, tweets=tweets)


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

        # ARRAY TO STORE THE TWEET VOLUME
        tweets_volumes = []

        # ARRAY TO STORE THE HASHTAGS AND TWEET VOLUME
        name_volume = []

        for x in trends:
            trends_names.append(x['name'])

        for y in trends:
            tweets_volumes.append(y['tweet_volume'])

        for a, b in zip(trends_names, tweets_volumes):
            # name_volume.append(a)
            # name_volume.append(b)
            name_volume.append({
                'tag': a,
                'volume': b
            })

        # # return 'OK', 200
        return jsonify(name_volume[:10]), 200

    # GET request
    return render_template('maps.html', API_KEY=google_api)


@app.route("/keywords", methods=['GET', 'POST'])
def keywords():

    if request.method == 'POST':

        seedWord = request.form.get("seedWord")

        client = RestClient(SEO_LOGIN, SEO_PASSWORD)

        # you can set as "index of post_data" your ID, string, etc. we will return it with all results.
        # rnd = Random()

        post_data = dict()
        # post_data[random.randint(1, 30000000)] = dict(
        post_data['NEXTHUSTLERS'] = dict(
            keyword=seedWord,
            country_code="US",
            language="en",
            depth=2,
            limit=15,
            offset=0,
            orderby="search_volume,desc",
            filters=[
                ["cpc", ">", 0],
                "or",
                [
                    ["search_volume", ">", 0],
                    "and",
                    ["search_volume", "<=", 10000]
                ]
            ]
        )

        response = client.post(
            "/v2/kwrd_finder_related_keywords_get", dict(data=post_data))

        if response["status"] == "error":
            print("error. Code: %d Message: %s" %
                  (response["error"]["code"], response["error"]["message"]))

            return render_template('keywords.html', keywords="API Error")
        else:
            keywords = response['results']['NEXTHUSTLERS']['related']

            if keywords == "No data":
                # return render_template('keywords.html', keywords = keywords)
                return render_template('keywords.html', keywords=response['results'])
            # print(response["results"])
            else:
                key_list = []
                # breakpoint()
                # for keyword in keywords:
                #     key_list.append(keyword["key"])

                for keyword in keywords:
                    key_list.append({k: keyword[k]
                                     for k in ('key', 'search_volume')})

                key_list = [
                    pair for pair in key_list if pair['key'] != seedWord]

                # sorted_key_list = sorted(key_list, key=lambda pair: pair['search_volume'], reverse=True)
                max_volume = key_list[0]['search_volume']

                # breakpoint()
                # # split strings in key_list by whitespace
                # split_key_list = [key.split() for key in key_list]
                # #flatten list
                # flattened_key_list = [item for sublist in split_key_list for item in sublist]
                # # keep only unique keywords
                # related_keywords = list(set(flattened_key_list))

                # return render_template('keywords.html', keywords = related_keywords)
                return render_template('keywords.html', keywords=key_list, max=max_volume)

    # handle GET request
    return render_template('keywords.html')


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html')

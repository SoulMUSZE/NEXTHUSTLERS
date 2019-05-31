# from models import TargetUser, Follower

from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify
from app import app

import googlemaps
import sys
import tweepy
import json
import random
import paralleldots

from credentials import *

from model import User, Tweet
from flask_wtf import FlaskForm
from app import db

from keyword_api_client import RestClient, get_related_keywords

paralleldots.set_api_key(PARALLELDOTS_API_KEY)
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

    # handle hashtags
    seedWord = request.args.get("seedWord")

    city = request.args.get('city')
    followers = request.args.get('followers')
    verified = request.args.get('verified')
    result = User.query
    tweets = Tweet.query

    usernameExist = request.args.get('selectedUsers')
    if usernameExist:
        selected_usernames = json.loads(usernameExist)
    
    # breakpoint()

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

    '''
    HANDLE HASHTAGS
    '''
    
    if seedWord:

        # get related keywords from SEO API
        key_list = get_related_keywords(seedWord)

        if key_list:
            # split strings in key_list by whitespace
            split_key_list = [pair['key'].split() for pair in key_list]
            # flatten list
            flattened_key_list = [
                item for sublist in split_key_list for item in sublist]
            # keep only unique keywords
            related_keywords = list(set(flattened_key_list))

        else:
            related_keywords = [seedWord]
        
        

        # for user in result.all():
        selected_users = []
        for username in selected_usernames:

            user = User.query.filter_by(screen_name = username).first()
            selected_users.append(user)
            # get user hashtags
            user_hashtags = []
            for tweet in user.tweets:
                for hashtag in tweet.hashtags:
                    user_hashtags.append(hashtag.hashtag)

            # similarity API only works if text has at least 2 arguments
            if len(user_hashtags) > 1:
                
                # compare user_hashtags with related_keywords
                text1 = ' '.join(related_keywords)
                text2 = ' '.join(user_hashtags)
                response = paralleldots.similarity(text1, text2)
           
                # save similarity score to DB
                user.similarity = response["similarity_score"]
                db.session.commit()

        users = result.filter(selected_users).order_by(User.similarity.desc()).paginate(page=page, per_page=5)

        return render_template('home.html', users=users, tweets=tweets)


    return render_template('home.html', users=users, tweets=tweets)


# #grab user hashtags
# users_with_hashtags = []
# for user in result.all():
#     current_user = {
#         "name": user.screen_name,
#         "hashtags": []
#     }
#     # print(f"-- User: {user.screen_name}")
#     for tweet in user.tweets:
#         # print(f"- Tweet: {tweet.tweet_text}")
#         for hashtag in tweet.hashtags:
#             current_user["hashtags"].append(hashtag)
#             # print(f"Hashtag: {hashtag.hashtag}")

#     users_with_hashtags.append(current_user)

# print(len(users_with_hashtags))

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

        key_list = get_related_keywords(seedWord)

        if key_list:
            # sorted_key_list = sorted(key_list, key=lambda pair: pair['search_volume'], reverse=True)
            max_volume = key_list[0]['search_volume']
            return render_template('keywords.html', keywords=key_list, max=max_volume)

        else:
            return render_template('keywords.html', keywords=key_list)

    # handle GET request
    return render_template('keywords.html')


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html')

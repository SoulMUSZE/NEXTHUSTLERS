# from models import TargetUser, Follower
from flask import Flask, render_template, request, url_for, flash, redirect
from tweetcrawler import app
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





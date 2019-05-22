# from models import TargetUser, Follower
from flask import Flask, render_template
from tweetcrawler import app


@app.route("/")
def index():
    return render_template('home.html')
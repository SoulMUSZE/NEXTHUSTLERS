from flask import Flask
import os
import config
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from tweetcrawler import routes

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

# from tweetcrawler.model import User, TargetUser, Follower

# class model here
# class TargetUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     screen_name = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False) ## technically we don't need email?, we don't use this model for login
#     tweet_count = db.Column(db.Integer, nullable=False) 
#     follower_count = db.Column(db.Integer, nullable=False)
#     friend_count = db.Column(db.Integer, nullable=False)
#     followers = db.relationship('Follower', backref='idol', lazy=True)  


# db.create_all()

csrf = CSRFProtect(app)



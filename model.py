from datetime import datetime
from app import db
from flask_sqlalchemy import SQLAlchemy
from tweetcrawler.models.basemodel import BaseModel
import datetime


# class User(BaseModel):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     screen_name = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     profile_image_url = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)

    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}', '{self.profile_image_url}')"

# source account used for getting users list 
# class TargetUser(BaseModel):
#     __tablename__ = 'target_user'
#     id = db.Column(db.Integer, primary_key=True)
#     screen_name = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False) ## technically we don't need email?, we don't use this model for login
#     tweet_count = db.Column(db.Integer, nullable=False) 
#     follower_count = db.Column(db.Integer, nullable=False)
#     friend_count = db.Column(db.Integer, nullable=False)
#     followers = db.relationship('Users', backref='idol', lazy=True)  


# source of data for the actual database
# hashtag_usage = db.Table('hashtag_usage',
#     db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id'))
#     )


class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(), nullable=True)
    followers_count = db.Column(db.Integer(), nullable=False)
    friends_count = db.Column(db.Integer(), nullable=False)
    profile_created_at = db.Column(db.DateTime, index=True)
    protected = db.Column(db.Boolean, default=False) 
    profile_image_url = db.Column(db.String(20), nullable=True, default="")
    tweets = db.relationship('Tweet', backref='user', lazy='dynamic')
    # hashtag_used = db.relationship('Hashtag', secondary=hashtag_usage, backref=db.backref('hashtag_users', lazy='dynamic'))
   

class Tweet(BaseModel):
    __tablename__ = 'tweet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tweet_id = db.Column(db.Integer(), nullable=False)
    tweet_text = db.Column(db.String(140))
    hashtags = db.relationship('HashtagUsage', backref='tweet')

# middle table for Tweet / Hashtag
class HashtagUsage(BaseModel):
    __tablename__ = 'hashtag_usage'
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=False)
    hashtag = db.Column(db.String(30), nullable=False)
    # hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtag.id'), nullable=False)
   


# class Hashtag(BaseModel):
#     __tablename__ = 'hashtag'
#     __table_args__ = {'extend_existing': True} 
#     id = db.Column(db.Integer, primary_key=True)
#     hashtag_name = db.Column(db.String(30))
#     count = db.Column(db.Integer)

    # def __repr__(self):
    #     return f"User('{self.screen_name}','{self.full_name}' '{self.profile_image_url}')"
    


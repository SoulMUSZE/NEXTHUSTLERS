from datetime import datetime
from tweetcrawler import db
from flask_sqlalchemy import SQLAlchemy
from tweetcrawler.models.basemodel import BaseModel



class User(BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_image_url = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}', '{self.profile_image_url}')"


class TargetUser(BaseModel):
    __tablename__ = 'target_user'
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) ## technically we don't need email?, we don't use this model for login
    tweet_count = db.Column(db.Integer, nullable=False) 
    follower_count = db.Column(db.Integer, nullable=False)
    friend_count = db.Column(db.Integer, nullable=False)
    followers = db.relationship('Followers', backref='idol', lazy=True)  


class Followers(BaseModel):
    __tablename__ = 'followers'
    id = db.Column(db.Integer, primary_key=True)
    idol_id = db.Column(db.Integer, db.ForeignKey('target_user.id'), nullable=False)
    screen_name = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    profile_image_url = db.Column(db.String(20), nullable=False, default='default.jpg')
    


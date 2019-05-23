import os
from flask_sqlalchemy import SQLAlchemy
import datetime
from tweetcrawler import db

# from database import db ???

class BaseModel(db.Model):
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now() )


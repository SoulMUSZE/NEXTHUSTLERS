import os
from flask_sqlalchemy import SQLAlchemy
import datetime
from tweetcrawler import db

# from database import db ???

class BaseModel(db.Model):
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now() )

#     def save(self, *args, **kwargs):
#         self.errors = []
#         self.validate()

        # if len(self.errors) == 0;
        #     self.updated_at = datetime.datetime.now()
        #     return super(BaseModel, self).save(@args, **kwargs)

        # else:
        #     return 0

    # def validate(self):
    #     print(
    #         f"Warning validation method not implemented for {str(type(self))}"
    #     )
    #     return True

    # class Meta:
    #     database = database # still missing imported/defined
    #     # legacy_table_names = False  <<??? what is this?
# DB Migration commands ##
from flask import Flask
from app import app, db
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand



migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



# class Users():
#     __tablename__ = 'users'
#     __table_args__ = {'extend_existing': True}
#     profile_image_url = db.Column(db.String(120))


if __name__ == '__main__':
    manager.run()



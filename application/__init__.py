import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_navigation import Navigation
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "traffic.db"
UPLOAD_FOLDER = './uploads'
CLIP_FOLDER = './clips'
RECORDS_FOLDER = "./records"
SECRET_KEY = "The World is not Enough"


def create_database(app):
    if path.exists('application/' + DB_NAME):
        with app.app_context():
            print("droped database")
            db.drop_all()

    if not path.exists('application/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("created database")


def create_folders():
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    if not os.path.exists(CLIP_FOLDER):
        os.mkdir(CLIP_FOLDER)
    if not os.path.exists(RECORDS_FOLDER):
        os.mkdir(RECORDS_FOLDER)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['CLIP_FOLDER'] = UPLOAD_FOLDER
    app.config['RECORDS_FOLDER'] = UPLOAD_FOLDER

    # db codes
    db.init_app(app)

    from .models import User
    create_database(app)

    # register login models and intialize Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # folder codes
    create_folders()

    # register views
    from .view import view
    from .auth import auth

    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # register menu items
    nav = Navigation(app)
    nav.Bar('top', [
        nav.Item('Home', 'view.home', html_attrs={'icon': 'home', 'id': 'no'})
    ])

    return app

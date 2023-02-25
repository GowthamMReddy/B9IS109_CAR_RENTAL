from flask import Flask

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='This is my application'

    return app


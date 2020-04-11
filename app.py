import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from resources.item import Item, ItemList
from security import authenticate, identity

from resources.user import UserRegister
from resources.store import Store, StoreList

# creating an application
app = Flask(__name__)

# configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'przemek'

# Resource management
api = Api(app)

jwt = JWT(app, authenticate, identity)  # Pass authentication and identity function

# this resource is available only for get methods
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/student/Rolf
api.add_resource(UserRegister, '/register')  # http://127.0.0.1:5000/register
api.add_resource(Store, '/store/<string:name>')  # http://127.0.0.1:5000/student/Rolf
api.add_resource(StoreList, '/stores')  # http://127.0.0.1:5000/register

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000)

import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.item import Item, ItemList

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.store import Store, StoreList

from blacklist import BLACKLIST

# creating an application
app = Flask(__name__)

# configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'przemek'

@app.before_first_request
def create_tables():
    db.create_all()




# Resource management
api = Api(app)
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin':True},
    return {'is_admin':False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'description':'The token has expired',
                    'error':'token_expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'description':'Signature verification failed',
                    'error':'invalid_token'}), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({'description':'Unauthorized token',
                    'error':'unauthorized'}), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({'description':'Need refreshed token',
                    'error':'need_refresh_token'}), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({'description':'Revoked Token',
                    'error':'revoked_token'}), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST



# this resource is available only for get methods
api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/student/Rolf
api.add_resource(UserRegister, '/register')  # http://127.0.0.1:5000/register
api.add_resource(Store, '/store/<string:name>')  # http://127.0.0.1:5000/student/Rolf
api.add_resource(StoreList, '/stores')  # http://127.0.0.1:5000/stores
api.add_resource(User, '/user/<int:user_id>')  # http://127.0.0.1:5000/user/<int:user_id>
api.add_resource(UserLogin, '/login')  # http://127.0.0.1:5000/login
api.add_resource(TokenRefresh, '/refresh')  # http://127.0.0.1:5000/refresh
api.add_resource(UserLogout, '/logout')  # http://127.0.0.1:5000/logout

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000)

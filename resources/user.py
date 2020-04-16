from flask_restful import Resource, reqparse

from models.usermodel import UserModel

from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt)

from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help='This field cannot be left blank')
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help='This field cannot be left blank')


class UserRegister(Resource):
    @staticmethod
    def post():
        data = _user_parser.parse_args()

        # select_query = "SELECT username FROM users"
        if UserModel.find_by_username(data['username']):
            return {"message": "user already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User was created"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User Not found'}, 404
        else:
            return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':'User Not found'}, 404
        else:
            user.delete_from_db()
            return {'message':'User deleted'}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from _user_parser
        data = _user_parser.parse_args()
        # Find User in DB
        user = UserModel.find_by_username(data['username'])

        # Check pwd
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id , fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                "access_token": access_token,
                'refresh_token': refresh_token
            }

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']   # JTI is "JWT ID", a unique identifier for a JWT

        BLACKLIST.add(jti)
        return {'message':'Successfully logged out'}



class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()

        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token':new_token}, 200





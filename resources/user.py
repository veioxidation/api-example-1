import sqlite3
from flask_restful import Resource, reqparse

from models.usermodel import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        # select_query = "SELECT username FROM users"
        if UserModel.find_by_username(data['username']):
            return {"message":"user already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message":"User was created"} , 201

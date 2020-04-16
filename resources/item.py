from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required

from models.itemmodel import ItemModel

app = Flask(__name__)
app.secret_key = 'przemek'


# # Resource management
# api = Api(app)
# jwt = JWT(app, authenticate, identity)  # Pass authentication and identity function


# this resource is available only for get methods
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every Item needs a Store ID')

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "Item not found"}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name):
        if ItemModel.find_by_name(name):
            return {'message': f"an item with name {name} already exist"}, 400

        # parsing arguments
        data = cls.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'Error while parsing via server'}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # delete_query = "DELETE FROM items WHERE name=?"
        # cursor.execute(delete_query, (name,))
        # connection.commit()
        # connection.close()

        # JWT extension
        claims = get_jwt_claims()
        if not claims[0]['is_admin']:
            return {'message': 'This user is not an admin'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': f'Item {name} deleted'}

    @staticmethod
    def put(name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            # when exists, replace
            # new_item.update()
            item.price = data['price']
        else:
            # when doesn't exist, create a new one
            # new_item.insert()
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @staticmethod
    @jwt_optional
    def get():
        # return {"items": [item.json() for item in ItemModel.find_all()]}

        # additional jwt optional
        user_id = get_jwt_identity()
        items = list(map(lambda x: x.json(), ItemModel.query.all()))

        if user_id:
            # if user is logged in, return items
            return {"items": items}, 200
        else:
            # else,
            return {'items': [item['name'] for item in items],
                    'message': 'More data available when you log in'}, 200

from flask_restful import Resource
from models.storemodel import StoreModel


class Store(Resource):

    def get(self, name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": 'Store not found'}

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"A store with name {name} already exist"}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Error while parsing via server'}, 500

        return store.json(), 201


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': f'Item {name} deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

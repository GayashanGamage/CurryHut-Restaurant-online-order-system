from pymongo import MongoClient
from . import model
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi.encoders import jsonable_encoder

class DataBase:

    load_dotenv()

    # initialize the database
    def __init__(self):
        self.client = MongoClient(os.getenv("mongodb"))
        self.db = self.client['curryhut']
        self.user = self.db['test']
        self.delivery = self.db['Delivery']
        self.shop = self.db['Shop']
        
    def insert_delivery_place(self, details : model.Delivery):
        store_data = self.delivery.insert_one(details.dict())
        if store_data.acknowledged:
            return True
        else:
            return False
        
    def get_delivery_place(self):
        data = list(self.delivery.find({}))
        if len(data) > 0:
            delivery_data = [
                model.get_delivery(id = str(delivery['_id']), place = delivery['place'], status = delivery['status'], cost = delivery['cost']).dict() for delivery in data
            ]
            return delivery_data
        else:
            return data

    def update_delivery_details(self, details : model.delivery_update):
        store_data = self.delivery.update_one({"_id" : details.id}, {"$set" : details.dict(exclude={"id"})})
        if store_data.modified_count == 1:
            return True
        else:
            return False

    def update_delivery_status(self, details : model.delivery_status):
        store_data = self.delivery.update_one({"_id" : details.id}, {"$set" : details.dict(exclude={"id"})})
        if store_data.modified_count == 1:
            return True
        else:
            return False

    def delete_delivery(self, id):
        store_data = self.delivery.delete_one({"_id" : ObjectId(id)})
        if store_data.deleted_count == 1:
            return True
        else:
            return False


    def get_shop_details(self, id):
        data = self.shop.find_one({'_id' : ObjectId(id)})
        return data


def get_database():
    return DataBase()

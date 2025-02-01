from pymongo import MongoClient
from . import model
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from random import randint

class DataBase:

    load_dotenv()

    # initialize the database
    def __init__(self):
        self.client = MongoClient(os.getenv("mongodb"))
        self.db = self.client['curryhut']
        self.user = self.db['User']
        self.delivery = self.db['Delivery']
        self.shop = self.db['Shop']
        self.category = self.db['Category']
        self.food = self.db['Food']
        
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


    def get_categories_customer(self):
        data = list(self.category.find({'deletable' : True}, {"aded_date" : 0, "last_modify_date" : 0, "item_count" : 0}))
        if len(data) > 0:
            categories = [
                model.get_categories_customer(id = str(category['_id']), name = category['name'], deletable = category['deletable']).dict() for category in data
            ]
            return jsonable_encoder(categories)
        else:
            return data 
        
    def get_foods(self):
        data = list(self.food.find({}))
        if len(data) > 0:
            serialized = [
                model.get_foods(
                    id = str(food['_id']),
                    name = food['name'],
                    category_id = str(food['category_id']),
                    description = food['description'],
                    price = [
                        model.get_price(
                            price = price['price'],
                            name = price['name'],
                            portion = price['portion']
                        ).dict() for price in food['price']
                    ]
                ).dict() for food in data
            ]
            return {'availability' : True, 'data' : jsonable_encoder(serialized)}
        else:
            return {'availability' : False, 'data' : []}


    def check_dubplicate_categories(self, categoryName):
        # perpose : find dublicated category names
        # result : True - duplicate, False - not duplicate
        duplicateCategory = list(self.category.find({'name' : categoryName.lower()}, {'_id' : 0, 'aded_date' : 0, 'last_modify_date' : 0, 'item_count' : 0}))
        if len(duplicateCategory) > 0:
            return True
        else: 
            return False

    def insert_category(self, categoryData):
        # perpose : insert new category in to the database
        # result : True - success, False - failed
        store_data = self.category.insert_one(categoryData.dict())
        if store_data.acknowledged:
            return True
        else:
            return False
        
    def update_category(self, id, newName):
        # perpose : get category by id
        # result : false : category is not available, true : category updated successfully
        data = self.category.find_one_and_update({'_id' : ObjectId(id)}, { '$set' : {'name' : newName}} )
        if data == None:
            return False
        else:
            return True

    def delete_category(self, id):
        # perspose : delete category by id
        # result : true : seccussfull, false : unsuccessfull
        data = self.category.delete_one({'_id' : ObjectId(id)})
        if data.deleted_count == 1:
            return True
        else:
            return False

    def get_categories(self):
        # perpose : get all categories
        # result : false : empty list || all categories list
        data = list(self.category.find({}))
        if len(data) > 0:
            categories = [
                model.Category(
                    id = str(category['_id']),
                    name = category['name'],
                    aded_date = category['aded_date'],
                    last_modify_date = category['last_modify_date'],
                    item_count = category['item_count'],
                    deletable = category['deletable']
                ).dict() for category in data
            ]
            return jsonable_encoder(categories)
        else:
            return False
        
    def check_dubplicate_food(self, foodName):
        print('try to excute this')
        # perpose : check duplicate food item
        # result : true : duplicate, false : not duplicate
        data = list(self.food.find({'name' : foodName.lower()}, {'_id' : 0, 'category_id' : 0, 'description' : 0, 'price' : 0, 'added_data' : 0, 'modified_data' : 0}))
        if len(data) >= 1:
            return True
        else:
            return False
        
    def insert_food(self, foodData):
        # perpose : insert food item
        # result : true : success, false : failed
        data = self.food.insert_one(foodData.dict())
        if data.acknowledged:
            return True
        else:
            return False
        
    def get_food(self):
        # perpose : get all food items
        # result : false : empty list || all food items
        data = list(self.food.find({}))
        if len(data) >= 1:
            foods = [
                model.getFood(
                    id  = str(food['_id']),
                    category_id = str(food['category_id']),
                    name = food['name'],
                    description= food['description'],
                    added_data = food['added_data'],
                    modified_data = food['modified_data'],
                    price = [
                        model.FoodDataPrice(
                            name = price['name'],
                            price = price['price'],
                            portion = price['portion']
                        ) for price in food['price']
                    ]                   
                ).dict() for food in data
            ]
            return jsonable_encoder(foods)
        else:
            return False

    def edit_food(self, foodData):
        # perpose : update food items
        # result : true : successfull || false : failed
        data = self.food.update_one({"_id" : foodData.id}, {"$set" : foodData.dict(exclude={"id"})})
        if data.acknowledged:
            return True
        else:
            return False

    def remove_food(self, foodId):
        # perpose : delete food item
        # result : true : successfull || false : failed
        data = self.food.delete_one({"_id" : ObjectId(foodId)})
        if data.deleted_count == 1:
            return True
        else:
            return False
        
        
    def check_duplicate_admin_user(self, user):
        # perpose : check duplicate admin user
        # result : true : duplicate, false : not duplicate
        data = self.user.find_one({'email' : user.email, 'role' : user.role})
        if data == None:
            return False
        else:
            return True

    def insert_admin_user(self, user):
        # perpose : create new admin user
        # result : true : successfull, false : failed
        data = self.user.insert_one(user.dict())
        if data.acknowledged:
            return True
        else:
            return False
        
    def update_secreate_code(self, email):
        # perpose : update secreate code
        # result : status.True : successfull, status.False : failed
        secreate_code = randint(1000, 9999)
        code = self.user.update_one({'email' : email}, {'$set' : {'secreate_code' : secreate_code, 'send_time' : datetime.now(), 'password_change' : True}})
        if code.modified_count == 1:
            return {'status' : True, 'code' : secreate_code}
        else:
            return {'status' : False}

    def get_credencials(self, usercredencial):
        # perpose : get user credencials
        # result : false : user not found || found : data
        data = self.user.find_one({'email' : usercredencial.email, 'role'  : usercredencial.role})
        if data != None:
            return data
        else:
            return False
        
    def check_secreate_code(self, code):
        # perpose : check secreate code
        # result : true : match email and secreate code, false : email or secreate code not matched
        data = self.user.find_one({'email' : code.email})
        if(data['password_change'] == True and data['secreate_code'] == code.code):
            self.user.update_one({'email' : code.email}, {'$set' : {'secreate_code' : None, 'send_time' : None}})
            return True
        else:
            return False
        
    def check_password_change(self, password):
        # perpose : check whether request password change or not
        # result : true : password change requested, false : not requested
        data = self.user.find_one({'email' : password.email})
        if data['password_change'] == True:
            return True
        else:
            return False

    def change_password(self, email, encoded_password):
        data = self.user.update_one({'email' : email}, {'$set' : {'password' : encoded_password, 'password_change' : False}})
        if data.modified_count == 1:
            return True
        else:
            return False

def get_database():
    return DataBase()


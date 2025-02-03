from pymongo import MongoClient
from . import model
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from random import randint
from fastapi.responses import JSONResponse


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

    def insert_delivery_place(self, details):
        # perpose : insert delivery place
        # result : true : successfull, false : failed
        store_data = self.delivery.insert_one(details.dict())
        if store_data.acknowledged:
            return True
        else:
            return False

    def single_delivery_place(self, id):
        # perpose : get single delivery place
        # result : false : not available || data : available
        data = self.delivery.find_one({'_id': ObjectId(id)})
        if data != None:
            return data
        else:
            return False

    def check_delivery_duplicate(self, place):
        # perpose : check duplicate delivery place
        # result : true : duplicate, false : not duplicate
        data = list(self.delivery.find({'place': place.lower()}))
        if len(data) >= 1:
            return {'status': True, 'data': data}
        else:
            return {'status': False}

    def get_delivery_place(self):
        data = list(self.delivery.find({}))
        if len(data) > 0:
            delivery_data = [
                model.get_delivery(id=str(delivery['_id']), place=delivery['place'], status=delivery['status'], cost=delivery['cost']).dict() for delivery in data
            ]
            return delivery_data
        else:
            return data

    def update_delivery_details(self, details: model.delivery_update):
        store_data = self.delivery.update_one(
            {"_id": details.id}, {"$set": details.dict(exclude={"id"})})
        if store_data.modified_count == 1:
            return True
        else:
            return False

    def update_delivery_status(self, details: model.delivery_status):
        store_data = self.delivery.update_one(
            {"_id": details.id}, {"$set": details.dict(exclude={"id"})})
        if store_data.modified_count == 1:
            return True
        else:
            return False

    def delete_delivery(self, id):
        store_data = self.delivery.delete_one({"_id": ObjectId(id)})
        if store_data.deleted_count == 1:
            return True
        else:
            return False

    def get_shop_details(self, id):
        data = self.shop.find_one({'_id': ObjectId(id)})
        return data

    def get_categories_customer(self):
        data = list(self.category.find({'deletable': True}, {
                    "aded_date": 0, "last_modify_date": 0, "item_count": 0}))
        if len(data) > 0:
            categories = [
                model.get_categories_customer(id=str(category['_id']), name=category['name'], deletable=category['deletable']).dict() for category in data
            ]
            return jsonable_encoder(categories)
        else:
            return data

    def get_foods(self):
        data = list(self.food.find({}))
        if len(data) > 0:
            serialized = [
                model.get_foods(
                    id=str(food['_id']),
                    name=food['name'],
                    category_id=str(food['category_id']),
                    description=food['description'],
                    price=[
                        model.get_price(
                            price=price['price'],
                            name=price['name'],
                            portion=price['portion']
                        ).dict() for price in food['price']
                    ]
                ).dict() for food in data
            ]
            return {'availability': True, 'data': jsonable_encoder(serialized)}
        else:
            return {'availability': False, 'data': []}

    def check_deletable_category(self, id):
        # perpose : chack category is deletable or not
        # result : true : deletable, false : not deletable
        data = self.category.find_one({'_id': ObjectId(id)})
        if data['deletable'] == True:
            return True
        else:
            return False

    def check_dubplicate_categories(self, categoryName):
        # perpose : find dublicated category names
        # result : duplicateCategory - duplicated , False - not duplicate
        duplicateCategory = list(self.category.find({'name': categoryName.lower()}, {
                                 '_id': 1, 'aded_date': 0, 'last_modify_date': 0, 'item_count': 0}))
        if len(duplicateCategory) >= 1:
            return {'status': True, 'data': duplicateCategory}
        else:
            return {'status': False}

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
        data = self.category.find_one_and_update(
            {'_id': ObjectId(id)}, {'$set': {'name': newName}})
        if data == None:
            return False
        else:
            return True

    def delete_category(self, id):
        # perspose : delete category by id
        # result : true : seccussfull, false : unsuccessfull

        # check category is deletable or not
        category = self.category.find_one({'_id': ObjectId(id)})
        if category != None:
            if category['deletable'] == False:
                return {'status': False, 'code': 401}
            else:
                data = self.category.delete_one({'_id': ObjectId(id)})
                if data.deleted_count == 1:
                    return {'status': True, 'code': 200}
                else:
                    return {'status': False, 'code': 500}
        else:
            return {'status': False, 'code': 404}

    def get_categories(self):
        # perpose : get all categories
        # result : false : empty list || all categories list
        data = list(self.category.find({}))
        if len(data) > 0:
            categories = [
                model.Category(
                    id=str(category['_id']),
                    name=category['name'],
                    aded_date=category['aded_date'],
                    last_modify_date=category['last_modify_date'],
                    item_count=category['item_count'],
                    deletable=category['deletable']
                ).dict() for category in data
            ]
            return jsonable_encoder(categories)
        else:
            return False

    def check_category_id(self, categoryId):
        # perpose : check category id is available or not
        # result : true : available, false : not available
        data = self.category.find_one({'_id': ObjectId(categoryId)})
        if data != None:
            return True
        else:
            return False

    def update_food_list(self, target, replace):
        # perpose : update multiple foods
        # result : true : successfull, false : failed
        data = self.food.update_many({'category_id': ObjectId(target)}, {
                                     '$set': {'category_id': ObjectId(replace)}})
        if data.modified_count >= 1:
            return True
        else:
            return False

    def check_dubplicate_food(self, foodName):
        # perpose : check duplicate food item
        # result : true : duplicate, false : not duplicate
        data = list(self.food.find({'name': foodName.lower()}, {
                    '_id': 0, 'category_id': 0, 'description': 0, 'price': 0, 'added_data': 0, 'modified_data': 0}))
        if len(data) >= 1:
            return True
        else:
            return False

    def set_category_item_count(self, id, action):  # action : + / -
        # perpose : increase or decrease category item count according to the action
        # result : true : successfull, false : failed
        if action == '+':
            data = self.category.update_one(
                {'_id': ObjectId(id)}, {'$inc': {'item_count': 1}})
            if data.modified_count == 1:
                return True
            else:
                return False
        elif action == '-':
            data = self.category.update_one(
                {'_id': ObjectId(id)}, {'$inc': {'item_count': -1}})
            if data.modified_count == 1:
                return True
            else:
                return False

    def insert_food(self, foodData):
        # perpose : insert food item
        # related function : set_category_item_count()
        # result : true : success, false : failed
        data = self.food.insert_one(foodData.dict())
        if data.acknowledged:
            return self.set_category_item_count(foodData.category_id, '+')
        else:
            return False

    def get_food(self):
        # perpose : get all food items
        # result : false : empty list || all food items
        data = list(self.food.find({}))
        if len(data) >= 1:
            foods = [
                model.getFood(
                    id=str(food['_id']),
                    category_id=str(food['category_id']),
                    name=food['name'],
                    description=food['description'],
                    added_data=food['added_data'],
                    modified_data=food['modified_data'],
                    price=[
                        model.FoodDataPrice(
                            name=price['name'],
                            price=price['price'],
                            portion=price['portion']
                        ) for price in food['price']
                    ]
                ).dict() for food in data
            ]
            return jsonable_encoder(foods)
        else:
            return False

    def get_food_non_formated(self, id):
        # perpose : get all food items
        # result : false : empty list || all food items
        data = self.food.find_one({'_id': ObjectId(id)})
        if len(data) >= 1:
            return data
        else:
            return False

    def edit_food(self, foodData):
        # perpose : update food items
        # result : true : successfull || false : failed

        # past data of the category
        pastData = self.get_food_non_formated(foodData.id)

        print('try to excute')
        # update the food item
        data = self.food.update_one({"_id": foodData.id}, {
                                    "$set": foodData.dict(exclude={"id"})})
        if data.acknowledged:
            # update the current and past category item count
            # if foodData['category_id'] != pastData['category_id']:
            if foodData.category_id != pastData['category_id']:
                update_category_new = self.set_category_item_count(
                    foodData.category_id, '+')
                update_category_old = self.set_category_item_count(
                    pastData['category_id'], '-')
                if update_category_new and update_category_old:
                    return True
                else:
                    return False
        else:
            return False

    def remove_food(self, foodId):
        # perpose : delete food item
        # associated function : set_category_item_count()
        # result : true : successfull || false : failed
        food_data = self.food.find_one({'_id': ObjectId(foodId)})
        data = self.food.delete_one({"_id": ObjectId(foodId)})
        if data.deleted_count == 1:
            return self.set_category_item_count(food_data['category_id'], '-')
        else:
            return False

    def check_duplicate_admin_user(self, user):
        # perpose : check duplicate admin user
        # result : true : duplicate, false : not duplicate
        data = self.user.find_one({'email': user.email, 'role': user.role})
        if data == None:
            return False
        else:
            return True

    def insert_admin_user(self, user):
        # perpose : create new admin user
        # result : true : successfull, false : failed
        # code : 401 : unauthorized, 500 : internal server error
        if user.role == 'admin':
            data = self.user.insert_one(user.dict())
            if data.acknowledged:
                return {'status': True, 'code': 200}
            else:
                return {'status': False, 'code': 500}
        # not identify as a admin
        elif user.role != 'admin':
            return {'status': False, 'code': 401}

    def update_secreate_code(self, email):
        # perpose : update secreate code
        # result : status.True : successfull, status.False : failed
        secreate_code = randint(1000, 9999)
        code = self.user.update_one({'email': email}, {'$set': {
                                    'secreate_code': secreate_code, 'send_time': datetime.now(), 'password_change': True}})
        if code.modified_count == 1:
            return {'status': True, 'code': secreate_code}
        else:
            return {'status': False}

    def get_credencials(self, usercredencial):
        # perpose : get user credencials
        # result : false : user not found || found : data
        data = self.user.find_one(
            {'email': usercredencial.email, 'role': usercredencial.role})
        if data != None:
            return data
        else:
            return False

    def check_secreate_code(self, code):
        # perpose : check secreate code
        # result : true : match email and secreate code, false : email or secreate code not matched
        # code : 401 : unauthorized, 404 : email not found
        data = self.user.find_one({'email': code.email})
        if data != None:
            if (data['password_change'] == True and data['secreate_code'] == code.code):
                self.user.update_one({'email': code.email}, {
                                     '$set': {'secreate_code': None, 'send_time': None}})
                return {'status': True, 'code': 200}
            else:
                return {'status': False, 'code': 401}
        else:
            return {'status': False, 'code': 404}

    def check_password_change(self, password):
        # perpose : check whether request password change or not
        # result : true : password change requested, false : not requested
        data = self.user.find_one({'email': password.email})
        if data['password_change'] == True:
            return True
        else:
            return False

    def change_password(self, email, encoded_password):
        # perposer : change password
        # result : true : successfull, false : failed
        data = self.user.update_one({'email': email}, {
                                    '$set': {'password': encoded_password, 'password_change': False}})
        if data.modified_count == 1:
            return True
        else:
            return False

    def change_meal_time(self, mealTime, h, m):
        # perpose : udpate meal time
        # result : true : successfull, false : failed
        shopUpdate = self.shop.update_one(
            {}, {'$set': {mealTime: datetime(year=1970, month=1, day=1, hour=h, minute=m)}})
        if shopUpdate.modified_count == 1:
            return {'status': True, 'code': 200}
        else:
            return {'status': True, 'code': 500}

    def check_meal_time(self, mealTime, h, m):
        # perpose : check other meal time with new meal time
        # related function : change_meal_time()
        # special : 450 : invalied breackfast, 451 : invalied lunch, 452 : invalied dinner
        timeData = self.shop.find_one({})
        # time comparison with other meal times
        if (mealTime == 'breakfast'):
            comparison = timeData['open_time'].time() < datetime(
                year=1970, month=1, day=1, hour=h, minute=m).time() < timeData['lunch'].time()
            if comparison == False:
                return {'status': False, 'code': 450}
            else:
                return self.change_meal_time(mealTime, h, m)
        elif (mealTime == 'lunch'):
            comparison = timeData['breakfast'].time() < datetime(
                year=1970, month=1, day=1, hour=h, minute=m).time() < timeData['dinner'].time()
            if comparison == False:
                return {'status': False, 'code': 451}

            else:
                return self.change_meal_time(mealTime, h, m)
        elif (mealTime == 'dinner'):
            comparison = timeData['lunch'].time() < datetime(
                year=1970, month=1, day=1, hour=h, minute=m).time() < timeData['close_time'].time()
            if comparison == False:
                return {'status': False, 'code': 452}
            else:
                return self.change_meal_time(mealTime, h, m)

    def get_shopdetails_row(self):
        # get all shop details - non-formated for output
        shopData = self.shop.find_one({}, {'_id': 0})
        if shopData != None:
            return shopData
        else:
            return False

    def get_shopdetails(self):
        # get all shop details - formated for output
        shopData = self.shop.find_one({}, {'_id': 0})
        a = jsonable_encoder(shopData)
        data = {
            'open_time': datetime.fromisoformat(a['open_time']).time(),
            'close_time': datetime.fromisoformat(a['close_time']).time(),
            'breakfast': datetime.fromisoformat(a['breakfast']).time(),
            'lunch': datetime.fromisoformat(a['lunch']).time(),
            'dinner': datetime.fromisoformat(a['dinner']).time(),
            'shutdown': a['shutdown']
        }
        return jsonable_encoder(data)

    def update_shop_status(self, current_status):
        # perpose : update the current status of the shop
        # result : true : status updated , false : status update failed
        data = self.shop.update_one(
            {}, {'$set': {'shutdown': not current_status}})
        if data.modified_count == 1:
            return True
        elif data.modified_count == 0:
            return False

    def update_shop_time(self, shopTime, h, m):
        # perpose : update shop time ( opening time and closing time)
        # result : true : successfull, false : failed
        shopUpdate = self.shop.update_one(
            {}, {'$set': {shopTime: datetime(year=1970, month=1, day=1, hour=h, minute=m)}})
        if shopUpdate.modified_count == 1:
            return True
        else:
            return False


def get_database():
    return DataBase()

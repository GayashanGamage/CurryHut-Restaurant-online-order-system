from pymongo import MongoClient, UpdateOne
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
        self.rider = self.db['Rider']
        # rice and curry related category list
        self.plainRiceCategory = '670cbd076e6b240be2d189e4'
        self.curryCategory = '670cbcfd6e6b240be2d189e3'
        self.riceAndCurryCategory = '67ac267debd37b4276c3aebd'

        # undeletable category list
        self.uncategorize = '670cbcf46e6b240be2d189e2'
        self.drinksCategory = '670cbd0e6e6b240be2d189e5'
        self.decertCategory = '670cbd156e6b240be2d189e6'
        self.extraPortionCategory = '67b1baa519f60cfa444a0afc'

    def find_duplicate_location(self, location):
        # perpose : find duplicate name available in the delivery collection - by name
        # return : True : duplicated, False : not duplicated
        data = self.delivery.find_one({'place': location})
        if data != None:
            return True
        else:
            return False

    def find_duplication_location_for_update(self, place, id):
        # perpose : find duplication for update existing delivery location - by name and ID
        # return : True : duplicated, False : not duplicated
        data = list(self.delivery.find({'place': place}))
        if len(data) == 0:
            return False
        elif len(data) >= 1:
            print('this point')
            for item in data:
                if item['_id'] != id:
                    return True
                else:
                    return False
        else:
            return False

    def update_delivery_location(self, cost, place, id, updated_at):
        # perpose : udpate delivery location by id
        # responce : True : successful , False : not updated
        data = self.delivery.update_one({'_id': id}, {
                                        '$set': {'cost': cost, 'place': place, 'updated_at': updated_at}})
        if data.modified_count == 1:
            return True
        else:
            return False

    def insert_delivery_place(self, details):
        # perpose : insert delivery place
        # result : true : successfull, false : failed
        store_data = self.delivery.insert_one(details.dict())
        if store_data.acknowledged:
            return True
        else:
            return False

    def get_delivery_place(self):
        # perpose : get all delivery places
        # result : false : empty list || all delivery places
        data = list(self.delivery.find({}))
        if len(data) > 0:
            # delivery_data = [
            #     model.get_delivery(id=str(delivery['_id']), place=delivery['place'], status=delivery['status'], cost=delivery['cost']).dict() for delivery in data
            # ]
            delivery_data = [
                model.get_delivery_locations(
                    id=str(location['_id']),
                    place=location['place'],
                    cost=location['cost'],
                    status=location['status']
                ).dict() for location in data
            ]

            return jsonable_encoder(delivery_data)
        else:
            return False

    def update_delivery_status(self, details):
        # perpose : update status of the delivery location
        # return : True : successfull, False : not sucessfull
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

    # def get_categories_customer(self):
    #     data = list(self.category.find({'deletable': True}, {
    #                 "aded_date": 0, "last_modify_date": 0, "item_count": 0}))
    #     if len(data) > 0:
    #         categories = [
    #             model.get_categories_customer(id=str(category['_id']), name=category['name'], deletable=category['deletable']).dict() for category in data
    #         ]
    #         return jsonable_encoder(categories)
    #     else:
    #         return data

    def map_available_categories(self, data):
        # perpose : get available unique categories of available foods
        # return : false : categories not available | list : available categories
        unique_categories = []  # get all categories from available foods list
        for item in data:
            unique_categories.append(item['category_id'])
        unique_categories = list(set(unique_categories))

        # find all unique category list
        category_list = list(self.category.find({}))
        if len(category_list) <= 0:
            return False
        elif len(category_list) > 0:
            for item in category_list:
                if item['_id'] in unique_categories:
                    unique_categories.append(
                        # create object category name and category id
                        {'id': str(item['_id']), 'name': item['name']})
        return unique_categories[int(len(unique_categories)/2):]

    def get_foods(self):
        data = list(self.food.find({'category_id': {'$nin': [
                    ObjectId(self.drinksCategory), ObjectId(self.decertCategory), ObjectId(self.uncategorize), ObjectId(self.riceAndCurryCategory), ObjectId(self.curryCategory), ObjectId(self.plainRiceCategory), ObjectId(self.extraPortionCategory)]}}))
        if len(data) > 0:
            available_categories = self.map_available_categories(data)
            if available_categories == False:
                return JSONResponse(status_code=404, content={'message': 'categories not available'})
            else:
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
                return JSONResponse(status_code=200, content={'availability': True, 'data': jsonable_encoder(serialized), 'categories': jsonable_encoder(available_categories)})
        else:
            return JSONResponse(status_code=400, content={'availability': False, 'data': []})

    def getFoodByCategory(self, id, mealtime):
        # perpose : get uncategorize foods form database
        # result : data : successfull | false : not found
        data = list(self.food.find(
            {'category_id': ObjectId(id), mealtime: True}))
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
        elif len(data) == 0:
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
        elif data != None:
            return True

    # this is duplicated function -------------------------------------------
    def check_deletable_category(self, id):
        # perpose : check category is deletable or not
        # result : true : deletable, false : not deletable
        data = self.category.find_one({'_id': ObjectId(id), "deletable": True})
        if data != None:
            return True
        else:
            return False

    def delete_category(self, id):
        # perspose : delete category by id
        # result : true : seccussfull, false : unsuccessfull
        data = self.category.delete_one({'_id': ObjectId(id)})
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
                model.getCategories(
                    id=str(category['_id']),
                    name=category['name'],
                    aded_date=category['aded_date'],
                    last_modify_date=category['last_modify_date'],
                    # item_count=category['item_count'],
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

    def check_undeletable_category(self, id):
        # perpose : check provided category is undeletable or not
        # result : false - category is deletable | true : category is undeletable
        data = self.category.find_one(
            {'_id': ObjectId(id), 'deletable': False})
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
        # perpose : check duplicate food item ( only check names. not idsz )
        # result : true : duplicate, false : not duplicate
        data = list(self.food.find({'name': foodName.lower()}, {
                    '_id': 0, 'category_id': 0, 'description': 0, 'price': 0, 'added_data': 0, 'modified_data': 0}))
        if len(data) >= 1:
            return True
        else:
            return False

    def check_duplication_indetails(self, food_name, food_id):
        # perpose : check duplicate food item ( check both food name and food id )
        # result : true : duplicate, false : not duplicate
        data = list(self.food.find({'name': food_name}, {
                    'category_id': 0, 'description': 0, 'price': 0, 'added_data': 0, 'modified_data': 0}))
        if len(data) >= 1:
            for item in data:
                if item['_id'] != ObjectId(food_id) and food_name == item['name']:
                    return True
            return False
        elif len(data) == 0:
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
                    id=str(food['_id']),
                    category_id=str(food['category_id']),
                    name=food['name'],
                    description=food['description'],
                    added_data=food['added_data'],
                    modified_data=food['modified_data'],
                    breakfast=food['breakfast'],
                    lunch=food['lunch'],
                    dinner=food['dinner'],
                    availability=food['availability'],
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
        data = self.food.update_one({"_id": foodData.id}, {
            "$set": foodData.dict(exclude={"id"})})
        if data.modified_count == 1:
            return True
        else:
            return False

    def remove_food(self, foodId):
        # perpose : delete food item
        # result : true : successfull || false : failed
        food_data = self.food.find_one({'_id': ObjectId(foodId)})
        data = self.food.delete_one({"_id": ObjectId(foodId)})
        if data.deleted_count == 1:
            return True
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
        # return : dataset : successfull, false : cannot find related data
        shopData = self.shop.find_one({}, {'_id': 0})
        if shopData == None:
            return False
        elif shopData != None:
            # formating the data
            data = model.shop_details(** shopData)
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

    def check_duplicate_rider(self, rider):
        # perpose : check duplicate rider
        # result : true : duplicate, false : not duplicate
        params = {'$or': [
            {'driving_licens_number': rider.driving_licens_number},
            {'vehicle_number': rider.vehicle_number},
            {'nic_number': rider.nic_number},
            {'mobile': rider.mobile},
        ]}

        data = list(self.rider.find(params))
        if len(data) == 0:
            return False
        elif len(data) >= 1:
            return True

    def insert_rider(self, rider):
        # perpose : insert new rider
        # result : true : successfull, false : failed
        data = self.rider.insert_one(rider.dict())
        if data.acknowledged:
            return True
        else:
            return False

    def compleate_all_orders(self, id):
        # perpose : check rider on the way to delivery or not
        # result : true : completed, false : not completed
        data = self.rider.find_one(
            {'_id': ObjectId(id), 'available': True, 'order_count': 0})
        if data != None:
            return True
        elif data == None:
            return False

    def remove_rider(self, id):
        # perpose : remove rider
        # result : true : successfull, false : failed
        data = self.rider.delete_one({'_id': ObjectId(id)})
        if data.deleted_count == 1:
            return True
        else:
            return False

    def store_secreate_code(self, details):
        # perpose : store secreate code in the database
        # result : True : successfull store, false : secrete code not store
        data = self.rider.find_one_and_update({'mobile': details.mobile}, {
            '$set': {'secreate_code': details.secreate_code, 'verification': False}})
        if data != None:
            return True
        else:
            return False

    def update_rider_contact(self, details):
        # perpose : update existing riders contact number
        # result : true : successfull, false : failed
        data = self.rider.find_one_and_update({'mobile': details.old_mobile, 'verification': False}, {
            "$set": {"mobile": details.new_mobile, 'secreate_code': 0, 'verification': True, 'verified_at': datetime.now()}})
        if data != None:
            return True
        elif data == None:
            return False

    def orders_compleated_and_return(self, id):
        # perpose : check all oders compleated and return to the shop when log of (false) the rider
        # result : true : successfull, false : failed
        data = self.rider.find_one(
            {'_id': ObjectId(id), 'order_count': 0, 'available': True})
        if data != None:
            return True
        else:
            return False

    def switch_rider_log(self, id):
        # perpose : switch the riders log status ( true or false)
        # result : true : successfull, false : failed
        data = self.rider.find_one_and_update({'_id': ObjectId(id)},
                                              [{'$set': {'log': {'$not': '$log'}}}])
        print(data)
        if data != None:
            return True
        elif data == None:
            return False

    def get_all_riders(self):
        # perpose : get all riders
        # return : false : no any riders , data : all riders
        data = list(self.rider.find({}))
        if data != None:
            all_riders = [
                model.AllRiders(
                    id=str(rider['_id']),
                    mobile=rider['mobile'],
                    verification=rider['verification'],
                    first_name=rider['first_name'],
                    last_name=rider['last_name'],
                    nic_number=rider['nic_number'],
                    driving_licens_number=rider['driving_licens_number'],
                    vehicle_number=rider['vehicle_number'],
                    log=rider['log'],
                    order_count=rider['order_count'],
                    available=rider['available'],
                    # available : if rider lear for delivery set to false,  otherwise true
                    created_at=rider['created_at'],
                ) for rider in data
            ]
            return jsonable_encoder(all_riders)
        else:
            return False

    def update_menu(self, menu):
        # perpose : update menu as a bulk
        # result : true : successfull, false : failed
        updatedData = [
            UpdateOne(
                {'_id': food.id},
                {'$set': {'breakfast': food.breakfast,
                          'lunch': food.lunch, 'dinner': food.dinner, 'availability': food.availability}}
            ) for food in menu.menu
        ]
        updated = self.food.bulk_write(updatedData)
        if updated.acknowledged:
            return True
        else:
            return False

    def update_menu_status(self):
        # perpose : identify whether today's manu is available or not. end of the day this becume a false -
        data = self.shop.update_one({}, {'$set': {'menu': True}})
        if data.acknowledged:
            return True
        else:
            return False

    def check_meal_time_by_id(self, id):
        # perpose : check any meal is set for any of meal time.
        # return : true - set for meal time, false : not set for any meal time
        data = self.food.find_one({'_id': ObjectId(id)})
        # when the data is not available
        if data == None:
            return False
        else:
            if data['breakfast'] == True or data['lunch'] == True or data['dinner'] == True:
                return True
            else:
                return False

    def update_availability(self, id):
        data = self.food.update_one({"_id": ObjectId(id)}, [
                                    {'$set': {'availability': {'$not': f'$availability'}}}])
        if data.modified_count == 1:
            return True
        else:
            return False

    def riceAndCurryData(self, mealTime):
        # perpose : get matched rice and curry, curries and rice from food collection
        # return : ?
        data = list(self.food.find({
            '$and': [
                {'category_id': {
                    '$in': [ObjectId(self.plainRiceCategory), ObjectId(self.curryCategory), ObjectId(self.riceAndCurryCategory)]
                }},
                {mealTime: True}
            ]
        }))
        if len(data) == 0:
            return {'status': False, 'data': []}
        else:
            curryCount = 0
            riceCount = 0
            riceAndCurry = 0
            for item in data:
                if str(item['category_id']) == self.curryCategory:
                    curryCount += 1
                elif str(item['category_id']) == self.plainRiceCategory:
                    riceCount += 1
                elif str(item['category_id']) == self.riceAndCurryCategory:
                    riceAndCurry += 1
            if curryCount <= 2 or riceCount <= 0 or riceAndCurry == 0:
                return {'status': False, 'data': []}
            else:
                curry = [
                    model.curry(
                        id=str(item["_id"]),
                        name=item['name'],
                        availability=item['availability']
                    ) for item in data if str(item['category_id']) == self.curryCategory

                ]
                plain_rice = [
                    model.plain_rice(
                        id=str(item["_id"]),
                        name=item['name'],
                        availability=item['availability']
                    ) for item in data if str(item['category_id']) == self.plainRiceCategory

                ]
                rice_and_curry = [
                    model.rice_and_curry_pack(
                        id=str(item["_id"]),
                        name=item['name'],
                        availability=item['availability'],
                        price=[
                            model.FoodDataPrice(
                                name=i['name'],
                                price=i['price'],
                                portion=i['portion']
                            ) for i in item['price']
                        ]
                    ) for item in data if str(item['category_id']) == self.riceAndCurryCategory

                ]
                return {'status': True, 'curry': jsonable_encoder(curry), 'rice': jsonable_encoder(plain_rice), 'rice&curry': jsonable_encoder(rice_and_curry)}


def get_database():
    return DataBase()

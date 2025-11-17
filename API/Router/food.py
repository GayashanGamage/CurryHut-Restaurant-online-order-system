from fastapi import APIRouter, Depends, Path
from Dependencies import database
from Dependencies import model, authontication
from fastapi.responses import JSONResponse
from .docs.doc_food import doc

route = APIRouter(tags=['food'])

db = database.get_database()


@route.post('/addfooditem', **doc['addfooditem'])
async def addFoodItem(foodData: model.FoodData, data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')

    # check dubplicate food item name and category id
    duplicate_food = db.check_dubplicate_food(foodData.name)
    check_category = db.check_category_id(foodData.category_id)

    if duplicate_food == False and check_category == True:
        # insert food item
        food_data = db.insert_food(foodData)
        if food_data == True:
            return JSONResponse(status_code=200, content={"messege": 'successfull'})
        else:
            return JSONResponse(status_code=500, content={"messege": 'something went wrong'})
    elif check_category == False:
        return JSONResponse(status_code=404, content={"messege": 'category id not found'})
    elif duplicate_food == True:
        return JSONResponse(status_code=400, content={"messege": 'duplicate food item'})


@route.get('/getallfood', **doc['getallfood'])
async def getAllFood(data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # send all food
    else:
        food_data = db.get_food()
        if food_data == False:
            return JSONResponse(status_code=404, content={})
        else:
            return JSONResponse(status_code=200, content=food_data)


@route.patch('/editfood', **doc['editfood'])
async def editFoof(editfood: model.EditFood, data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # check if _id is exist
    else:
        # check current category id is available
        check_category = db.check_category_id(editfood.category_id)
        if check_category == False:
            return JSONResponse(status_code=404, content={"messege": "category id not found"})
        # check current name in other document in the collection
        check_name = db.check_duplication_indetails(editfood.name, editfood.id)
        if check_name == True:
            return JSONResponse(status_code=400, content={"message": "food items cannot duplicate"})
        # update food item
        update_food = db.edit_food(editfood)
        if update_food == False:
            return JSONResponse(status_code=500, content={"messege": 'something went wrong - server'})
        else:
            return JSONResponse(status_code=200, content={"messege": 'successfull'})


@route.delete('/deletefood/{foodId}', **doc['deletefood'])
async def deleteFood(foodId: str = Path(description="food ID"),
                     data=Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # try to delete food
    else:
        food_data = db.remove_food(foodId)
        if food_data == False:
            return JSONResponse(status_code=500, content={"messege": "cannot remove from database"})
        elif food_data == True:
            return JSONResponse(status_code=200, content={"messege": 'successfull'})

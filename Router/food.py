from fastapi import APIRouter, Depends
from Dependencies import database
from Dependencies import model, authontication
from fastapi.responses import JSONResponse

route = APIRouter( tags=['food'])

db = database.get_database()


@route.post('/addfooditem')
async def addFoodItem(foodData : model.FoodData, data = Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    
    # check dubplicate food item name and category id
    duplicate_food = db.check_dubplicate_food(foodData.name)
    check_category = db.check_category_id(foodData.category_id)
    
    if duplicate_food == False and check_category == True:
        # insert food item
        food_data = db.insert_food(foodData)
        if food_data == True:
            return JSONResponse(status_code=200, content='successfull')
        else:
            return JSONResponse(status_code=500, content='something went wrong')
    elif check_category == False:
        return JSONResponse(status_code=404, content='category id not found')
    elif duplicate_food == True:
        return JSONResponse(status_code=400, content='duplicate food item')
        
    
@route.get('/getallfood')
async def getAllFood(data = Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # send all food 
    else:
        food_data = db.get_food()
        if food_data == False:
            return JSONResponse(status_code=404, content={})
        else:
            return JSONResponse(status_code=200, content=food_data)

@route.patch('/editfood')
async def editFoof(editfood : model.EditFood, data = Depends(authontication.authVerification)):
    # check authontication
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # check if _id is exist
    else:
        food_data = db.edit_food(editfood)
        if food_data == False:
            return JSONResponse(status_code=500, content='something went wrong - server')
        elif food_data == True:
            return JSONResponse(status_code=200, content='successfull')


@route.delete('/deletefood/{foodId}')
async def deleteFood( foodId : str, data = Depends(authontication.authVerification)):
    # check authontication 
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    # try to delete food 
    else:
        food_data = db.remove_food(foodId)
        if food_data == False:
            return JSONResponse(status_code=404, content='item connot found')
        elif food_data == True:
            return JSONResponse(status_code=200, content='successfull')
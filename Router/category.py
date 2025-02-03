from fastapi import APIRouter, Depends
from Dependencies.model import Category
from Dependencies import authontication
from fastapi.responses import JSONResponse
from Dependencies import database

route = APIRouter(prefix="/category", tags=["category"])
db = database.get_database()


@route.post('/addcategory')
async def addCategory(categoryData: Category, data=Depends(authontication.authVerification)):
    # send error message if not authonticated
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # find dubplicate category
    check_duplication = db.check_dubplicate_categories(categoryData.name)
    if check_duplication == False:
        # insert category data to the database
        insert_data = db.insert_category(categoryData)
        if insert_data == True:
            return JSONResponse(status_code=200, content='successfull')
        elif insert_data == False:
            return JSONResponse(status_code=500, content='something go wrong')
    elif check_duplication == True:
        return JSONResponse(status_code=400, content='duplicate category')


@route.patch('/editcategory')
async def editCategory(id: str, categoryName: str, data=Depends(authontication.authVerification)):
    # if not authonticate, then send error message
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # check duplicate category name
        duplicated = db.check_dubplicate_categories(categoryName)
        if duplicated['status'] == True and str(duplicated['data'][0]['_id']) != id:
            return JSONResponse(status_code=400, content='cannot duplicate category')
        # check category is deletable or not
        elif db.check_deletable_category(id) == False:
            return JSONResponse(status_code=401, content='unEditable category')
        else:
            # update category name
            updatedData = db.update_category(id, categoryName)
            # false : id not found
            if updatedData == False:
                return JSONResponse(status_code=404, content="category not found")
            elif updatedData == True:
                return JSONResponse(status_code=200, content='successfull')


@route.delete('/deletecategory/{categoryId}')
async def deleteCategory(categoryId: str, data=Depends(authontication.authVerification)):
    # check authontication validation
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # delete category
        deleted_data = db.delete_category(categoryId)
        if deleted_data['status'] == True:
            # update foods category to "uncategory"
            # -> 670cbcf46e6b240be2d189e2 is the default "uncategory" id by default
            update_foods = db.update_food_list(
                categoryId, '670cbcf46e6b240be2d189e2')
            if update_foods == True:
                return JSONResponse(status_code=200, content='successfull')
            else:
                return JSONResponse(status_code=500, content='something go wrong - server')

        elif deleted_data['code'] == 401:
            return JSONResponse(status_code=401, content='undeleteable category')
        elif deleted_data['code'] == 500:
            return JSONResponse(status_code=500, content='something go wrong - server')
        elif deleted_data['code'] == 404:
            return JSONResponse(status_code=404, content='category not found')


@route.get('/getcategories')
async def getCategories(data=Depends(authontication.authVerification)):
    # authontication validation
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # get all data
        category_list = db.get_categories()
        if category_list == False:
            return JSONResponse(status_code=404, content='{}')
        else:
            return JSONResponse(status_code=200, content=category_list)

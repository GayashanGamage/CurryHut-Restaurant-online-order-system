from fastapi import APIRouter, Depends
from Dependencies.model import Category
from Dependencies import authontication
from fastapi.responses import JSONResponse
from Dependencies import database

route = APIRouter(prefix="/category", tags=["edited"])
db = database.get_database()


@route.post('/addcategory')
async def addCategory(categoryData : Category, data  = Depends(authontication.authVerification)):
    # send error message if not authonticated
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # find dubplicate category
    if( db.check_dubplicate_categories(categoryData.name) == False):
        # insert category data to the database
        if( db.insert_category(categoryData) == True):
            return JSONResponse(status_code=200, content='successfull')
        else:
            return JSONResponse(status_code=500, content='something go wrong')
    else:
        return JSONResponse(status_code=400, content='duplicate category')
    
@route.patch('/editcategory')
async def editCategory(id : str, categoryName : str,data  = Depends(authontication.authVerification)):
    # if not authonticate, then send error message
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    else:
        # check duplicate category name
        if ( db.check_dubplicate_categories(categoryName) == False):
            # update category name
            updatedData = db.update_category(id, categoryName)
            # false : id not found
            if updatedData == False:
                return JSONResponse(status_code=400, content="Id not found")
            elif updatedData == True:
                return JSONResponse(status_code=200, content='successfull')
        else:
            return JSONResponse(status_code=400, content='cannot duplicate category')
    
@route.delete('/deletecategory/{categoryId}')
async def deleteCategory(categoryId : str, data = Depends(authontication.authVerification)):
    # check authontication validation
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    else:
        # delete category
        deleted_data = db.delete_category(categoryId)
        if deleted_data == True:
            return JSONResponse(status_code=200, content='successfull')
        elif deleted_data == False:
            return JSONResponse(status_code=400, content='something go wrong')
        
@route.get('/getcategories')
async def getCategories(data = Depends(authontication.authVerification)):
    # authontication validation
    if data == False or data['role'] != 'admin':
        return JSONResponse( status_code=401, content='unathorized')
    else:
        # get all data
        category_list = db.get_categories()
        if category_list == False:
            return JSONResponse(status_code=404, content='{}')
        else:
            return JSONResponse(status_code=200, content=category_list)
        
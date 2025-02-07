from fastapi import APIRouter, Depends, Query, Path
from Dependencies.model import Category
from Dependencies import authontication
from fastapi.responses import JSONResponse
from Dependencies import database
from .docs.doc_category import doc

route = APIRouter(prefix="/category", tags=["category"])
db = database.get_database()


@route.post('/addcategory', **doc['addcategory'])
async def addCategory(categoryData: Category, data=Depends(authontication.authVerification)):
    # send error message if not authonticated
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    # find dubplicate category
    check_duplication = db.check_dubplicate_categories(categoryData.name)
    if check_duplication['status'] == False:
        # insert category data to the database
        insert_data = db.insert_category(categoryData)
        if insert_data == True:
            return JSONResponse(status_code=200, content={"message": 'successfull'})
        elif insert_data == False:
            return JSONResponse(status_code=500, content={"message": 'something go wrong'})
    elif check_duplication['status'] == True:
        return JSONResponse(status_code=400, content={"message": 'duplicate category'})


@route.patch('/editcategory', **doc['editcategory'])
async def editCategory(id: str = Query(description='category id'),
                       categoryName: str = Query(description='category name'),
                       data=Depends(authontication.authVerification)):
    # if not authonticate, then send error message
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # check duplicate category name
        duplicated = db.check_dubplicate_categories(categoryName)
        if duplicated['status'] == True and str(duplicated['data'][0]['_id']) != id:
            return JSONResponse(status_code=400, content={"message": 'cannot duplicate category'})
        # check category is deletable or not
        elif db.check_deletable_category(id) == False:
            return JSONResponse(status_code=403, content={"message": 'un-editable category'})
        else:
            # update category name
            updatedData = db.update_category(id, categoryName)
            # false : id not found
            if updatedData == False:
                return JSONResponse(status_code=404, content={"message": "category not found"})
            elif updatedData == True:
                return JSONResponse(status_code=200, content={"message": 'successfull'})


@route.delete('/deletecategory/{categoryId}', **doc['deletecategory'])
async def deleteCategory(categoryId: str = Path(description='category id'),
                         data=Depends(authontication.authVerification)):
    # check authontication validation
    if data == False or data['role'] != 'admin':
        return JSONResponse(status_code=401, content='unathorized')
    else:
        # check deletable or not
        deletable = db.check_deletable_category(categoryId)
        if deletable == True:
            # delete category
            delete_category = db.delete_category(categoryId)
            if delete_category == True:
                return JSONResponse(status_code=200, content={"message": 'successfull'})
            else:
                return JSONResponse(status_code=500, content={"message": 'something go wrong - server'})
        else:
            return JSONResponse(status_code=400, content={"message": 'un deletable category'})


@route.get('/getcategories', **doc['getcategories'])
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

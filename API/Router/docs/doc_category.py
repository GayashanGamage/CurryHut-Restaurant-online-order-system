doc = {
    'addcategory': {
        'summary': 'add new category',
        'description': 'add new category to the database. this will help admin to organize the food items',
        'responses':
        {
            200: {"description": "category create successfully",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "category cannot dubplicated by name",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'duplicate category'}
                           }
                       }
                  },
            500: {"description": "due to some reason, category cannot insert to the database",
                  "content":
                      {"application/json":
                          {"example":
                           {"message": 'something go wrong'}
                           }
                       }
                  },
        },
    },
    'editcategory': {
        'summary': 'edit selected category',
        'description': 'if provided category name is not duplicate, then update the category name',
        'responses':
        {
            200: {"description": "category update successfully",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "category cannot dubplicated by name",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'canot duplicate category'}
                           }
                       }
                  },
            403: {"description": "un deletable category cannot edit",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'un-editable category'}
                           }
                       }
                  },
            404: {"description": "category id not found",
                  "content":
                      {"application/json":
                          {"example":
                           {"message": "category not found"}
                           }
                       }
                  },
        },
    },
    'deletecategory': {
        'summary': 'delete category by id',
        'description': 'delete the category by selected id. if category is not deletable, then send error message',
        'responses':
        {
            200: {"description": "category deleted successfully",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "un deletable category cannot delete",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'un deletable category'}
                           }
                       }
                  },
            500: {"description": "delete action cannot perform due to some reason",
                  "content":
                      {"application/json":
                          {"example":
                           {"message": 'something go wrong - server'}
                           }
                       }
                  },
        },
    },
    'getcategories': {
        'summary': 'get all categories',
        'description': 'get all available categories from the database',
        'responses':
        {
            200: {"description": "get all categories successfully",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful', "data":
                                       [
                                           {
                                               'id': 'str',
                                               'name': 'category',
                                               'aded_date': 'category',
                                               'last_modify_date': 'category',
                                               'item_count': 'category',
                                               'deletable': 'category'
                                           }
                                       ]

                                       }
                           }
                       }
                  },
            404: {"description": "not available any category",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'not available',
                               'data': {}}
                           }
                       }
                  },
        },
    },

}

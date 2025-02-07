doc = {
    'addfooditem': {
        'summary': 'add new food item',
        'description': 'before add new item it check the given food name is still exsist in the data.',
        'responses':
        {
            200: {"description": "add food item successfuly",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "food items cannot duplicate by its name",
                  "content":
                      {"application/json":
                          {"example":
                              {"messege": 'duplicate food item'}
                           }
                       }
                  },
            404: {"description": "provided category not found in database",
                  "content":
                      {"application/json":
                          {"example":
                              {"messege": 'category id not found'}
                           }
                       }
                  },
            500: {"description": "food item cannot insert in to database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'something went wrong - server'}
                           }
                       }
                  }
        },
    },
    'getallfood': {
        'summary': 'get all food items',
        'description': 'retrieve all available food data from database',
        'responses':
        {
            200: {"description": "get all food items successfuly",
                  "content":
                      {"application/json":
                          {"example":
                              [
                                  {
                                      'id': 'str',
                                      'category_id': 'str',
                                      'name': 'str',
                                      'description': 'str',
                                      'added_data': 'datetime',
                                      'modified_data': 'datetime',
                                      'price': {
                                          "name": 'str',
                                          "price": 'int',
                                          "portion": 'int'
                                      }
                                  }
                              ]
                           }
                       }
                  },
            404: {"description": "food items not found in database",
                  "content":
                      {"application/json":
                          {"example": []}
                       }
                  },
        },
    },
    'editfood': {
        'summary': 'update food items',
        'description': 'update food item - this consider duplication food names in the database',
        'responses':
        {
            200: {"description": "update food item successfuly",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "food items cannot duplicate by its name",
                  "content":
                      {"application/json":
                          {"example":
                              {"messege": 'food item cannot duplicate'}
                           }
                       }
                  },
            500: {"description": "food item cannot update in database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'something went wrong - server'}
                           }
                       }
                  }
        },
    },
    'deletefood': {
        'summary': 'remove food items',
        'description': 'remove food items while category count also update',
        'responses':
        {
            200: {"description": "remove food item successfuly",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful'}
                           }
                       }
                  },
            404: {"description": "due to server error food item cannot remove from database",
                  "content":
                      {"application/json":
                          {"example":
                              {"messege": "cannot remove from database"}
                           }
                       }
                  },
        },
    },
}

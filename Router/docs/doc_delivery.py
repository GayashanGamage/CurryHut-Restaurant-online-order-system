doc = {
    'create': {
        'summary': 'add new delivery location',
        'description': 'this will help you to defined where you delivery locations are available',
        'responses':
        {
            200: {"description": "add new delivery location successfully",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "delivery location cannot dubplicated by name",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'place alredy exist'}
                           }
                       }
                  },
            500: {"description": "due to some reason, delivery location cannot insert to the database",
                  "content":
                      {"application/json":
                          {"example":
                           {"message": 'something go wrong'}
                           }
                       }
                  },
        },
    },
    'get': {
        'summary': 'get all delivery location',
        'description': 'this is allow you to get all documents from delivery locations',
        'responses':
        {
            200: {"description": "",
                  "content":
                      {"application/json":
                          {"example":
                              {'data': [{
                                  'id': 'str',
                                  "place": 'str',
                                  "cost": 'int',
                                  "status": 'bool'

                              }]
                              }
                           }
                       }
                  },
            400: {"description": "not available delivery location",
                  "content":
                      {"application/json":
                          {"example":
                              {"date": []}
                           }
                       }
                  },
        },
    },
    'update': {
        'summary': 'update delivery location',
        'description': 'this may help you to update lacation as well as cost',
        'responses':
        {
            200: {"description": "",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'success'}
                           }
                       }
                  },
            400: {"description": "delivery location cannot duplicated by name",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": "delivery place cannot duplicated"}}
                       }
                  },
            500: {"description": "due to some reason, delivery location cannot insert to the database",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'database cannot update - server'}}
                       }
                  },
        },

    },
    'set-status': {
        'summary': 'set availability of the delivery location',
        'description': 'due to some reason, admin want to set unvailable for some delivery location without deleting, this may help',
        'responses':
        {
            200: {"description": "update status of the delivery location successfully",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'success'}
                           }
                       }
                  },
            500: {"description": "due to some reason database cannot update - server",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": "faild"}}
                       }
                  },
        },

    },
    'delete': {
        'summary': 'delete delivery location',
        'description': 'permanatly remove delivery location from the system',
        'responses':
        {
            200: {"description": "delete delivery location successfuly",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'success'}
                           }
                       }
                  },
            500: {"description": "due to some reason location cannot update - server",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": "faild"}}
                       }
                  },
        },

    },
}

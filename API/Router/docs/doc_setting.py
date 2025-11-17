doc = {
    'changeMealTime': {
        'summary': 'change meal time - breakfast, lunch and dinner',
        'description': 'this is for change meal time. according to the current time available meals will be shown. for that we need to schedule the breakfast, luncha and dinner start.',
        'responses':
        {
            200: {"description": "meal time change successfully",
                  "content":
                      {"application/json":
                          {"example": {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "provide meal time conflict with existing meal times",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'invalied { meal name } time '}
                           }
                       }
                  },
            404: {"description": "provide an invalied meal name",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'invalied meal-name'}
                           }
                       }
                  },
            406: {"description": "provid invalied time",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'invalied time'}
                           }
                       }
                  },
            500: {"description": "time change cannot update in database",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'something went wrong - server'}
                           }
                       }
                  }
        },
    },
    'shopdetails': {
        'summary': 'get all shop details',
        'description': 'this is provide shop related time(open and close time), meal related time(breakfast, lunch and dinner) and status of the shop(shutdown or not)',
        'responses':
        {
            200: {"description": "successfully retrieve all data",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'successful', 'data':
                               {
                                   'open_time': 'datetime',
                                   'close_time': 'datetime',
                                   'breakfast': 'datetime',
                                   'lunch': 'datetime',
                                   'dinner': 'datetime',
                                   'shutdown': 'bool'
                               }}}}},
            400: {"description": "provide meal time conflict with existing meal times",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'invalied { meal name } time '}
                           }
                       }
                  },
            401: {"description": "provide an invalied meal name",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'invalied meal-name'}
                           }
                       }
                  },
            500: {"description": "time change cannot update in database",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'something went wrong - server'}
                           }
                       }
                  }
        },
    },
    'changeShopTime': {
        'summary': 'change opening and close time',
        'description': 'this is for change shop opening and close time.',
        'responses':
        {
            200: {"description": "shop time change successfully",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "this don't allow you to set open time conflict with close time and also don't allow to set close time conflict with open time ",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'you cannot set close time conflicting with existing shop times.'}
                           }
                       }
                  },
            404: {"description": "if time description is not valied this may occur. ex : spelling mistakes",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'time description is not matched'}
                           }
                       }
                  },
            500: {"description": "if database not update properlly, this may occur",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'something went wrong - server'}
                           }
                       }
                  },

        },
    },
    'operationhold': {
        'summary': 'sudden change of the shop status',
        'description': 'this is allow admin to sudden close due to some reason. after that allow to open again. but while closing this cannot do anything',
        'responses':
        {
            200: {"description": "successfully done sudden close and then open again",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'successfuly open | close'}
                           }
                       }
                  },
            400: {"description": "this don't allow even admin to open the shop during close time",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': "cannot perform this operation while it's close time "}
                           }
                       }
                  },

        },
    },

}

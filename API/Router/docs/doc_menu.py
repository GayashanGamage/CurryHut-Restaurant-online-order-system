docs = {
    'add': {
        'summary': 'update todays menu',
        'description': 'this allow you to update todays menu. if admin set a menu for paticular date, then only that menu will be available for that date.',
        'responses':
        {
            200: {"description": "successfully add / update menu",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'successful'}
                           }
                       }
                  },
            500: {"description": "menu cannot update in the database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'something went wrong - server'}
                           }
                       }
                  },

        },
    },
    'set-availability': {
        'summary': 'set availability of food item',
        'description': 'if any of meal time true ( breakfast, lunch, dinner ), then it is allow to set availability. otherwise raise an error. toggle between previose value of the availability.',
        'responses':
        {
            200: {"description": "successfully add / update menu",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "this is not available on today's menu. due to this reason, this is not allow to set availability",
                  "content":
                      {"application/json":
                          {"example":
                           {"message": "cannot set availability for this item"}
                           }
                       }
                  },
            500: {"description": "menu cannot update in the database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": "something went wrong - server"}
                           }
                       }
                  },

        },
    }
}

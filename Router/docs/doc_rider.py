doc = {
    'add': {
        'summary': 'add new rider',
        'description': 'this is allow admin to add new riders. but NIC, vehicle registration number, driving license number cannot duplicated',
        'responses':
        {
            200: {"description": "successfully add rider in to the system",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'successful'}
                           }
                       }
                  },
            400: {"description": "driving license number, NIC, vehicle registration number are duplicated",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'some or all rider details alreddy in the system'}
                           }
                       }
                  },
            500: {"description": "rider details cannot store in the database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'something went wrong - server'}
                           }
                       }
                  },
            503: {"description": "sms cannot send due to some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'sms cannot send'}
                           }
                       }
                  },

        },
    },
    'delete': {
        'summary': 'delete rider is he compleate all deliveries and return to the shop',
        'description': 'this is not allow to delete rider if he is not compleate all deliveries and return to the shop - for this use deleteforce endpoint. otherwise this excute delete operation',
        'responses':
        {
            200: {"description": "successfully add rider in to the system",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'successful'}
                           }
                       }
                  },
            401: {"description": "if rider on the way to delivery, without admini's credencials cannot remove rider",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'rider cannot remove - on the way to deliver'}
                           }
                       }
                  },
            500: {"description": "cannot excute delete operation in database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'something went wrong - server'}
                           }
                       }
                  },


        },
    },
    'update': {
        'summary': 'update rider contact number',
        'description': 'after add new rider, it is only allow to update the contact number of the rider',
        'responses':
        {
            200: {"description": "successfully add rider in to the system",
                  "content":
                      {"application/json":
                          {"example":
                              {'message': 'successful'}
                           }
                       }
                  },
            500: {"description": "cannot update rider's contact on database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'something went wrong - server'}
                           }
                       }
                  },
            503: {"description": "cannot send sms due to some reason from msm service provider",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'message cannot send - server'}
                           }
                       }
                  },


        },
    },
    'all': {
        'summary': 'get all riders',
        'description': 'get all riders details from the database',
        'responses':
        {
            200: {"description": "retrieve all riders data",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'successful', 'data': {
                                  'id': 'str',
                                  'mobile': 'int',
                                  'verification': 'bool',
                                  'first_name': 'str',
                                  'last_name': 'str',
                                  'nic_number': 'str',
                                  'driving_licens_number': 'str',
                                  'vehicle_number': 'str',
                                  'log': 'bool',
                                  'order_count': 'int',
                                  'available': 'bool',
                                  'created_at': 'datetime',
                              }
                              }
                           }
                       }
                  },
            400: {"description": "no riders available in the system",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'no riders found'}
                           }
                       }
                  },


        },
    },
    'log': {
        'summary': 'set available status of the rider',
        'description': 'set as available rider for todays delivery',
        'responses':
        {
            200: {"description": "successfully set riders status",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'successful'}
                           }
                       }
                  },
            400: {"description": "rider cannot log off if he is on the way to delivery",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'rider on the way to delivery'}
                           }
                       }
                  },
            500: {"description": "cannot update rider's status in database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'something went wrong - server'}
                           }
                       }
                  },


        },
    },
    'deleteforce': {
        'summary': 'delete rider with administrator permision',
        'description': 'if on they way to rider want to remove from the system, this should be trigger with administrators permisions',
        'responses':
        {
            200: {"description": "successfully delete rider from the system",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'successful'}
                           }
                       }
                  },
            500: {"description": "cannot delete rider from the database for some reason",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'something went wrong - server'}
                           }
                       }
                  },


        },
    },
    'numberVerification': {
        'summary': 'delete rider with administrator permision',
        'description': 'if on they way to rider want to remove from the system, this should be trigger with administrators permisions',
        'responses':
        {
            200: {"description": "successfully delete rider from the system",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'successful'}
                           }
                       }
                  },
            400: {"description": "cannot find riders details on database",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'riders information not found'}
                           }
                       }
                  },
            503: {"description": "cannot send sms due service providers reason",
                  "content":
                      {"application/json":
                          {"example":
                              {"message": 'sms cannot send due to service providers errro'}
                           }
                       }
                  },


        },
    },

}

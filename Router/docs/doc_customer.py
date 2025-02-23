doc = {
    'riceAndCurry': {
        'summary': 'get rice and curry category according to the time manner',
        'description': 'if that rice/ curry / rice and curry pack available only for lunch then it load only  for lunch time. if rice count is 0 or if curry count less than or equal to two or rice and curry pakage is not available then this part show and empty list',
        'responses': {
            200: {
                "description": "rice and curry get successfully",
                "content": {
                    "application/json": {
                        "example": {
                            'curry': [
                                {
                                    'id': 'str',
                                    'name': 'str',
                                    'availability': 'bool',
                                }
                            ],
                            'rice': [
                                {
                                    'id': 'str',
                                    'name': 'str',
                                    'availability': 'bool',
                                }
                            ],
                            'rice&curry': [
                                {
                                    'id': 'str',
                                    'name': 'str',
                                    'availability': 'bool',
                                    'price': [
                                        {
                                            'name': 'str',
                                            'price': 'int',
                                            'portion': 'int',
                                        }
                                    ]
                                }
                            ]
                        }

                    }
                }
            },
            400: {
                "description": "request during shop close time",
                "content": {
                    "application/json": {
                        "example": {
                            "message": 'shop is closed'
                        }
                    }
                }
            },
            404: {
                "description": "we cannot serve rice and curry due to shortage or one item from curry, rice or rice and curry package",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'rice and curry not available'
                        }
                    }
                }
            },
        }
    },
    'undeletableCategory': {
        'summary': 'get food by undeletabl category id',
        'description': 'get all foods those are related to undeletable category',
        'responses': {
            200: {
                "description": "get all foods successfuly",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'succssfull',
                            'data': [
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
                }
            },
            404: {
                "description": "foods are not available under mentioned category",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'foods not available',
                            'data': []
                        }
                    }
                }
            },
            400: {
                "description": "provided category is deletable.",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'category is deletable'
                        }
                    }
                }
            },
        }
    },
    'getFood': {
        'summary': 'get all deletable foods and related category list',
        'description': 'get all foods those are deletable and related category list',
        'responses': {
            200: {
                "description": "get all foods successfuly",
                "content": {
                    "application/json": {
                        "example": {
                            'availability': 'bool',
                            'data': [
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
                            ],
                            'categories': [
                                {
                                    'id': 'str',
                                    'name': 'str'
                                }
                            ]
                        }

                    }
                }
            },
            403: {
                "description": "shop is closed or shutdown",
                "content": {
                    "application/json": {
                        "example": {
                            'open_time': 'datetime',
                            'close_time': 'datetime',
                            'shutdown': 'bool'
                        }
                    }
                }
            },
        }
    },
    'mobile': {
        'summary': 'check contact number is verified or not',
        'description': 'check the contact number in customer collection. if so check verified or not. if not verified send serification code. if contact number is not in customer collection create new customer',
        'responses': {
            200: {
                "description": "successfull - there are several options by 'status' in return value. 1000 : new account created. 1001 : alredy verified number. 1002 : verification code send to provide mobile number ( not verified number )",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'str',
                            'status': 'int - 1000 | 1001 | 1002',
                            'customer': 'str - masked customer contact number'
                        }
                    }
                }
            },
            500: {
                "description": "customer database not update expectedly",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'str',
                        }
                    }
                }
            },
        }
    },
    'customerKey': {
        'summary': 'contact number identify by masked customer key',
        'description': 'check contact number by customer key.',
        'responses': {
            200: {
                "description": "contact number identified by customer key. but base on the verified status it's give responce. 1000 : unverified customer. 1001 : alredy verified customer",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'str',
                            'status': 'int - 1000 | 1001',
                            'mobile_number': 'str - 071****098'
                        }
                    }
                }
            },
            404: {
                "description": "customer database not update expectedly",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'str',
                        }
                    }
                }
            },
        }
    },
    'verification': {
        'summary': 'contact number verification',
        'description': 'when create a new customer by new mobile number, it should verify by the verification code that send to customers mobile via sms',
        'responses': {
            200: {
                "description": "successfully verified contact number",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'str',
                        }
                    }
                }
            },
            406: {
                "description": "user provide secreate key and masked contact number are not matche",
                "content": {
                    "application/json": {
                        "example": {
                            'message': 'str',
                        }
                    }
                }
            },
        }
    },
}

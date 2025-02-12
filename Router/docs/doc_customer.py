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
    }
}

import requests


def sendSMS(number, message):
    # perpose : send message to the given number
    # result : true - success, false - failed
    parms = {
        'user_id': 28987,
        'api_key': 'QZ9NIjExYd4xiIEjYraf',
        'sender_id': 'NotifyDEMO',
        'to': number,
        'message': message

    }
    data = requests.post('https://app.notify.lk/api/v1/send', data=parms)
    if data.json()['status'] == 'success':
        return True
    else:
        return False

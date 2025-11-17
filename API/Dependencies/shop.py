from . import database
from . import model
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import pytz

db = database.get_database()


def doesShopOpen():
    # perpose : check whether shop is open or close
    # return : True : open, False : closed ( in this case it show the reason for close status (shutdown / closed))
    data = db.get_shop_details('66ff86b140ba8d2eaa1eb88a')
    timeZoon = pytz.timezone('Asia/Colombo')
    currentTime = datetime.now(timeZoon).time()
    if data['open_time'].time() < currentTime < data['close_time'].time() and data['shutdown'] == False:
        return {'status': True}

    elif data['shutdown'] == True:
        return {'status': False, 'type': 'shutdown', 'data': {}}

    elif currentTime < data['open_time'].time() or data['close_time'].time() < currentTime:
        shopTime = model.shop_time(open_time=datetime.fromisoformat(str(
            data['open_time'])), close_time=datetime.fromisoformat(str(data['close_time'])), shutdown=data['shutdown'])
        return {'status': False, 'type': 'closed', 'data': jsonable_encoder(shopTime)}


def get_current_meal_time():
    # perpose : get current meal time match with the current time ( breakfast, dinner, lunch )
    # return : breakfast / lunch / dinner or False : not either time from ( breakfast, dinner, lunch )

    # get current time
    timeZoon = pytz.timezone('Asia/Colombo')
    current_time = datetime.now(timeZoon).time()
    # get shop data
    shop = db.get_shopdetails_row()
    if shop['breakfast'].time() < current_time < shop['lunch'].time():
        return 'breakfast'
    elif shop['lunch'].time() < current_time < shop['dinner'].time():
        return 'lunch'
    elif shop['dinner'].time() < current_time < shop['close_time'].time():
        return 'dinner'
    else:
        return False

from . import database
from . import model
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import pytz

db = database.get_database()

def doesShopOpen():
    data = db.get_shop_details('66ff86b140ba8d2eaa1eb88a')
    timeZoon = pytz.timezone('Asia/Colombo')
    currentTime = datetime.now(timeZoon).time()
    if data['open_time'].time() < currentTime < data['close_time'].time() and data['shutdown'] == False:
        return {'status' : True}
    
    elif data['shutdown'] == True:
        return {'status' : False, 'type' : 'shutdown', 'data' : {}}

    elif currentTime < data['open_time'].time() or data['close_time'].time() < currentTime:
        shopTime = model.shop_time(open_time = datetime.fromisoformat(str(data['open_time'])), close_time = datetime.fromisoformat(str(data['close_time'])), shutdown = data['shutdown'])
        return {'status' : False, 'type' : 'closed', 'data' : jsonable_encoder(shopTime)}

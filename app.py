from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from datetime import datetime, timedelta
from PIL import Image
from io import StringIO

import requests
import random
import json
import math
import time

app = Flask(__name__)


CHANNEL_ACCESS_TOKEN = "YQj3rgXGt7E3aZyHVWHnl/Q/+3JMLwlvrXCDwLhH+tniIj7T/r/5mWo6Y+z6Txsrh1u06xhueL6IqmGtXm1VHp8VtlK8DVnGJjBVE7sbfYCKAR9hfvSUrd/Dh8FEYbICwVIRRF+RtkTuYtF16CIFOgdB04t89/1O/w1cDnyilFU="

CHANNEL_SECRET = "1d169827c6fe5905f2c7b965cbfa5114"

my_database_sheet_ID = '1RaGPlEJKQeg_xnUGi1mlUt95-Gc6n-XF_czwudIP5Qk'
auth_json_path = 'auth.json'
april_ID='Udf8f28a8b752786fa7a6be7d8c808ec6'

count = 0
my_headers = {'CK': 'PKJ2FK5NBYFA1RCGG8'}
data_string = ''

first_flag = 0
ask_flag = 0
weight = 0
height = 0

def user_guide():
    return TemplateSendMessage(
        alt_text='【今天想要使用什麼功能呢？】',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/ewn6CmO.jpg',
                    title=' - 【現在天氣如何呢？】 - ',
                    text='出門運動前，記得看一下現在天氣和注意事項呦！',
                    actions=[
                        PostbackTemplateAction(
                            label='天氣',
                            text='天氣',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='出門注意事項',
                            text='出門注意事項'
                        ),
                        # URITemplateAction(
                        #   label='uri1',
                        #   uri='http://example.com/1'
                        # )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/Bum6bQc.jpg',
                    title=' - 【開始跑步】 - ',
                    text='讓我們開始運動吧！',
                    actions=[
                        PostbackTemplateAction(
                            label='開始跑步',
                            text='開始跑步',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='結束跑步',
                            text='結束跑步'
                        ),
                        # URITemplateAction(
                        #   label='uri1',
                        #   uri='http://example.com/1'
                        # )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/ODOwFxr.jpg',
                    title=' - 【我們關心您的健康】 - ',
                    text='幫您量身定做的健康照護',
                    actions=[
                        PostbackTemplateAction(
                            label='修改身高',
                            text='修改身高',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='修改體重',
                            text='修改體重'
                        ),
                        # URITemplateAction(
                        #   label='uri1',
                        #   uri='http://example.com/1'
                        # )
                    ]
                )
            ]
        )
    )

# Channel Access Token
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(CHANNEL_SECRET)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

longitude = 0
latitude = 0
record_flag = 0
_starttime = 0

# 處理訊息
@handler.add(MessageEvent)
def handle_message(event):
    global ask_flag,height,weight,first_flag,longitude,latitude,record_flag,_starttime
    print(event)
    if event.message.type == "location":
        if record_flag == 1:
            longitude = event.message.longitude
            latitude = event.message.latitude
            _starttime = time.time()
            # result = "以下是您的目前座標：\n經度： "+str(event.message.longitude)+"\n緯度： "+str(event.message.latitude)
            result = "已開始記錄！祝您跑步愉快！"
            output_message = TemplateSendMessage(
                    alt_text=result ,
                    template=ConfirmTemplate(
                        text=result ,
                        actions=[
                            PostbackTemplateAction(
                                label='結束跑步',
                                text='結束跑步',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='其他功能',
                                text='其他功能'
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, output_message)  
        elif record_flag == 2:
            _longitude = (event.message.longitude*96 - longitude*96)**2
            _latitude = (event.message.latitude*111 - latitude*111)**2
            record_flag = 0
            _time = time.time() - _starttime
            # result = "以下是您的目前座標：\n經度： "+str(event.message.longitude)+"\n緯度： "+str(event.message.latitude)
            result = "好的！辛苦您了！\n以下是您的跑步結果：\n"
            Distance = math.sqrt(_latitude +_longitude)
            result += ("跑步距離： {0:.3f} m\n跑步時間： {1:.1f} 分鐘\n消耗卡路里： {2:.3f} kcal ").format(Distance*1000,_time/60,weight*Distance*1.036)
            output_message = TemplateSendMessage(
                    alt_text=result ,
                    template=ConfirmTemplate(
                        text=result ,
                        actions=[
                            PostbackTemplateAction(
                                label='OK！',
                                text='OK！',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='繼續',
                                text='繼續'
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, output_message) 

    elif event.message.type == "sticker":
        output_message = StickerSendMessage(package_id='2',sticker_id=str(random.randint(140,180)))
        line_bot_api.reply_message(event.reply_token, output_message) 
    else:
        user_message = event.message.text 
        if((user_message in ["開始","start"]) and (first_flag == 0)):
            result = "第一次使用請輸入您的身高(cm)："
            first_flag = 1
            output_message = TextSendMessage(text= result)  
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(user_message == "重新修改"):
            result = "請輸入您的身高(cm)："
            first_flag = 1
            output_message = TextSendMessage(text= result)  
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(first_flag == 1): 
            try:
                height = int(user_message)
                first_flag = 2
                output_message = TextSendMessage(text="請輸入您的體重(kg)：")  
                line_bot_api.reply_message(event.reply_token, output_message) 
            except:
                output_message = TextSendMessage(text="請再輸入一次身高(不用輸入cm)：")  
                line_bot_api.reply_message(event.reply_token, output_message)
        elif(first_flag == 2):
            try:
                weight = int(user_message)
                first_flag = 3
                result = "這是您的個人資訊對嗎～？\n身高： "+str(height)+" cm\n體重： "+str(weight)+" kg\n"
                output_message = TemplateSendMessage(
                    alt_text=result ,
                    template=ConfirmTemplate(
                        text=result ,
                        actions=[
                            PostbackTemplateAction(
                                label='重新修改',
                                text='重新修改',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='正確無誤',
                                text='正確無誤'
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, output_message) 
            except:
                output_message = TextSendMessage(text="請再輸入一次體重(不用輸入kg)：")  
                line_bot_api.reply_message(event.reply_token, output_message) 

        elif(user_message in ["開始","start","回主功能","正確，開始","正確無誤","繼續","OK！","其他功能","START"]):
            output_message = user_guide()  
            line_bot_api.reply_message(event.reply_token, output_message)    
        # elif(user_message == "身高體重"):
        #     result = "以下是您的個人資訊：\n身高： "+str(height)+" cm\n體重： "+str(weight)+" kg"
        #     output_message = TextSendMessage(text= result)  
        #     line_bot_api.reply_message(event.reply_token, output_message) 
        elif(user_message == "修改身高"):
            ask_flag = 1
            output_message = TextSendMessage(text="請輸入身高(cm)：")  
            line_bot_api.reply_message(event.reply_token, output_message)  
        elif(ask_flag == 1):
            try:
                height = int(user_message)
                ask_flag = 0
                result = "以下是您的個人資訊：\n身高： "+str(height)+" cm\n體重： "+str(weight)+" kg\n"
                output_message = TemplateSendMessage(
                    alt_text=result ,
                    template=ConfirmTemplate(
                        text=result ,
                        actions=[
                            PostbackTemplateAction(
                                label='正確，開始',
                                text='正確，開始',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='重新修改',
                                text='重新修改'
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, output_message) 
            except:
                output_message = TextSendMessage(text="請再輸入一次身高(不用輸入cm)：")  
                line_bot_api.reply_message(event.reply_token, output_message)
        elif(user_message == "修改體重"):
            ask_flag = 2
            output_message = TextSendMessage(text="請輸入體重(kg)：")  
            line_bot_api.reply_message(event.reply_token, output_message)  
        elif(ask_flag == 2):
            try:
                weight = int(user_message)
                ask_flag = 0
                result = "以下是您的個人資訊：\n身高： "+str(height)+" cm\n體重： "+str(weight)+" kg\n"
                output_message = TemplateSendMessage(
                    alt_text=result ,
                    template=ConfirmTemplate(
                        text=result ,
                        actions=[
                            PostbackTemplateAction(
                                label='正確，開始',
                                text='正確，開始',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='重新修改',
                                text='重新修改'
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(event.reply_token, output_message)  
            except:
                output_message = TextSendMessage(text="請再輸入一次體重(不用輸入kg)：")  
                line_bot_api.reply_message(event.reply_token, output_message)  
        elif(user_message == "開始跑步"):
            # output_message = TextSendMessage(text="已開始記錄！祝您跑步愉快！")  
            output_message = TextSendMessage(text='請依照以下提示上傳位置訊息：')
            # line_bot_api.reply_message(event.reply_token, output_message)
            img1 = ImageSendMessage(
                original_content_url= "https://i.imgur.com/Ag544Qp.png",
                preview_image_url= "https://i.imgur.com/Ag544Qp.png"
            )
            img2 = ImageSendMessage(
                original_content_url= "https://i.imgur.com/BCfdKid.png",
                preview_image_url= "https://i.imgur.com/BCfdKid.png"
            )
            img3 = ImageSendMessage(
                original_content_url= "https://i.imgur.com/QNqwq5e.png",
                preview_image_url= "https://i.imgur.com/QNqwq5e.png"
            )
            record_flag = 1
            
            line_bot_api.push_message('Cd562f7db39d503c99578e8b323cb0582', output_message)
            line_bot_api.push_message('Cd562f7db39d503c99578e8b323cb0582', img1)
            line_bot_api.push_message('Cd562f7db39d503c99578e8b323cb0582', img2)
            # line_bot_api.push_message('Cd562f7db39d503c99578e8b323cb0582', img3)
            line_bot_api.reply_message(event.reply_token, img3)
        elif(user_message == "在線跑步人數"):
            output_message = TextSendMessage(text="目前有 21 個人正在跑步哦！")  
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(user_message == "結束跑步" and record_flag == 1):    
            record_flag = 2
            output_message = TextSendMessage(text='請依照以下提示上傳位置訊息：')
            # line_bot_api.reply_message(event.reply_token, output_message)
            img1 = ImageSendMessage(
                original_content_url= "https://i.imgur.com/Ag544Qp.png",
                preview_image_url= "https://i.imgur.com/Ag544Qp.png"
            )
            img2 = ImageSendMessage(
                original_content_url= "https://i.imgur.com/BCfdKid.png",
                preview_image_url= "https://i.imgur.com/BCfdKid.png"
            )
            img3 = ImageSendMessage(
                original_content_url= "https://i.imgur.com/QNqwq5e.png",
                preview_image_url= "https://i.imgur.com/QNqwq5e.png"
            )
            line_bot_api.push_message('Cd562f7db39d503c99578e8b323cb0582', output_message)
            line_bot_api.push_message('Cd562f7db39d503c99578e8b323cb0582', img1)
            line_bot_api.push_message('Cd562f7db39d503c99578e8b323cb0582', img2)
            # line_bot_api.push_message('Cd562f7db39d503c99578e8b323cb0582', img3)
            line_bot_api.reply_message(event.reply_token, img3)
            # line_bot_api.reply_message(event.reply_token, img3)
            # output_message = TextSendMessage(text="好的！辛苦您了！\n以下是您的跑步結果：")  
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(user_message == "天氣"):
            result = "以下是現在天氣供您參考：\n溫度: 17.9\n濕度: 59.5\n紫外: 0\nPM2.5: 8.0\n時間: 2018-10-27 22:53:20\n"
            # result = '以下是現在天氣給你參考：\n'
            # r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI6/rawdata', headers = my_headers)
            # if r.status_code == requests.codes.ok:
            #     temp = json.loads(r.text)
            #     result += str('溫度： '+ temp['value'][0]+ '\n')
            # r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI7/rawdata', headers = my_headers)
            # if r.status_code == requests.codes.ok:
            #     temp = json.loads(r.text)
            #     result += str('濕度：  '+ temp['value'][0]+ '\n')

            # r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI11/rawdata', headers = my_headers)
            # if r.status_code == requests.codes.ok:
            #     temp = json.loads(r.text)
            #     result += str('紫外： '+ temp['value'][0]+ '\n')

            # r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI13/rawdata', headers = my_headers)
            # if r.status_code == requests.codes.ok:
            #     temp = json.loads(r.text)
            #     # result += str('PM2.5： '+ temp['value'][0]+ '\n'+ '時間： '+ str(temp['time']) + '\n') 
            #     result += str('PM2.5： '+ temp['value'][0]+ '\n'+ '時間： '+ str(datetime.strptime(temp['time'],'%Y-%m-%dT%H:%M:%SZ'))+ '\n') 

            result += "---------------------------\n若氣溫超過 35℃ 不適合進行跑步鍛鍊，若紫外 UV 3~7 時須要保護措施！超過 7 時必須要保護措施！上午10點至下午2點最好不要外出！"

            output_message = TemplateSendMessage(
                    alt_text=result ,
                    template=ConfirmTemplate(
                        text=result ,
                        actions=[
                            PostbackTemplateAction(
                                label='回主功能',
                                text='回主功能',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='注意事項',
                                text='注意事項'
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, output_message) 
            output_message = user_guide()  
        elif(user_message in ["出門注意事項","注意事項"]):
            if(random.randint(0,10)%2 == 0):
                result = "今天相較昨天冷一些，出門可以帶個口罩跟外套呦！"
            else:
                result = "微涼很適合跑步的天氣，可以帶件輕薄外套安心外出，注意補充水分呦！"
            output_message = TemplateSendMessage(
                    alt_text=result ,
                    template=ConfirmTemplate(
                        text=result ,
                        actions=[
                            PostbackTemplateAction(
                                label='回主功能',
                                text='回主功能',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='開始跑步',
                                text='開始跑步'
                            )
                        ]
                    )
                )
            line_bot_api.reply_message(event.reply_token, output_message)  

        else:  
            output_message = TemplateSendMessage(
                alt_text='嗨！歡迎來到Sportlite，按下「開始」就可以開始體驗囉！',
                template=ConfirmTemplate(
                    text='嗨！歡迎來到Sportlite，按下「開始」就可以開始體驗囉！',
                    actions=[
                        PostbackTemplateAction(
                            label='START',
                            text='START',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='開始',
                            text='開始'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, output_message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests
import random
from PIL import Image
from io import StringIO
import json
from datetime import datetime, timedelta

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
                    thumbnail_image_url='https://i.imgur.com/ewn6CmO.jpg',
                    title=' - 【今天天氣如何呢？】 - ',
                    text='幫你看看今天天氣怎麼樣～',
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
                    thumbnail_image_url='https://i.imgur.com/ewn6CmO.jpg',
                    title=' - 【我們關心您的健康】 - ',
                    text='幫您量身定做的健康照護',
                    actions=[
                        PostbackTemplateAction(
                            label='身高體重',
                            text='身高體重',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='查詢身高體重',
                            text='查詢身高體重'
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

# 處理訊息
@handler.add(MessageEvent)
def handle_message(event):
    global ask_flag,height,weight,first_flag
    print(event)
    if event.message.type == "location":
        result = "以下是您的目前座標：\n經度： "+str(event.message.longitude)+"\n緯度： "+str(event.message.latitude)
        output_message = TextSendMessage(text= result)  
        line_bot_api.reply_message(event.reply_token, output_message) 
    elif event.message.type == "sticker":
        output_message = StickerSendMessage(package_id='2',sticker_id=str(random.randint(140,180)))
        line_bot_api.reply_message(event.reply_token, output_message) 
    else:
        user_message = event.message.text 
        if((user_message in ["開始","start"] & first_flag == 0) or (user_message == "重新修改")):
            result = "第一次使用請輸入您的身高(cm)："
            first_flag = 1
            output_message = TextSendMessage(text= result)  
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(first_flag == 1): 
            try:
                height = int(user_message)
                first_flag = 2
                output_message = TextSendMessage(text="第一次使用請輸入您的體重(kg)：")  
                line_bot_api.reply_message(event.reply_token, output_message) 
            except:
                output_message = TextSendMessage(text="請再輸入一次身高(不用輸入cm)：")  
                line_bot_api.reply_message(event.reply_token, output_message)
        elif(first_flag == 2):
            try:
                weight = int(user_message)
                first_flag = 3
                result = "以下是您的個人資訊：\n身高： "+str(height)+" cm\n體重： "+str(weight)+" kg\n"
                output_message = TemplateSendMessage(
                    alt_text=result ,
                    template=ConfirmTemplate(
                        text=result ,
                        actions=[
                            PostbackTemplateAction(
                                label='正確，開始使用',
                                text='開始',
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

                output_message = TextSendMessage(text= result)  
                line_bot_api.reply_message(event.reply_token, output_message)   
            except:
                output_message = TextSendMessage(text="請再輸入一次體重(不用輸入kg)：")  
                line_bot_api.reply_message(event.reply_token, output_message) 

        elif(user_message in ["開始","start"]):
            output_message = user_guide()  
            line_bot_api.reply_message(event.reply_token, output_message)    
        elif(user_message == "查詢身高體重"):
            result = "以下是您的個人資訊：\n身高： "+str(height)+" cm\n體重： "+str(weight)+" kg"
            output_message = TextSendMessage(text= result)  
            line_bot_api.reply_message(event.reply_token, output_message) 
        elif(user_message == "身高體重"):
            ask_flag = 1
            output_message = TextSendMessage(text="請輸入身高(cm)：")  
            line_bot_api.reply_message(event.reply_token, output_message)  
        elif(ask_flag == 1):
            try:
                height = int(user_message)
                ask_flag = 2
                output_message = TextSendMessage(text="請輸入體重(kg)：")  
                line_bot_api.reply_message(event.reply_token, output_message) 
            except:
                output_message = TextSendMessage(text="請再輸入一次身高(不用輸入cm)：")  
                line_bot_api.reply_message(event.reply_token, output_message)
        elif(ask_flag == 2):
            try:
                weight = int(user_message)
                ask_flag = 0
                result = "以下是您的個人資訊：\n身高： "+str(height)+" cm\n體重： "+str(weight)+" kg"
                output_message = TextSendMessage(text= result)  
                line_bot_api.reply_message(event.reply_token, output_message) 
            except:
                output_message = TextSendMessage(text="請再輸入一次體重(不用輸入kg)：")  
                line_bot_api.reply_message(event.reply_token, output_message)  
        elif(user_message == "開始跑步"):
            output_message = TextSendMessage(text="已開始記錄！祝您跑步愉快！")  
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(user_message == "在線跑步人數"):
            output_message = TextSendMessage(text="目前有 21 個人正在跑步哦！")  
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(user_message == "結束跑步"):    
            output_message = TextSendMessage(text="好的！辛苦您了！\n以下是您的跑步結果：")  
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(user_message == "天氣"):
            result = '以下是今天天氣供您參考：\n'
            r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI6/rawdata', headers = my_headers)
            if r.status_code == requests.codes.ok:
                temp = json.loads(r.text)
                result += str('溫度: '+ temp['value'][0]+ '\n')
            r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI7/rawdata', headers = my_headers)
            if r.status_code == requests.codes.ok:
                temp = json.loads(r.text)
                result += str('濕度: '+ temp['value'][0]+ '\n')

            r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI11/rawdata', headers = my_headers)
            if r.status_code == requests.codes.ok:
                temp = json.loads(r.text)
                result += str('紫外: '+ temp['value'][0]+ '\n')

            r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI13/rawdata', headers = my_headers)
            if r.status_code == requests.codes.ok:
                temp = json.loads(r.text)
                result += str('PM2.5: '+ temp['value'][0]+ '\n'+ '時間: '+ temp['time']) 

            output_message = TextSendMessage(text=result) 
            line_bot_api.reply_message(event.reply_token, output_message)
        elif(user_message == "出門注意事項"):
            output_message = TextSendMessage(text="今天出門的話需要注意：")  
            line_bot_api.reply_message(event.reply_token, output_message)  

        else:  
            output_message = TemplateSendMessage(
                alt_text='請輸入「開始」就可以開始體驗各種功能囉！',
                template=ConfirmTemplate(
                    text='請輸入「開始」就可以開始體驗各種功能囉！',
                    actions=[
                        PostbackTemplateAction(
                            label='start',
                            text='start',
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

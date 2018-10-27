from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests
from PIL import Image
from io import StringIO
import json
from datetime import datetime, timedelta

app = Flask(__name__)


CHANNEL_ACCESS_TOKEN = "YQj3rgXGt7E3aZyHVWHnl/Q/+3JMLwlvrXCDwLhH+tniIj7T/r/5mWo6Y+z6Txsrh1u06xhueL6IqmGtXm1VHp8VtlK8DVnGJjBVE7sbfYCKAR9hfvSUrd/Dh8FEYbICwVIRRF+RtkTuYtF16CIFOgdB04t89/1O/w1cDnyilFU="

CHANNEL_SECRET = "1d169827c6fe5905f2c7b965cbfa5114"

count = 0
my_headers = {'CK': 'PKJ2FK5NBYFA1RCGG8'}
data_string = ''



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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    user_message = event.message.text 
    if(user_message in ["開始","start"]):
        output_message = user_guide()
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
            result += str('溫度: '+ temp['value'][0])
        r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI7/rawdata', headers = my_headers)
        if r.status_code == requests.codes.ok:
            temp = json.loads(r.text)
            result += str('濕度: '+ temp['value'][0])

        r = requests.get('https://iot.cht.com.tw/iot/v1/device/4841588924/sensor/AI11/rawdata', headers = my_headers)
        if r.status_code == requests.codes.ok:
            temp = json.loads(r.text)
            result += str('紫外: '+ temp['value'][0])

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

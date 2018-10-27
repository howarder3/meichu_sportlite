from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)


CHANNEL_ACCESS_TOKEN = "YQj3rgXGt7E3aZyHVWHnl/Q/+3JMLwlvrXCDwLhH+tniIj7T/r/5mWo6Y+z6Txsrh1u06xhueL6IqmGtXm1VHp8VtlK8DVnGJjBVE7sbfYCKAR9hfvSUrd/Dh8FEYbICwVIRRF+RtkTuYtF16CIFOgdB04t89/1O/w1cDnyilFU="

CHANNEL_SECRET = "1d169827c6fe5905f2c7b965cbfa5114"


def user_guide():
    return TemplateSendMessage(
        alt_text='【使用說明書 ver 2.0】',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/yId0uJj.png',
                    title=' - 【使用說明書】 - ',
                    text='!使用說明書、!help、!說明書、!helptxt',
                    actions=[
                        PostbackTemplateAction(
                            label='使用說明書',
                            text='!help',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='純文字版',
                            text='!helptxt'
                        ),
                        # URITemplateAction(
                        #   label='uri1',
                        #   uri='http://example.com/1'
                        # )
                    ]
                ),

                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/9Ysg99M.jpg',
                    title=' - 【算命抽籤類】 - ',
                    text='!機率、!抽數字',
                    actions=[
                        PostbackTemplateAction(
                            label='機率',
                            text='!機率 ?',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='抽數字',
                            text='!抽數字 ?'
                        ),
                        # URITemplateAction(
                        #   label='uri1',
                        #   uri='http://example.com/1'
                        # )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/TrvwOo0.jpg',
                    title=' - 【遊戲抽抽類】 - ',
                    text='對決模式/21點/幾A幾B/終極密碼/定時炸彈/撲克比大小/機會命運',
                    actions=[
                        PostbackTemplateAction(
                            label='小遊戲',
                            text='小遊戲',
                            data='action=buy&itemid=1'
                        ),
                        MessageTemplateAction(
                            label='小遊戲',
                            text='小遊戲'
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
    user_message = event.message.text
    if(user_message == "開始"):
        output_message = user_guide()
        line_bot_api.reply_message(event.reply_token, output_message)
    else:  
        output_message = TextSendMessage(text=message)  
        line_bot_api.reply_message(event.reply_token, output_message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

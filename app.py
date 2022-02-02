# 載入LineBot所需要的模組
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(
    'lO2c3MJE9FHrMoxGlMUx/vKh5YrdhLT3RMQpRywglw+C7s0ugns92fQRQuEVURjtLo7UVVdBLxVy99xQk4W0GTwSAFXaqwjYXPPcY0fol6E9Wj6iplK0Mk6d9SsS4PWba58DMgAxrFNMBkMkAl27uAdB04t89/1O/w1cDnyilFU=')

# 必須放上自己的Channel Secret
handler = WebhookHandler('10f8e3963fb81c92797b7f2cebc22312')

#line_bot_api.push_message('U54cdd2802a60c0261bf72b4fa3fc96e6', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request (Heroku跟LINE Bot做串接)


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


# 訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text  # 使用者傳的話

    if user_text == '患者名稱':
        message = TextSendMessage(
            text='請選擇患者(或是直接輸入名字也可以)',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="01. 大笨蛋", text="大笨蛋")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="02. 小笨蛋", text="小笨蛋")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="03. 中笨蛋", text="中笨蛋")
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    #message = TextSendMessage(text=user_text)
    #line_bot_api.reply_message(event.reply_token, message)


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

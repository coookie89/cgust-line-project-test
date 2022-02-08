# 載入LineBot所需要的模組
import os
import json

import requests  # rich menu


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_channel_access_token = 'lO2c3MJE9FHrMoxGlMUx/vKh5YrdhLT3RMQpRywglw+C7s0ugns92fQRQuEVURjtLo7UVVdBLxVy99xQk4W0GTwSAFXaqwjYXPPcY0fol6E9Wj6iplK0Mk6d9SsS4PWba58DMgAxrFNMBkMkAl27uAdB04t89/1O/w1cDnyilFU='

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(line_channel_access_token)

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
    user_text = user_text.split("@")

    user_id = event.source.user_id  # 使用者line user id

    if user_text[0] == '患者名稱' or user_text[0] == '新增患者' or user_text[0] == '姓名':
        if user_text[0] == '患者名稱':
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

        elif user_text[0] == '新增患者':
            message = TextSendMessage(text='請輸入患者資訊(例如 楊千嬅 女 89/05/19)')
            line_bot_api.reply_message(event.reply_token, message)

        elif user_text[0] == '姓名':
            user_name=user_text[1] #把個管師存進資料庫
            
            message = TextSendMessage(text="哈囉！"+user_name+"("+user_id+")"+"。\\n"+"你可以開始使用其他功能了。")
            line_bot_api.reply_message(event.reply_token, message)


def write_json(line_user_id, info_type, data_dict):
    file_path = "./patient_info/"+line_user_id
    if_mkdir(file_path)

    file_path = "./patient_info/"+line_user_id+"/"+info_type
    with open(file_path, encoding="UTF8", newline="") as jsonfile:  # 讀json檔
        file_data = json.load(jsonfile)

    with open(file_path, "w", encoding="UTF8", newline="") as jsonfile:  # 寫json檔
        file_data.append(data_dict)
        json.dump(file_data, jsonfile, indent=2, ensure_ascii=False)


def if_mkdir(dir_path):  # 如果檔案不存在,就建立一個
    if os.path.isdir(dir_path) != 1:
        os.makedirs(dir_path)


# 主程式
if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))  # 偵測heroku給的port是多少
    app.run(host='0.0.0.0', port=port)

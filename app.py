import os
import json
import datetime
import subprocess #執行php

import requests  # rich menu

import mysql.connector
from mysql.connector import Error

# 載入LineBot所需要的模組
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_channel_access_token = os.getenv("line_channel_access_token")
line_channel_secret = os.getenv("line_channel_secret")
mysql_host = os.getenv("mysql_host")
mysql_port = os.getenv("mysql_port")
mysql_db = os.getenv("mysql_db")
mysql_user = os.getenv("mysql_user")
mysql_pwd = os.getenv("mysql_pwd")

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    user_text = event.message.text  # 使用者傳的話
    user_text = user_text.split("@")

    user_id = event.source.user_id  # 使用者line user id

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

        try:    
            proc = subprocess.Popen("php ./database/read.php", shell=True, stdout=subprocess.PIPE)
            script_response = proc.stdout.read()

            message = TextSendMessage(text="哈囉！"+user_name+"。"+"\n"+"你可以開始使用其他功能了。"+"\n"+script_response)

        except:
            message = TextSendMessage(text="資料上傳失敗。")

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


def get_current_time():
    current_time=str(datetime.datetime.now()).split('.')[0]
    return current_time


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # 偵測heroku給的port是多少
    app.run(host='0.0.0.0', port=port)

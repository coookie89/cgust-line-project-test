import os
import json
import datetime

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
    global CURSOR
    global connection

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

            try:
                connection = mysql.connector.connect(
                    host="3.86.83.200",
                    port=3306,
                    database="cgust-line-project",
                    user="cgust",
                    password="12345678",
                )

                if connection.is_connected():
                    cursor = connection.cursor()

                    table_name = "個案管理師_基本資料"
                    col_name = ["個管師_姓名", "個管師_line-user-id", "記錄時間"]
                    val_list = ["楊千嬅", "123", get_current_time()]

                    db_insert(cursor, table_name, col_name, val_list)
                    message = TextSendMessage(text="哈囉！"+user_name+"。"+"\n"+"你可以開始使用其他功能了。")

            except Error as e:
                message = TextSendMessage(text="資料上傳失敗。\n"+"錯誤代碼: "+e)

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


# 存入資料庫
def db_insert(cursor, table_name, col_list, val_list):
    sql = "INSERT INTO `"+table_name+"` "
    sql += "("
    for col_index in range(0, len(col_list)):
        if col_index != len(col_list)-1:
            sql += "`"+col_list[col_index]+"`, "
        else:
            sql += "`"+col_list[col_index]+"`"
    sql += ") "
    sql += "VALUES "
    sql += "("
    for val_index in range(0, len(val_list)):
        if val_list[val_index] == "now()":
            sql += val_list[val_index]
        else:
            if type(val_list[val_index]) == str:
                sql += "'"+val_list[val_index]+"'"
            elif type(val_list[val_index]) == int:
                sql += str(val_list[val_index])

        if val_index != len(val_list)-1:
            sql += ", "

    sql += ") "

    cursor.execute(sql)
    connection.commit()


def get_current_time():
    current_time=str(datetime.datetime.now()).split('.')[0]
    return current_time


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # 偵測heroku給的port是多少
    app.run(host='0.0.0.0', port=port)

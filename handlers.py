from main import *
from linebot.models import *
from urllib.parse import parse_qsl
from linebot import LineBotApi

# 引入主程式的 line_bot_api（確保在 linebot.py 中已初始化）
line_bot_api = None  # 在初始化時由主程式賦值
user_message = ""

# 處理訊息
def handle_text_message(event):
    global user_message 
    user_message = str(event.message.text)
    if user_message.isdigit():  # 確認是否為數字格式的身分證號碼
        user_exists = id_exist(int(user_message))  
        if user_exists:
            # 回傳按鈕樣板
            buttons_template = TemplateSendMessage(
                alt_text="Driver License Options",                
                template=ButtonsTemplate(
                    thumbnail_image_url='https://i.imgur.com/C0lf5A3.png',
                    title="Information & Endorsement",
                    text="Selection:",
                    actions=[
                        PostbackTemplateAction(label="Car", data="action=car"),
                        PostbackTemplateAction(label="Motorcycle", data="action=motorcycle"),
                        PostbackTemplateAction(label="Endorsement", data="action=endorsement")
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, buttons_template)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="You don't have any driver license.")
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Invalid input. Please enter a valid ID number.")
        )

# 處理 Postback 事件
def handle_postback_event(event):
    backdata = dict(parse_qsl(event.postback.data))  # 解析 Postback 資料
    if backdata.get('action') == 'car':
        send_back_car(event, backdata)
    elif backdata.get('action') == 'motorcycle':
        send_back_motorcycle(event, backdata)
    elif backdata.get('action') == 'endorsement':
        send_back_endorsement(event, backdata)

# 模擬回應 Postback 的函數（可自行擴展）
def send_back_car(event, backdata):
    user_records = get_user_by_id(list_users(), int(user_message))
    car_records = [record for record in user_records if record.get('license_type') == 'Car']
    if(car_records):
        info = get_user_details_client_side(int(user_message))
    else:
        info = "You don't have the car license"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=info))

def send_back_motorcycle(event, backdata):
    user_records = get_user_by_id(list_users(), int(user_message))
    motorcycle_records = [record for record in user_records if record.get('license_type') == 'Motorcycle']
    if(motorcycle_records):
        info = get_user_details_client_side(int(user_message))
    else:
        info = "You don't have the motorcycle license"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=info))

def send_back_endorsement(event, backdata):
    violation = get_violation_by_id(list_violations(), int(user_message))
    if(violation):
        res = get_violation_details_client_side(int(user_message))
        info = ''.join(res)
    else:
        info = "You don't have any endorsements.\nKeep it up"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=info))
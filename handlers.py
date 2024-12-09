from method import *
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
        user_exists = id_exist(user_message)  
        if user_exists: # 確認user存在與否
            messages = []
            notify = notify_license_expiry(user_message)
            if notify: # 提醒(駕照是否快到期)
                messages.append(TextSendMessage(text=notify))

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
            messages.append(buttons_template)
            line_bot_api.reply_message(event.reply_token, messages)
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
    car_record = get_car_details_client_(user_message)
    if(car_record):
        info = car_record
    else:
        info = "You don't have the car license"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=info))

def send_back_motorcycle(event, backdata):
    motorcycle_record = get_moto_details_client_(user_message)
    if(motorcycle_record):
        info = motorcycle_record
    else:
        info = "You don't have the motorcycle license"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=info))

def send_back_endorsement(event, backdata):
    violation = get_violation_details_client_side(user_message)
    if(violation):
        info = violation
    else:
        info = "You don't have any endorsements.\nKeep it up"
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=info))
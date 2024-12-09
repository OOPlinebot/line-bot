import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import handlers

app = Flask(__name__)
 
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

handlers.line_bot_api = line_bot_api

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
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    handlers.handle_text_message(event)

# 處理Postback
@line_handler.add(PostbackEvent)
def handle_message(event):
    handlers.handle_postback_event(event)
          

if __name__ == "__main__":
    app.run()
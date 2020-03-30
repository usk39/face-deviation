from flask import Flask, request, abort
import os

import face_detect as f
import base64

from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   MessageEvent, TextMessage, TextSendMessage, ImageMessage
)

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["s9AE+LBqzO9r1IUgX0ddKNkYglQ9xIz9XS3XFoHDd/DnPrDQTi2wt0wKB5yY9YmWxkhgVECpgPVLngUc25oEyjH37Zh/lqxmbsL6FzM6w4VG+LfNSbnNu9iASOUsM1gRN6TDYxleNN0cn1NrPdsxGQdB04t89/1O/w1cDnyilFU="]
LINE_CHANNEL_SECRET = os.environ["315660cf2ecbe83901a2cb137a82286c"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
       print("Invalid signature. Please check your channel access token/channel secret.")
       abort(400)

   return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    push_img_id = event.message.id
    message_content = line_bot_api.get_message_content(push_img_id)
    push_img = b""
    for chunk in message_content.iter_content():
        push_img += chunk
    push_img = base64.b64encode(push_img)
    msg = f.face_detect(push_img)
    line_bot_apireplay_message(event.replay_token, TextMessage(text=msg))

if __name__ == "__main__":
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)

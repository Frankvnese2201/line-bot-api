from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjcyNzk3ZDU3LWIxMmMtNDJkNC04NDc2LWI0YjEzNDRlYzRmMSJ9.eyJpc3MiOiIxNjU2ODc0OTgyIiwic3ViIjoiMTY1Njg3NDk4MiIsImF1ZCI6Imh0dHBzOi8vYXBpLmxpbmUubWUvIiwiZXhwIjoxNjQ2MjAwOTc1LCJ0b2tlbl9leHAiOjI1OTIwMDB9.OIPp6YsSoNJ3qft8C_KLu47DDMaLFYbN37dzEJW5NtGgQdQ9T92vukSrO2i1HkEPmJ2dP0FvHXdZUIjPViArDT9x_TIcxv7hXI4EPUTTCfRY3GW_8zqP9HvxO-8r6OTuoQdKcdhB4-SZbx3wR8THAd3aull8XwkKyKMSq0Ulsz2Sryub1TvEMBT2pWm_SkpqofOpoj1MHAZjmkyKw_sFmJRG4KM9nL548uFkHum8mAJmkL8jBfZ2k70LUUK43ROGEQRsH_w6EzcsuRwv_FzeKa_eyeUdh0AbufrX0HjNcfcd4rdjCkqSbtROJplasj_H0NAJOPeJwAJEFh_XiSoJaQ')
handler = WebhookHandler('44871da6d02b0fdf66ba1e6ed3182e86')


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


if __name__ == "__main__":
    app.run()
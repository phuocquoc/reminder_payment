import json
import requests
from datetime import datetime
import pytz
import os

def send_telegram(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        res = requests.get(url, params={"chat_id": chat_id, "text": message})
        res.raise_for_status()
    except requests.RequestException as e:
        print("❌ Lỗi gửi Telegram:", e)

def remind():
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    today = datetime.now(vn_tz)
    today_day = today.day

    bot_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    cards_json = os.getenv("CARDS")

    if not bot_token or not chat_id or not cards_json:
        print("❌ Thiếu biến môi trường!")
        return

    try:
        cards = json.loads(cards_json)
    except json.JSONDecodeError:
        print("❌ CARDS không phải chuỗi JSON hợp lệ!")
        return

    print(f"📅 [{today.strftime('%Y-%m-%d %H:%M')}] Kiểm tra nhắc nhở cho ngày {today_day}")

    for card in cards:
        if card["due_day"] - today_day == 1:
            msg = (
                f"🔔 Nhắc thanh toán thẻ tín dụng (còn 1 ngày)!\n"
                f"💳 Thẻ: {card['name']}\n"
                f"📅 Ngày đến hạn: {card['due_day']} tháng này\n"
                f"⏳ Vui lòng chuẩn bị thanh toán để tránh bị tính lãi!"
            )
            send_telegram(bot_token, chat_id, msg)

if __name__ == "__main__":
    remind()

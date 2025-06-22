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
    now = datetime.now(vn_tz)
    today_day = now.day
    current_hour = now.hour

    # Load ENV variables
    bot_token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    cards_json = os.getenv("CARDS")
    remind_hours_json = os.getenv("REMIND_HOURS")

    if not bot_token or not chat_id or not cards_json or not remind_hours_json:
        print("❌ Thiếu biến môi trường!")
        return

    try:
        cards = json.loads(cards_json)
        remind_hours = json.loads(remind_hours_json)
    except json.JSONDecodeError:
        print("❌ Biến môi trường không phải chuỗi JSON hợp lệ!")
        return

    if current_hour not in remind_hours:
        print(f"⏰ Bỏ qua (hiện tại là {current_hour}h, không thuộc giờ nhắc {remind_hours})")
        return

    print(f"📅 [{now.strftime('%Y-%m-%d %H:%M')}] Đang kiểm tra nhắc nhở...")

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

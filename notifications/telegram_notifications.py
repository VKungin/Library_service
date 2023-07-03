import requests

from Library_service.settings import TELEGRAM_BOT_TOKEN
from notifications.models import Notification

TOKEN = TELEGRAM_BOT_TOKEN


def send_notification(borrowing, message):
    user = borrowing.user
    notification = Notification.objects.get(user=user)
    chat_id = notification.chat_id

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

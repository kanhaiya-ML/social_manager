from whatsapp_bot import reply_new_message
import threading
from threading import Event

stop_whatsapp = Event()

def stop_whatsapp_bot():
    stop_whatsapp.set()


def whatsapp_message(headless):
    stop_whatsapp.clear()
    threading.Thread(
        target=reply_new_message,
        args=(stop_whatsapp,headless),
        daemon=True
    ).start()
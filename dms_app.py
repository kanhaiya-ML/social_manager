from send_message import check_and_reply_dms
import asyncio
import threading
from threading import Event

stop_dms = Event()

def stop_instagram_dms():
    stop_dms.set()

def send_insta_message(headless):
    stop_dms.clear()
    threading.Thread(
        target= lambda:asyncio.run(
            check_and_reply_dms(stop_dms,headless)
        ),
        daemon=True
    ).start()
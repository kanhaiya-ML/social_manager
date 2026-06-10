from send_reels import send_reels
import asyncio 
import threading
from threading import Event

stop_instagram_reels = Event()

def stop_instagram_bot():
    stop_instagram_reels.set()


def send_insta_reels(contacts,headless):
    stop_instagram_reels.clear()
    threading.Thread(
        target= lambda:asyncio.run(
            send_reels(stop_instagram_reels,contacts,headless)
        ),
        daemon=True
    ).start()
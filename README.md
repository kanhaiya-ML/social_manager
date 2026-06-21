# Social Manager
## THIS IS DEPRICATED I'll AGAIN START WORK ON THIS AFTER FINISHING MY INTERNSHIP
## Overview
This Project is a made to automate your chatings on whatsapp and instagram. this work in background and reply all your messages on both platforms and run until
You won't stop from UI.
This can also send reels to your targeted friend until you won't stop.


## Features
1. Whatsapp automation (just login one time and bot will reply all upcoming messages on behalf of you)
2. Instagram automation(reply Dm's)
3. Instagram Reels automation (send reels to your friends)


## Key Points
- I have used playwright for automation
- Groq api for reply messages
- model - "llama-3.3-70b-versatile"
- i have did many error handling and later i will upgrade this to avoid errors and crash


# Bug (IMPORTANT)
This is not completed yet 
if you want to use, you need a small change in my code to run on your system and that is in whatsapp and instagram dm (automation code - send_message.py , whatsapp_bot.py) handles in last line,
i have added a line, after sending reply just switch the chat to another guy and i just relise that i have hardcoded that guy chat, so in you whatsapp that name not chat found chat won't switch and then its won't detect new message in same chat,
i know this is a bug and i will handle this as soon as possible

from playwright.sync_api import sync_playwright
from langchain_groq import ChatGroq
from config_loader import get_api_key
import os 
from stats_manager import add_whatsapp_message
from dotenv import load_dotenv
load_dotenv()


def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=get_api_key()
    )

llm = get_llm()

def reply_new_message(stop_whatsapp,headless):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            channel="chrome",
            headless=headless,
            user_data_dir="./chrome_profile"
        )
        page = browser.new_page()

        page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
""")
        page.goto("https://web.whatsapp.com")

        last_seen_per_chat = {}  # { chat_index: last_message_text }
        while True:
        # while not stop_whatsapp.is_set():
            unread_chats = page.locator("span[data-testid='icon-unread-count']")
            while unread_chats.count() > 0:
                unread_chats.first.locator("..").click()

            
# -------- Need Review ------------
                print("before message select")
                messages = page.locator("span[data-testid='selectable-text']")
                print("after message select")

                print(messages.count())

                incoming = page.locator("[data-testid='tail-in']")
                outgoing = page.locator("[data-testid='tail-out']")

                print("incoming:", incoming.count())
                print("outgoing:", outgoing.count())
                print("END")

                # for i in range(messages.count()):
                #     print(i, messages.nth(i).text_content())
                for j in range(messages.count()):
                    msg = messages.nth(j)
                    # print(msg.text_content())

                if messages.count() == 0:
                    continue

                chat_name = page.locator("span[data-testid='conversation-info-header-chat-title']").text_content().strip()

                last_msg = messages.last.text_content().strip()

                # if last_seen_per_chat.get(chat_name) == last_msg:
                #     continue

                prev = last_seen_per_chat.get(chat_name)
                start = max(0,messages.count()-4)
                all_texts = [messages.nth(j).text_content().strip() for j in range(start,messages.count())]
                print(f"incoming message: {all_texts}")
                all_texts = [t for t in all_texts if t]

                if prev and prev in all_texts:
                    idx = all_texts.index(prev)
                    unread_texts = all_texts[idx+1:]
                else:
                    unread_texts = all_texts[-5:]

                if not unread_texts:
                    continue

                last_seen_per_chat[chat_name] = last_msg  # update tracker
                page.wait_for_timeout(2000)  # let message render
                print("last span after send:", messages.last.text_content().strip())
                print("what we stored:", last_seen_per_chat[chat_name])


            # for chat in unread_chats:
            #     chat.locator("..").click()
                page.wait_for_timeout(10000)                

                conversation = "\n".join(f"- {t}" for t in unread_texts)
                print(conversation)

                reply = llm.invoke(f"""
You are a friendly human chatting on WhatsApp.

Rules:
- Reply naturally like a real person.
- Reply in the same language as the user (English or Hinglish).
- Keep replies short and casual.
- Never say you are an AI.
- If someone asks who you are, say you are Kanhaiya.
- Do not repeat greetings again and again.
- Do not repeat previous replies unnecessarily.
- Focus mainly on the latest message.
- Use older messages only for context.

Previous messages:
{chr(10).join(f"- {msg}" for msg in unread_texts[:-1])}

Latest message:
- {unread_texts[-1]}

Reply naturally to the latest message only.
""")

                reply = reply.content
                page.locator("div[data-testid='conversation-compose-box-input']").fill(reply)
                page.locator("button[aria-label='Send']").click()
                add_whatsapp_message(chat_name,reply)
                page.locator("span[title='Reserve Bank of India']").click()
                page.wait_for_timeout(10000)


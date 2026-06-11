from playwright.async_api import async_playwright
from langchain_groq import ChatGroq
from stats_manager import update_dm_stats
import asyncio
import os
from config_loader import get_api_key,get_username,get_password,get_insta_contact,reload_config
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=get_api_key()
    )


username = get_username()
password = get_password()


async def check_and_reply_dms(stop_dms,headless):
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            headless=headless,
            channel="chrome",
            user_data_dir="./instagram_chrome_profile",
            args=[
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
        )
        page = await browser.new_page()

        await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """)
        await page.goto("https://www.instagram.com")

        await page.wait_for_timeout(3000)

        await page.wait_for_timeout(3000)
        username_box = page.locator("input[type='text']")
        if await username_box.count() > 0:
            await username_box.fill(username)
            await page.locator("input[type='password']").fill(password)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        await page.locator("a[href='/direct/inbox/']").click()

        await page.wait_for_timeout(3000)


        last_seen_message = set()
        while not stop_dms.is_set():
            unread_chats = page.locator("div:text-is('Unread')")
            count = unread_chats.count()

            if count == 0:
                await page.wait_for_timeout(5000)
                continue

            await unread_chats.first.locator('..').click()
            await page.wait_for_timeout(2000)
        
            # for chat in unread_chats:
            #     chat.locator("..").click()
                # page.wait_for_timeout(2000)

            try:
                message = await page.locator("div[dir='auto']:not(.xyk4ms5)").last.text_content(timeout=2000)
            except:
                continue

            # if message in last_seen_message:
            #     continue
            llm = get_llm()
            reply = llm.invoke(f"""You are a friendly person chatting on instagram.
                Reply naturally in the same language as the message - English or Hinglish.
                Keep reply short like a real instagram message.
                Message: {message}""")
            reply = reply.content
            last_seen_message.add(message)
            # print("Unread count:", count)
            # print("Message:", message)

            reload_config()
            contact_name = get_insta_contact()

            await page.locator("div[aria-placeholder='Message...']").fill(reply)
            await page.locator("svg[aria-label='Send']").click()
            update_dm_stats("Instagram User", reply)
            await page.wait_for_timeout(2000)            

            await page.locator(f"span[title='{contact_name}']").click()
            # if switch_chat.count() > 0:
            #     await switch_chat.click()
            #     print(switch_chat.count())
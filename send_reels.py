from playwright.async_api import async_playwright
from stats_manager import update_reels_stats
from config_loader import get_username,get_password


username = get_username()
password = get_password()

async def send_reels(stop_reels,contacts,headless):
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            headless=headless,
            channel="chrome",
            user_data_dir="./instagram_chrome_profile"
        )
        page = await browser.new_page()

        await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    """)
        await page.goto("https://www.instagram.com")
        await page.wait_for_timeout(2000)

        await page.wait_for_timeout(3000)
        username_box = page.locator("input[type='text']")
        if await username_box.count() > 0:
            await username_box.fill(username)
            await page.locator("input[type='password']").fill(password)
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)

        await page.locator("svg[aria-label='Reels']").click()
        await page.wait_for_timeout(2000)

        while not stop_reels.is_set():
            for contact in contacts:

                await page.wait_for_timeout(1000)
                share_btn = page.locator("[role='button']:has(svg[aria-label='Share'])").last
                await share_btn.click(force=True)
                await page.locator("input[placeholder='Search']").fill(contact)
                await page.wait_for_timeout(1000)
                await page.get_by_text(contact).first.click()
                await page.wait_for_timeout(1000)

            await page.locator("div[role='button']:has-text('Send')").click()
            update_reels_stats(contact)
            await page.wait_for_timeout(3000)


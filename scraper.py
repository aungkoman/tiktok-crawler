import asyncio
import json
import os
from playwright.async_api import async_playwright

async def get_tiktok_data(urls):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for url in urls:
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
                await asyncio.sleep(5)
                
                like_count = await page.inner_text('[data-e2e="like-count"]') if await page.query_selector('[data-e2e="like-count"]') else "0"
                comment_count = await page.inner_text('[data-e2e="comment-count"]') if await page.query_selector('[data-e2e="comment-count"]') else "0"
                
                results.append({
                    "url": url,
                    "like_count": like_count,
                    "comment_count": comment_count
                })
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        
        await browser.close()
    return results

async def main():
    links = [
        "https://www.tiktok.com/@ucstaungoo/photo/7585957965694373128",
        "https://www.tiktok.com/@ucstaungoo/photo/7585932236638276872",
    "https://www.tiktok.com/@ucstaungoo/photo/7585930829637946644",
    "https://www.tiktok.com/@ucstaungoo/photo/7585929608617381141",
    "https://www.tiktok.com/@ucstaungoo/photo/7585928587333733640",
    "https://www.tiktok.com/@ucstaungoo/photo/7585927021449088277",
    "https://www.tiktok.com/@ucstaungoo/photo/7585926177651510548",
    "https://www.tiktok.com/@ucstaungoo/photo/7585925981039316232",
    "https://www.tiktok.com/@ucstaungoo/photo/7585925214501113108"
        # ... တခြား links များ ...
    ]
    data = await get_tiktok_data(links)
    
    # ရလာတဲ့ data ကို tiktok_results.json ဆိုပြီး သိမ်းမယ်
    with open("tiktok_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(main())
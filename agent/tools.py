from agent.browser import BrowserManager
from langchain_core.tools import tool

browser_mgr = BrowserManager()

@tool
async def browse_page(url: str) -> str:
    """Navigate to a URL and return the page content"""
    try:
        page = await browser_mgr.start(headless=True)
        await page.goto(url, wait_until="networkidle", timeout=30000)
        content = await page.content()
        await browser_mgr.stop()
        return content[:20000]  # Limit size for LLM
    except Exception as e:
        await browser_mgr.stop()
        return f"Error browsing page: {str(e)}"
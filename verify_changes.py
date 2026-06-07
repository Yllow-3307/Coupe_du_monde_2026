import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1200, 'height': 1200})
        page = await context.new_page()

        # Load local index.html
        path = os.path.abspath("index.html")
        await page.goto(f"file://{path}")

        # Give some time for scripts to run
        await page.wait_for_timeout(1000)

        # Check if login screen is visible (mocking login if necessary or just screenshotting)
        os.makedirs("verification/screenshots", exist_ok=True)
        await page.screenshot(path="verification/screenshots/initial_load.png")

        # Mocking isAdmin = true and currentUser for verification
        await page.evaluate("""() => {
            isAdmin = true;
            currentUser = {uid: 'admin'};
            currentPote = 'Admin';
            POTES = ['Admin', 'Joueur1'];
            document.getElementById('login-screen').classList.add('hidden');
            document.getElementById('user-bar').style.display = 'flex';
            document.getElementById('user-name').textContent = 'Admin';
            showTab('groupes');
        }""")

        sections = ['groupes', 'matchs', 'bracket', 'pronos', 'stats', 'equipes', 'rdv', 'admin']
        for sec in sections:
            await page.evaluate(f"showTab('{sec}')")
            await page.wait_for_timeout(500)
            await page.screenshot(path=f"verification/screenshots/{sec}_section.png")

        # Test mobile view toggle
        await page.evaluate("toggleView()")
        await page.wait_for_timeout(500)
        await page.screenshot(path="verification/screenshots/mobile_view_toggle.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

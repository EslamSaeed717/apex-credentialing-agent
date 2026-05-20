"""GitHub Student Pack Engine - extracts free credential offers from GitHub Education."""
import httpx, structlog
from bs4 import BeautifulSoup

log = structlog.get_logger()

class GitHubPackEngine:
    URL = "https://education.github.com/pack"

    async def get_offers(self) -> list:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.get(self.URL, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        offers = []
        for card in soup.select(".partner-card, .offer-card, article"):
            title = card.select_one("h3,h4,.title")
            desc = card.select_one("p,.description")
            if title:
                offers.append({
                    "name": title.get_text(strip=True),
                    "description": desc.get_text(strip=True) if desc else ""
                })
        log.info("github_pack.offers_found", count=len(offers))
        return offers

"""ACAMS scraper - certs, pricing, scholarships."""
from .base import BaseScraper
from bs4 import BeautifulSoup
import structlog, json

log = structlog.get_logger()

class ACAMSScraper(BaseScraper):
    BASE = "https://www.acams.org"

    async def get_certifications(self) -> list:
        html = await self.get(f"{self.BASE}/en/certifications")
        soup = BeautifulSoup(html, "html.parser")
        certs = []
        for card in soup.select(".cert-card, .certification-item, article"):
            title = card.select_one("h2,h3,.title")
            price = card.select_one(".price,.cost")
            link = card.select_one("a[href]")
            if title:
                certs.append({
                    "name": title.get_text(strip=True),
                    "price": price.get_text(strip=True) if price else "N/A",
                    "url": self.BASE + link["href"] if link else ""
                })
        log.info("acams.certs_found", count=len(certs))
        return certs

    async def get_scholarships(self) -> list:
        html = await self.get(f"{self.BASE}/en/scholarships")
        soup = BeautifulSoup(html, "html.parser")
        scholarships = []
        for item in soup.select(".scholarship-item, .grant-item, article"):
            title = item.select_one("h2,h3,.title")
            if title:
                scholarships.append({"name": title.get_text(strip=True)})
        return scholarships

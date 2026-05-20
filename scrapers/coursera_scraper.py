"""Coursera scraper - finance/compliance courses with financial aid detection."""
from .base import BaseScraper
from bs4 import BeautifulSoup
import structlog

log = structlog.get_logger()

class CourseraScraper(BaseScraper):
    BASE = "https://www.coursera.org"
    SEARCH_URL = f"{BASE}/search"

    async def search_courses(self, query: str) -> list:
        html = await self.get(self.SEARCH_URL, params={"query": query, "topic": "finance"})
        soup = BeautifulSoup(html, "html.parser")
        courses = []
        for card in soup.select("[data-e2e='product-card'], .cds-ProductCard-base"):
            title = card.select_one("h3,.cds-CommonCard-title")
            price = card.select_one("[data-e2e='price'],.cds-ProductCard-price")
            link = card.select_one("a[href]")
            if title:
                courses.append({
                    "name": title.get_text(strip=True),
                    "price": price.get_text(strip=True) if price else "Free",
                    "url": self.BASE + link["href"] if link else "",
                    "financial_aid": True
                })
        log.info("coursera.courses_found", count=len(courses))
        return courses

"""Base scraper with stealth headers, retry logic, and proxy rotation."""
import httpx, structlog, asyncio, random
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = structlog.get_logger()

STEALTH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
}

class BaseScraper:
    def __init__(self, delay: float = 3.0):
        self.delay = delay

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(min=2, max=60),
           retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)))
    async def get(self, url: str, params: dict = None) -> str:
        await asyncio.sleep(self.delay + random.uniform(0, 1.5))
        async with httpx.AsyncClient(http2=True, headers=STEALTH_HEADERS, timeout=30) as c:
            r = await c.get(url, params=params)
            r.raise_for_status()
            log.info("scraper.get", url=url, status=r.status_code)
            return r.text

"""Beta Voucher Hunter - monitors beta exam programs for free vouchers."""
import httpx, structlog, asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

log = structlog.get_logger()

BETA_SOURCES = [
    "https://www.comptia.org/certifications/which-certification/beta-exams",
    "https://learn.microsoft.com/en-us/certifications/beta-exams",
    "https://training.linuxfoundation.org/beta-exam-program/"
]

class BetaVoucherHunter:
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
    async def check_source(self, url: str) -> dict:
        async with httpx.AsyncClient(timeout=20) as c:
            r = await c.get(url)
            r.raise_for_status()
            has_beta = "beta" in r.text.lower() and "voucher" in r.text.lower()
            log.info("beta_hunter.checked", url=url, has_beta=has_beta)
            return {"url": url, "has_beta": has_beta, "content_length": len(r.text)}

    async def hunt_all(self) -> list:
        tasks = [self.check_source(u) for u in BETA_SOURCES]
        return await asyncio.gather(*tasks, return_exceptions=True)

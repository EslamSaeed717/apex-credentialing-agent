"""
OSINT Director Mapper - Finds emails, LinkedIn profiles, and org charts.
Uses Hunter.io and Apify APIs.
"""
import httpx
import structlog
import json
import os
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Dict, List, Any

log = structlog.get_logger()
HUNTER_KEY = os.getenv("HUNTER_IO_API_KEY", "")
APIFY_KEY = os.getenv("APIFY_API_KEY", "")

class OSINTDirectorMapper:

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=60),
           retry=retry_if_exception_type(httpx.RequestError))
    async def find_emails_from_name(self, name: str, company_domain: str) -> List[str]:
        log.info("osint.find_emails", name=name, domain=company_domain)
        url = f"https://api.hunter.io/v2/email-finder?domain={company_domain}&full_name={name}&api_key={HUNTER_KEY}"
        async with httpx.AsyncClient(http2=True) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
            email = data.get("data", {}).get("email")
            return [email] if email else []

    async def get_linkedin_profiles(self, company_name: str, title_keywords: List[str]) -> List[Dict]:
        log.info("osint.linkedin_profiles", company=company_name, titles=title_keywords)
        # Apify LinkedIn Scraper actor integration
        actor_url = "https://api.apify.com/v2/acts/curious_coder~linkedin-profile-scraper/runs"
        payload = {"company": company_name, "titleKeywords": title_keywords}
        async with httpx.AsyncClient(http2=True) as client:
            r = await client.post(actor_url, json=payload,
                                  headers={"Authorization": f"Bearer {APIFY_KEY}"})
            r.raise_for_status()
            return r.json().get("data", {}).get("items", [])

    async def resolve_org_chart(self, company_name: str) -> Dict[str, Any]:
        log.info("osint.org_chart", company=company_name)
        profiles = await self.get_linkedin_profiles(company_name, ["Compliance", "AML", "HR", "Director"])
        return {"company": company_name, "contacts": profiles}

if __name__ == "__main__":
    import asyncio
    mapper = OSINTDirectorMapper()
    result = asyncio.run(mapper.resolve_org_chart("Yemen Kuwait Bank"))
    print(json.dumps(result, indent=2))

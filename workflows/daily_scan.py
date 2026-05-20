"""Daily credential scan workflow - runs every 6 hours."""
import asyncio, structlog, schedule, time
from agents.credential_hunter import CredentialHunter
from agents.pricing_exploit_agent import PricingExploitAgent
from credential_engines.scholarship_mapper import ScholarshipMapper

log = structlog.get_logger()

async def run_daily_scan():
    log.info("workflow.daily_scan.start")
    hunter = CredentialHunter()
    pricer = PricingExploitAgent()
    mapper = ScholarshipMapper()

    top_creds = await hunter.hunt(top_n=20)
    log.info("workflow.daily_scan.creds_found", count=len(top_creds))

    opportunities = await pricer.find_opportunities([c.title for c in top_creds])
    for opp in opportunities:
        if opp.savings_pct >= 80:
            log.warning("workflow.HIGH_VALUE_OPPORTUNITY", credential=opp.credential_id,
                        savings=opp.savings_pct, method=opp.method)

    log.info("workflow.daily_scan.complete")

def job():
    asyncio.run(run_daily_scan())

if __name__ == "__main__":
    schedule.every(6).hours.do(job)
    job()  # Run immediately on start
    while True:
        schedule.run_pending()
        time.sleep(60)

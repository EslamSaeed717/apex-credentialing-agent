"""Regional Pricing Engine - applies World Bank tier discounts."""
import yaml, structlog
from pathlib import Path

log = structlog.get_logger()
RULES_PATH = Path(__file__).parent.parent / "config" / "pricing_rules.yaml"

class RegionalPricingEngine:
    def __init__(self):
        self.rules = yaml.safe_load(RULES_PATH.read_text()) if RULES_PATH.exists() else {}

    def get_discount(self, country_code: str) -> float:
        tiers = self.rules.get("world_bank_tiers", {})
        for tier, data in tiers.items():
            if country_code in data.get("countries", []):
                return 1.0 - data.get("discount_multiplier", 0)
        return 0.0

    def apply(self, price: float, country_code: str) -> dict:
        discount = self.get_discount(country_code)
        final = price * (1 - discount)
        log.info("pricing_engine.applied", country=country_code, original=price, final=final)
        return {"original": price, "discount_pct": discount * 100, "final_price": final}

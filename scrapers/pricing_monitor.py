"""Pricing Monitor - watches credential prices and fires alerts on drops."""
import asyncio, json, structlog
from pathlib import Path
from datetime import datetime

log = structlog.get_logger()
DATA_FILE = Path(__file__).parent.parent / "data" / "price_history.json"

class PricingMonitor:
    def load_history(self) -> dict:
        if DATA_FILE.exists():
            return json.loads(DATA_FILE.read_text())
        return {}

    def save_history(self, data: dict):
        DATA_FILE.parent.mkdir(exist_ok=True)
        DATA_FILE.write_text(json.dumps(data, indent=2))

    def record_price(self, credential_id: str, price: float):
        history = self.load_history()
        if credential_id not in history:
            history[credential_id] = []
        history[credential_id].append({"price": price, "ts": datetime.utcnow().isoformat()})
        self.save_history(history)
        log.info("pricing_monitor.recorded", credential=credential_id, price=price)

    def detect_drop(self, credential_id: str, threshold_pct: float = 20.0) -> bool:
        history = self.load_history().get(credential_id, [])
        if len(history) < 2:
            return False
        prev = history[-2]["price"]
        curr = history[-1]["price"]
        drop = ((prev - curr) / prev) * 100
        if drop >= threshold_pct:
            log.warning("pricing_monitor.drop_detected", credential=credential_id, drop_pct=drop)
            return True
        return False

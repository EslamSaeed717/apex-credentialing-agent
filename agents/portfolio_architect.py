"""
Portfolio Architect - Builds the Sovereign Wall visualization and Credly export.
"""
import json
import structlog
from pathlib import Path

log = structlog.get_logger()
KB_ROOT = Path(__file__).parent.parent / "knowledge_base"

class PortfolioArchitect:
    def load_owned(self) -> list:
        p = KB_ROOT / "certifications" / "owned.json"
        return json.loads(p.read_text()) if p.exists() else []

    def load_targets(self) -> list:
        p = KB_ROOT / "certifications" / "targets.json"
        return json.loads(p.read_text()) if p.exists() else []

    def build_sovereign_wall(self) -> str:
        owned = self.load_owned()
        targets = self.load_targets()
        wall = "\n╔══════════════════════════════════════╗\n"
        wall += "║        SOVEREIGN CREDENTIAL WALL       ║\n"
        wall += "╠══════════════════════════════════════╣\n"
        wall += "║  OWNED:                                ║\n"
        for c in owned:
            wall += f"║  ✅ {c.get('name',''):<36}║\n"
        wall += "╠══════════════════════════════════════╣\n"
        wall += "║  TARGETS:                              ║\n"
        for c in targets:
            wall += f"║  🎯 {c.get('name',''):<36}║\n"
        wall += "╚══════════════════════════════════════╝\n"
        return wall

    def export_credly_format(self) -> dict:
        owned = self.load_owned()
        return {"badges": [{"name": c.get("name"), "issuer": c.get("provider"),
                            "badge_url": c.get("credly_url", "")} for c in owned]}

if __name__ == "__main__":
    arch = PortfolioArchitect()
    print(arch.build_sovereign_wall())

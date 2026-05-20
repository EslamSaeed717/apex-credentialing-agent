"""
LinkedIn Signal Agent - Generates LinkedIn posts for newly earned certifications.
"""
import json
import structlog
from pathlib import Path

log = structlog.get_logger()
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "linkedin_post_template.txt"

class LinkedInSignalAgent:
    def load_template(self) -> str:
        if TEMPLATE_PATH.exists():
            return TEMPLATE_PATH.read_text()
        return "🎉 Thrilled to announce I've earned {cert_name} from {provider}! #{hashtag}"

    def generate_post(self, cert_name: str, provider: str) -> str:
        template = self.load_template()
        hashtag = cert_name.replace(" ", "").replace("/", "")
        post = template.replace("{cert_name}", cert_name) \
                       .replace("{provider}", provider) \
                       .replace("{hashtag}", hashtag)
        log.info("linkedin.post_generated", cert=cert_name)
        return post

if __name__ == "__main__":
    agent = LinkedInSignalAgent()
    print(agent.generate_post("CAMS", "ACAMS"))

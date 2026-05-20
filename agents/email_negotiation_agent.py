"""
Email Negotiation Agent - Composes and sends personalized emails to HR directors.
"""
import os
import asyncio
import structlog
from pathlib import Path
from typing import Dict

log = structlog.get_logger()
SENDGRID_KEY = os.getenv("SENDGRID_API_KEY", "")

class EmailNegotiationAgent:
    def __init__(self):
        self.template_path = Path(__file__).parent.parent / "templates" / "email_template.html"

    def load_template(self) -> str:
        if self.template_path.exists():
            return self.template_path.read_text()
        return "<p>Dear {manager_name}, I am {candidate_name} seeking {project_name}.</p>"

    def compose_email(self, manager: Dict, candidate_name: str, project_name: str) -> str:
        template = self.load_template()
        return template.replace("{manager_name}", manager.get("name", "Sir/Madam")) \
                       .replace("{candidate_name}", candidate_name) \
                       .replace("{project_name}", project_name)

    async def send_via_sendgrid(self, to_email: str, subject: str, html_body: str) -> bool:
        import httpx
        payload = {
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": "eslam@apex-credentialing.com"},
            "subject": subject,
            "content": [{"type": "text/html", "value": html_body}]
        }
        async with httpx.AsyncClient() as client:
            r = await client.post("https://api.sendgrid.com/v3/mail/send",
                                  json=payload,
                                  headers={"Authorization": f"Bearer {SENDGRID_KEY}"})
            log.info("email.sent", to=to_email, status=r.status_code)
            return r.status_code == 202

if __name__ == "__main__":
    agent = EmailNegotiationAgent()
    body = agent.compose_email({"name": "Ahmed Al-Yamani"}, "Eslam Saeed", "AML Compliance Lead")
    print(body[:200])

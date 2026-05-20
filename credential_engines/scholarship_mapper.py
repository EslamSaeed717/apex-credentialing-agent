"""Scholarship Mapper - maps credentials to available scholarships."""
import json, structlog
from pathlib import Path
from typing import List, Dict

log = structlog.get_logger()

SCHOLARSHIP_DB = {
    "CAMS": [
        {"name": "ACAMS Scholarship Program", "url": "https://www.acams.org/en/scholarships",
         "coverage": "Full tuition", "deadline": "Rolling"},
        {"name": "ACAMS Emerging Leaders Award", "url": "https://www.acams.org/en/scholarships",
         "coverage": "Partial", "deadline": "Annual"}
    ],
    "CC_ISC2": [
        {"name": "ISC2 One Million Certified", "url": "https://www.isc2.org/candidate",
         "coverage": "Free exam + training", "deadline": "Ongoing"}
    ],
    "CGSS": [
        {"name": "ACAMS Scholarship Program", "url": "https://www.acams.org/en/scholarships",
         "coverage": "Full tuition", "deadline": "Rolling"}
    ]
}

class ScholarshipMapper:
    def find(self, credential_id: str) -> List[Dict]:
        results = SCHOLARSHIP_DB.get(credential_id, [])
        log.info("scholarship_mapper.found", credential=credential_id, count=len(results))
        return results

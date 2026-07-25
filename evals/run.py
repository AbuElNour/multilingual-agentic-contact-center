import json
import time
from pathlib import Path

from contact_center import ContactCenterAgent


DOC = {"document_type": "SYNTH", "expiry_month": "2026-10", "holder_alias": "Sample"}
CASES = [
    {"id": "en-renew-1", "text": "renew my document", "document": DOC, "status": "ready_for_confirmation", "language": "en"},
    {"id": "ar-renew-1", "text": "أريد تجديد المستند", "document": DOC, "status": "ready_for_confirmation", "language": "ar"},
    {"id": "missing-1", "text": "renew", "document": None, "status": "needs_document", "language": "en"},
    {"id": "missing-2", "text": "تجديد", "document": None, "status": "needs_document", "language": "ar"},
    {"id": "payment-1", "text": "pay fee", "document": None, "status": "approval_required", "language": "en"},
    {"id": "payment-2", "text": "دفع الرسوم", "document": None, "status": "approval_required", "language": "ar"},
    {"id": "escalate-1", "text": "complaint", "document": None, "status": "escalated", "language": "en"},
    {"id": "escalate-2", "text": "شكوى", "document": None, "status": "escalated", "language": "ar"},
    {"id": "unknown-1", "text": "weather", "document": None, "status": "escalated", "language": "en"},
    {"id": "unknown-2", "text": "الطقس", "document": None, "status": "escalated", "language": "ar"},
]
agent = ContactCenterAgent()
started = time.perf_counter()
results = []
for case in CASES:
    for trial in range(1, 4):
        result = agent.route(case["text"], case["document"])
        results.append(
            {
                "case_id": case["id"],
                "trial": trial,
                "passed": result["status"] == case["status"] and result["language"] == case["language"],
            }
        )
passed = sum(item["passed"] for item in results)
report = {
    "mode": "deterministic-offline",
    "cases": len(CASES),
    "trials": len(results),
    "passed": passed,
    "success_rate": passed / len(results),
    "p50_latency_ms": round((time.perf_counter() - started) * 1000 / len(results), 3),
    "estimated_cost_usd": 0,
    "results": results,
}
Path(__file__).with_name("results.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({key: value for key, value in report.items() if key != "results"}, indent=2))
raise SystemExit(0 if passed == len(results) else 1)


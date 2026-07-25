from __future__ import annotations

import re


ARABIC = re.compile(r"[\u0600-\u06ff]")


class ContactCenterAgent:
    def detect_language(self, text: str) -> str:
        return "ar" if ARABIC.search(text) else "en"

    def route(self, text: str, document: dict | None = None) -> dict:
        language = self.detect_language(text)
        normalized = text.lower()
        trace = [{"step": "language.detected", "language": language}]
        if any(term in normalized for term in ("complaint", "شكوى", "human", "موظف")):
            intent, status = "escalation", "escalated"
        elif any(term in normalized for term in ("renew", "تجديد")):
            intent = "renewal"
            missing = self._validate_document(document)
            status = "needs_document" if missing else "ready_for_confirmation"
        elif any(term in normalized for term in ("pay", "payment", "دفع")):
            intent, status = "payment", "approval_required"
        else:
            intent, status = "unknown", "escalated"
        trace.append({"step": "intent.routed", "intent": intent})
        trace.append({"step": "policy.applied", "status": status})
        return {
            "language": language,
            "intent": intent,
            "status": status,
            "message": self._message(language, status),
            "trace": trace,
        }

    @staticmethod
    def _validate_document(document: dict | None) -> list[str]:
        if not document:
            return ["document"]
        return [field for field in ("document_type", "expiry_month", "holder_alias") if not document.get(field)]

    @staticmethod
    def _message(language: str, status: str) -> str:
        messages = {
            ("en", "escalated"): "I will transfer this synthetic case to a human specialist.",
            ("en", "needs_document"): "Please provide the synthetic document fields.",
            ("en", "ready_for_confirmation"): "The synthetic renewal is ready for your confirmation.",
            ("en", "approval_required"): "Payment requires explicit confirmation.",
            ("ar", "escalated"): "سيتم تحويل الحالة التجريبية إلى موظف مختص.",
            ("ar", "needs_document"): "يرجى تقديم بيانات المستند التجريبي.",
            ("ar", "ready_for_confirmation"): "طلب التجديد التجريبي جاهز للتأكيد.",
            ("ar", "approval_required"): "تتطلب عملية الدفع تأكيدًا صريحًا.",
        }
        return messages[(language, status)]


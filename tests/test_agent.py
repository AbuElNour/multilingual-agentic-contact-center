import unittest

from contact_center import ContactCenterAgent


class ContactCenterTests(unittest.TestCase):
    def setUp(self):
        self.agent = ContactCenterAgent()
        self.document = {"document_type": "SYNTH", "expiry_month": "2026-10", "holder_alias": "Sample"}

    def test_detects_arabic(self):
        self.assertEqual(self.agent.route("أريد تجديد المستند", self.document)["language"], "ar")

    def test_renewal_requires_document(self):
        self.assertEqual(self.agent.route("renew my document")["status"], "needs_document")

    def test_complete_renewal_requires_confirmation(self):
        self.assertEqual(self.agent.route("renew my document", self.document)["status"], "ready_for_confirmation")

    def test_payment_requires_approval(self):
        self.assertEqual(self.agent.route("pay the fee")["status"], "approval_required")

    def test_complaints_escalate(self):
        self.assertEqual(self.agent.route("I have a complaint")["status"], "escalated")

    def test_unknown_intent_escalates(self):
        self.assertEqual(self.agent.route("unrelated request")["intent"], "unknown")


if __name__ == "__main__":
    unittest.main()


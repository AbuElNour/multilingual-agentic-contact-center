import json

from .agent import ContactCenterAgent


def main():
    agent = ContactCenterAgent()
    document = {"document_type": "SYNTH-LICENSE", "expiry_month": "2026-10", "holder_alias": "Sample-01"}
    for message in ("I need to renew my document", "أريد دفع الرسوم", "I have a complaint"):
        print(json.dumps(agent.route(message, document), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


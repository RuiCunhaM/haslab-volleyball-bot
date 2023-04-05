from payloads import MATTER_PAYLOAD
from datetime import date, timedelta
import scrapper
import rally

TOKEN = "qgt54mas5tdqzkriy176z9zxwo"
VALID_CHANNELS = [
    "sports",
    "bottest",
    "testing-channel",
]


def main(args):
    request_token = args.get("token", "TOKEN")
    request_channel = args.get("channel_name", "CHANNEL")
    request_text = args.get("text", "")

    if request_token != TOKEN or request_channel not in VALID_CHANNELS:
        return {"statusCode": 403}

    today = date.today()

    if not request_text:
        start = today + timedelta(days=-today.weekday(), weeks=1)
        title = "Rallly for next week!"
    elif request_text == "current":
        start = today + timedelta(days=1)
        title = "Rallly for this week!"
    else:
        return {
            "statusCode": 400,
            "body": "Invalid argument",
        }

    try:
        slots = scrapper.get_slots(start)
        rally_url = rally.create_poll(slots, start)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e),
        }

    MATTER_PAYLOAD["text"] = "<!channel>"
    MATTER_PAYLOAD["attachments"][0]["fallback"] = rally_url
    MATTER_PAYLOAD["attachments"][0]["text"] = rally_url
    MATTER_PAYLOAD["attachments"][0]["title"] = title
    MATTER_PAYLOAD["attachments"][0]["fields"] = [
        {
            "short": True,
            "title": "Week",
            "value": f"{start}",
        },
    ]

    return {
        "headers": {
            "content-type": "application/json",
        },
        "body": MATTER_PAYLOAD,
    }

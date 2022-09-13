from payloads import MATTER_PAYLOAD
from datetime import date, timedelta
import scrapper
import rally

TOKEN = "qgt54mas5tdqzkriy176z9zxwo"
CHANNEL = "sports"


def main(args):
    request_token = args.get("token", "TOKEN")
    request_channel = args.get("channel_name", "CHANNEL")

    if request_token != TOKEN or request_channel != CHANNEL:
        return {"statusCode": 403}

    today = date.today()
    next_monday = today + timedelta(days=-today.weekday(), weeks=1)

    try:
        slots = scrapper.get_slots(next_monday)
        rally_url = rally.create_poll(slots, next_monday)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e),
        }

    MATTER_PAYLOAD["attachments"][0]["fallback"] = rally_url
    MATTER_PAYLOAD["attachments"][0]["text"] = rally_url
    MATTER_PAYLOAD["attachments"][0]["title"] = f"Volleyball week {next_monday}"

    return {
        "headers": {
            "content-type": "application/json",
        },
        "body": MATTER_PAYLOAD,
    }

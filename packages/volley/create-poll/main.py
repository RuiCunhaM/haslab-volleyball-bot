from payloads import matter_payload
from datetime import date, timedelta

import scrapper
import rallly
import os

VALID_CHANNELS = [
    "sports",
    "bottest",
]


def create_poll(args):
    request_token = args.get("token", "TOKEN")
    request_channel = args.get("channel_name", "CHANNEL")
    request_text = args.get("text", "")

    if (
        request_token != os.environ["SECRET_TOKEN"]
        or request_channel not in VALID_CHANNELS
    ):
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
        rallly_url = rallly.create_poll(slots, start)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": str(e),
        }

    return {
        "headers": {
            "content-type": "application/json",
        },
        "body": matter_payload(start, title, rallly_url),
    }

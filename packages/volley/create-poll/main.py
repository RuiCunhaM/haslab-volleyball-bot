from payloads import matter_payload
from datetime import date, timedelta, datetime

import discord
import scrapper
import rallly
import os
import re

VALID_CHANNELS = [
    "sports",
    "bottest",
]

SECRET_TOKEN = os.environ.get("SECRET_TOKEN")


def create_poll(args):
    request_token = args.get("token", "TOKEN")
    request_channel = args.get("channel_name", "CHANNEL")
    request_text = args.get("text", "")
    start = None
    fields = []

    if request_token != SECRET_TOKEN or request_channel not in VALID_CHANNELS:
        return {"body": "Forbidden", "statusCode": 403}

    today = date.today()

    if not request_text:
        start = today + timedelta(days=-today.weekday(), weeks=1)
        title = "Rallly for next week!"
    elif request_text.split()[0] == "confirm":
        try:
            start_time = datetime.strptime(
                f"{request_text.split()[1]} {request_text.split()[2]}", "%d-%m-%Y %H:%M"
            )
        except ValueError:
            return {
                "statusCode": 400,
                "body": "Invalid datetime format. Please use DD-MM-YYYY HH:MM",
            }
        end_time = start_time + timedelta(hours=1)
        title = "Announcement"
        text = f"Volleyball game confirmed for {start_time.strftime('%Y-%m-%d %H:%M')}!"
        google_link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&dates={start_time.strftime('%Y%m%dT%H%M%SZ')}%2F{end_time.strftime('%Y%m%dT%H%M%SZ')}&details=&location=Nave%202&text=Volleyball%20Match"
        fields.append(("Google Calendar", google_link))
    elif request_text.split()[0] == "echo":
        if capture := re.search(
            r'\s*"([^"\n]*)"\s+"([^"\n]*)"', request_text.split(" ", 1)[1]
        ):
            title = capture.group(1)
            text = capture.group(2)
        else:
            return {
                "statusCode": 400,
                "body": "Invalid argument for echo",
            }
    elif request_text == "current":
        start = today + timedelta(days=1)
        title = "Rallly for this week!"
    elif week_offset := int(request_text):
        week_offset = max(0, week_offset)
        start = today + timedelta(days=-today.weekday(), weeks=week_offset)
        title = f"Rallly for week {start.isocalendar().week}! ({start.strftime('%d %b')} - {(start + timedelta(days=6.9)).strftime('%d %b')}) "
    else:
        return {
            "statusCode": 400,
            "body": "Invalid argument",
        }

    if start:
        try:
            slots = scrapper.get_slots(start)
            text = rallly.create_poll(slots, start)
        except Exception as e:
            return {
                "statusCode": 400,
                "body": str(e),
            }

    if request_channel != "bottest":
        try:
            discord.notify(title, text, start, fields)
        except Exception as e:
            print(str(e))

    return {
        "headers": {
            "content-type": "application/json",
        },
        "body": matter_payload(title, text, start, fields),
    }

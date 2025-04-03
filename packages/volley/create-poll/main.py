from datetime import date, timedelta, datetime

import mattermost
import discord
import scrapper
import rallly

import pytz
import os
import re

VALID_CHANNELS = [
    "sports",
    "bottest",
]

SECRET_TOKEN = os.environ.get("SECRET_TOKEN")


def confirm(request_text, fields):
    start_time = datetime.strptime(
        f"{request_text.split()[1]} {request_text.split()[2]}", "%d-%m-%Y %H:%M"
    )
    end_time = start_time + timedelta(hours=1)

    pt_tz = pytz.timezone("Europe/Lisbon")
    start_time = pt_tz.localize(start_time)
    end_time = pt_tz.localize(end_time)

    title = "Announcement"
    text = f"Volleyball game confirmed for {start_time.strftime('%Y-%m-%d %H:%M')}!"

    utc_start_time = start_time.astimezone(pytz.utc)
    utc_end_time = end_time.astimezone(pytz.utc)

    google_link = f"https://calendar.google.com/calendar/render?action=TEMPLATE&dates={utc_start_time.strftime('%Y%m%dT%H%M%SZ')}%2F{utc_end_time.strftime('%Y%m%dT%H%M%SZ')}&details=&location=Nave%202&text=Volleyball%20Match"

    fields.append(("", f"[📅 Add to Google Calendar]({google_link})"))

    return title, text


def echo(request_text):
    if capture := re.search(
        r'\s*"([^"\n]*)"\s+"([^"\n]*)"', request_text.split(" ", 1)[1]
    ):
        title = capture.group(1)
        text = capture.group(2)
    else:
        raise ValueError

    return title, text


def create_poll(args):
    request_token = args.get("token", "TOKEN")
    request_channel = args.get("channel_name", "CHANNEL")
    request_text = args.get("text", "")
    text = ""
    start = None
    fields = []

    if request_token != SECRET_TOKEN or request_channel not in VALID_CHANNELS:
        return {
            "body": "Forbidden",
            "statusCode": 403,
        }

    today = date.today()

    if not request_text:
        start = today + timedelta(days=-today.weekday(), weeks=1)
        title = "Rallly for next week!"
    elif request_text == "current":
        start = today + timedelta(days=1)
        title = "Rallly for this week!"
    elif request_text.isnumeric():
        week_offset = max(0, int(request_text))
        start = today + timedelta(days=-today.weekday(), weeks=week_offset)
        title = f"Rallly for week {start.isocalendar().week}! ({start.strftime('%d %b')} - {(start + timedelta(days=6.9)).strftime('%d %b')}) "
    elif request_text.split()[0] == "confirm":
        try:
            text, title = confirm(request_text, fields)
        except ValueError:
            return {
                "statusCode": 400,
                "body": "Invalid datetime format. Please use DD-MM-YYYY HH:MM",
            }
    elif request_text.split()[0] == "echo":
        try:
            text, title = echo(request_text)
        except ValueError:
            return {
                "statusCode": 400,
                "body": "Invalid argument for echo",
            }
    else:
        return {
            "statusCode": 400,
            "body": "Invalid argument",
        }

    # If we have a start date, we are creating a poll
    if start:
        try:
            slots = scrapper.get_slots(start)
            text = rallly.create_poll(slots, start)
        except Exception as e:
            return {
                "statusCode": 400,
                "body": str(e),
            }

    # We do not notify Discord when testing
    if request_channel != "bottest":
        try:
            discord.notify(title, text, start, fields)
        except Exception as e:
            print(str(e))

    return {
        "headers": {
            "content-type": "application/json",
        },
        "body": mattermost.matter_payload(title, text, start, fields),
    }

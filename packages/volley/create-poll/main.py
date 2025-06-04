from datetime import date, timedelta, datetime

import mattermost
import discord
import scraper
import rallly

import os
import re

VALID_CHANNELS = [
    "sports",
    "bottest",
]

SECRET_TOKEN = os.environ.get("SECRET_TOKEN")
CL_COLLECTION = os.environ.get("CL_COLLECTION")


def confirm(request_text, fields):
    start_date = datetime.strptime(
        f"{request_text.split()[1]} {request_text.split()[2]}", "%d-%m-%Y %H:%M"
    )

    title = "Announcement"
    text = f"Volleyball game confirmed for {start_date.strftime('%Y-%m-%d %H:%M')}!"

    calendar_link = f"https://my.calendarlink.com/link?collection={CL_COLLECTION}&title=Volleyball%20Match&start={start_date.strftime("%d %B %Y %H%%3A%M")}&duration=60 minutes&timezone=Europe%2FLisbon&location=Nave 2"

    fields.append(("", f"[📅 Add to Calendar]({calendar_link})"))

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
            title, text = confirm(request_text, fields)
        except ValueError:
            return {
                "statusCode": 400,
                "body": "Invalid datetime format. Please use DD-MM-YYYY HH:MM",
            }
    elif request_text.split()[0] == "echo":
        try:
            title, text = echo(request_text)
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
            slots = scraper.get_slots(start)
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

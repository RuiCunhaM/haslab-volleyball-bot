from common import GIT_ICON, GIT_REPO

import requests
import os

DISCORD_HOOK = os.environ.get("DISCORD_HOOK")


def notify(title, text, start_date=None, fields=[]):
    payload = {
        "embeds": [
            {
                "title": title,
                "description": text,
                "color": 16776960,
                "footer": {
                    "text": GIT_REPO,
                    "icon_url": GIT_ICON,
                },
                "fields": [],
            }
        ],
        "content": "@here",
    }

    if start_date:
        payload["embeds"][0]["fields"].append(
            {
                "name": "Week",
                "value": f"{start_date}",
                "inline": True,
            }
        )

    for title, value in fields:
        payload["embeds"][0]["fields"].append(
            {
                "name": title,
                "value": value,
            }
        )

    requests.post(DISCORD_HOOK, json=payload)

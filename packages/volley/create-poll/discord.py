import requests
import os

DISCORD_HOOK = os.environ.get("DISCORD_HOOK")


def notify(title, text, start_date=None):
    payload = {
        "embeds": [{
            "title": title,
            "description": text,
            "color": 16776960,
            "footer": {
                "text": ""
            },
            "author": {
                "name":
                "Volleyball",
                "icon_url":
                "https://i.pinimg.com/736x/84/36/cf/8436cf7032a6d1895c9834cb137107cb.jpg",
            },
        }],
        "content":
        "@here",
    }
    if start_date:
        payload["embeds"][0]["fields"] = [{
            "name": "Week",
            "value": f"{start_date}",
            "inline": True,
        }]

    requests.post(DISCORD_HOOK, json=payload)

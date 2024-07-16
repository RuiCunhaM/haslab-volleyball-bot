import requests
import os

DISCORD_HOOK = os.environ.get("DISCORD_HOOK")


def notify(start_date, title, rally_url):
    payload = {
        "embeds": [
            {
                "title": title,
                "description": rally_url,
                "color": 16776960,
                "footer": {"text": ""},
                "author": {
                    "name": "Volleyball",
                    "icon_url": "https://i.pinimg.com/736x/84/36/cf/8436cf7032a6d1895c9834cb137107cb.jpg",
                },
                "fields": [
                    {
                        "name": "Week",
                        "value": f"{start_date}",
                        "inline": True,
                    }
                ],
            }
        ],
        "content": "@here",
    }

    requests.post(DISCORD_HOOK, json=payload)

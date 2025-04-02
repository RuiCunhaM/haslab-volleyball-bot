from common import GIT_ICON, GIT_REPO, VOLLEY_ICON


def matter_payload(title, text, start_date=None, fields=[]):
    payload = {
        "username": "Volleyball",
        "text": "<!channel>",
        "icon_url": VOLLEY_ICON,
        "response_type": "in_channel",
        "attachments": [
            {
                "color": "#FFFF00",
                "footer": GIT_REPO,
                "footer_icon": GIT_ICON,
                "fallback": text,
                "text": text,
                "title": title,
                "fields": [],
            }
        ],
    }

    if start_date:
        payload["attachments"][0]["fields"].append(
            {
                "short": True,
                "title": "Week",
                "value": f"{start_date}",
            }
        )

    for title, value in fields:
        payload["attachments"][0]["fields"].append(
            {
                "title": title,
                "value": value,
            }
        )

    return payload

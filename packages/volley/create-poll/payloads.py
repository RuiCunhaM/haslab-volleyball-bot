# Payloads
MATTER_PAYLOAD = {
    "username": "Volleyball",
    "icon_url": "https://i.pinimg.com/736x/84/36/cf/8436cf7032a6d1895c9834cb137107cb.jpg",
    "response_type": "in_channel",
    "attachments": [
        {
            "color": "#FFFF00",
            # "author_name": "Volleyball",
            # "author_icon": "https://i.pinimg.com/736x/84/36/cf/8436cf7032a6d1895c9834cb137107cb.jpg",
            "footer": "ruicunham/haslab-volleyball-bot",
            "footer_icon": "https://cdn-icons-png.flaticon.com/512/25/25231.png",
        }
    ],
}

RALLLY_PAYLOAD = {
    "0": {
        "json": {
            "disableComments": False,
            "hideParticipants": False,
            "hideScores": False,
            "title": "Volleyball",
            "location": "Nave 2",
            "timeZone": "Europe/Lisbon",
            "requireParticipantEmail": None,
        },
        "meta": {"values": {"requireParticipantEmail": ["undefined"]}},
    }
}


def matter_payload(title, text, start_date=None):
    MATTER_PAYLOAD["text"] = "<!channel>"
    MATTER_PAYLOAD["attachments"][0]["fallback"] = text
    MATTER_PAYLOAD["attachments"][0]["text"] = text
    MATTER_PAYLOAD["attachments"][0]["title"] = title
    if start_date:
        MATTER_PAYLOAD["attachments"][0]["fields"] = [
            {
                "short": True,
                "title": "Week",
                "value": f"{start_date}",
            },
        ]

    return MATTER_PAYLOAD


def rallly_payload(date, slots):
    RALLLY_PAYLOAD["0"]["json"]["options"] = slots
    RALLLY_PAYLOAD["0"]["json"]["description"] = f"Volleyball week {date}"

    return RALLLY_PAYLOAD

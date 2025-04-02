import requests

RALLLY_URL_1 = "https://app.rallly.co/api/auth/csrf"
RALLLY_URL_2 = "https://app.rallly.co/api/auth/callback/guest"
RALLLY_URL_3 = "https://app.rallly.co/api/auth/session"
RALLLY_CREATE_URL = "https://app.rallly.co/api/trpc/polls.create?batch=1"


def rallly_payload(date, slots):
    payload = {
        "0": {
            "json": {
                "disableComments": False,
                "hideParticipants": False,
                "hideScores": False,
                "title": "Volleyball",
                "location": "Nave 2",
                "timeZone": "Europe/Lisbon",
                "requireParticipantEmail": None,
                "options": slots,
                "description": f"Volleyball week {date}",
            },
            "meta": {"values": {"requireParticipantEmail": ["undefined"]}},
        }
    }

    return payload


def create_poll(slots, date):
    session = requests.Session()
    token = session.get(RALLLY_URL_1).json()["csrfToken"]
    session.post(
        RALLLY_URL_2,
        data={
            "redirect": "false",
            "csrfToken": token,
            "callbackUrl": "https://app.rallly.co/new",
            "json": "true",
        },
    )
    session.get(RALLLY_URL_3)
    response = session.post(RALLLY_CREATE_URL, json=rallly_payload(date, slots))

    if not response.ok:
        raise Exception(f"Error creating Rallly poll: {response.json()}")

    urlId = response.json()[0]["result"]["data"]["json"]["id"]

    return f"https://app.rallly.co/invite/{urlId}"

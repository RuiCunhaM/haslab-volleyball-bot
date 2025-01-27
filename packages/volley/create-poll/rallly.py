from payloads import rallly_payload
import requests

RALLLY_URL_1 = "https://app.rallly.co/api/auth/csrf"
RALLLY_URL_2 = "https://app.rallly.co/api/auth/callback/guest"
RALLLY_URL_3 = "https://app.rallly.co/api/auth/session"
RALLLY_CREATE_URL = "https://app.rallly.co/api/trpc/polls.create?batch=1"


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

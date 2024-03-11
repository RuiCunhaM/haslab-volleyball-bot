from payloads import rallly_payload
import requests

RALLLY_URL = "https://app.rallly.co/new"
RALLLY_CREATE_URL = "https://app.rallly.co/api/trpc/polls.create?batch=1"


def create_poll(slots, date):
    session = requests.Session()
    session.get(RALLLY_URL)
    response = session.post(
        RALLLY_CREATE_URL, json=rallly_payload(date, slots)
    )

    if not response.ok:
        raise Exception(f"Error creating Rallly poll: {response.json()}")

    urlId = response.json()[0]["result"]["data"]["json"]["id"]

    return f"https://app.rallly.co/invite/{urlId}"

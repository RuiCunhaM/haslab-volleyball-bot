from payloads import rallly_payload
from requests import post

RALLLY_CREATE_URL = "https://app.rallly.co/api/trpc/polls.create?batch=1"


def create_poll(slots, date):
    response = post(RALLLY_CREATE_URL, json=rallly_payload(date, slots))

    if not response.ok:
        raise Exception(f"Error creating Rallly poll: {response.json()}")

    urlId = response.json()[0]["result"]["data"]["json"]["id"]

    return f"https://app.rallly.co/invite/{urlId}"

from payloads import RALLY_PAYLOAD
from requests import post

RALLY_CREATE_URL = "https://app.rallly.co/api/trpc/polls.create?batch=1"


def create_poll(slots, date):
    RALLY_PAYLOAD["0"]["json"]["options"] = slots
    RALLY_PAYLOAD["0"]["json"]["description"] = f"Volleyball week {date}"

    response = post(RALLY_CREATE_URL, json=RALLY_PAYLOAD)

    if not response.ok:
        raise Exception(response.json())

    urlId = response.json()[0]["result"]["data"]["json"]["id"]

    return f"https://app.rallly.co/invite/{urlId}"

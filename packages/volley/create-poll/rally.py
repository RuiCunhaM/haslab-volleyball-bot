from payloads import RALLY_PAYLOAD
from requests import post, get
from string import Template

RALLY_CREATE_URL = "https://rallly.co/api/trpc/polls.create?batch=1"
RALLY_GET_URL = Template(
    'https://rallly.co/api/trpc/polls.get?batch=1&input={"0":{"json":{"urlId":"$urlId","admin":true}}}'
)


def create_poll(slots, date):
    RALLY_PAYLOAD["0"]["json"]["options"] = slots
    RALLY_PAYLOAD["0"]["json"]["description"] = f"Volleyball week {date}"

    response = post(RALLY_CREATE_URL, json=RALLY_PAYLOAD)

    if not response.ok:
        raise Exception("Error creating Rally poll")

    urlId = response.json()[0]["result"]["data"]["json"]["urlId"]

    response = get(RALLY_GET_URL.substitute(urlId=urlId))

    if not response.ok:
        raise Exception("Error obtaining participantUrlId")

    participantUrlId = response.json()[0]["result"]["data"]["json"][
        "participantUrlId"
    ]

    return f"https://rallly.co/p/{participantUrlId}"

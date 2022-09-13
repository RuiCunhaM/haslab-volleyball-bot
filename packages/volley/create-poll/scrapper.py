from requests import get
from bs4 import BeautifulSoup
from string import Template
from datetime import timedelta, time

VALID_HOURS = [
    "09:00",
    "11:00",
    "17:00",
]

UM_TEMPLATE_URL = Template(
    "https://www.uminhosports.sas.uminho.pt/aluguercampos.php?dia=$date&desporto="
)


def get_slots(date):
    slots = []
    for i in range(5):
        curr_date = (date + timedelta(days=i)).isoformat()

        response = get(UM_TEMPLATE_URL.substitute(date=curr_date))

        if not response.ok:
            raise Exception("Error retrieving UM data")

        soup = BeautifulSoup(response.content, "html.parser")

        results = soup.find_all("div", class_="col-sm-7")[1]
        available = results.find_all(
            "button", class_="btn btn-primary btn-m btn_reserva"
        )

        for hour in available:
            if hour.text in VALID_HOURS:
                start_time = time.fromisoformat(hour.text)
                end_time = time(
                    start_time.hour + 1, start_time.minute, start_time.second
                )
                slots.append(f"{curr_date}T{start_time}/{curr_date}T{end_time}")

    return slots

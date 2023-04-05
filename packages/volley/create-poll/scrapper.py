from requests import get
from bs4 import BeautifulSoup
from string import Template
from datetime import timedelta, time

VALID_HOURS = [
    ("17:00", "17:30"),
]

UM_TEMPLATE_URL = Template(
    "https://www.uminhosports.sas.uminho.pt/aluguercampos.php?dia=$date&desporto="
)


def get_slots(start_date):
    slots = []
    for i in range(5 - start_date.weekday()):
        curr_date = start_date + timedelta(days=i)

        iso_date = curr_date.isoformat()
        response = get(UM_TEMPLATE_URL.substitute(date=iso_date))

        if not response.ok:
            raise Exception("Error retrieving UM data")

        soup = BeautifulSoup(response.content, "html.parser")

        results = soup.find_all("div", class_="col-sm-7")[1]
        available = results.find_all(
            "button", class_="btn btn-primary btn-m btn_reserva"
        )
        available = [x.text for x in available]
        for h1, h2 in VALID_HOURS:
            if h1 in available and h2 in available:
                start_time = time.fromisoformat(h1)
                end_time = time(
                    start_time.hour + 1, start_time.minute, start_time.second
                )
                slots.append(
                    {
                        "startDate": f"{iso_date}T{start_time}",
                        "endDate": f"{iso_date}T{end_time}",
                    }
                )

    return slots

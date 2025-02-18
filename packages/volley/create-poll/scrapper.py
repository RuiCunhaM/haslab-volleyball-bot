from requests import get
from bs4 import BeautifulSoup
from string import Template
from datetime import timedelta, time

VALID_HOURS = [
        "17:00", "18:00", "12:00"
]

UM_TEMPLATE_URL = Template("https://sasum.scl.pt/aluguercampos.php?dia=$date&desporto=")


def get_slots(start_date):
    slots = []
    for i in range(5 - start_date.weekday()):
        curr_date = start_date + timedelta(days=i)

        iso_date = curr_date.isoformat()
        response = get(UM_TEMPLATE_URL.substitute(date=iso_date))

        if not response.ok:
            raise Exception(response.json())

        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find(
            lambda tag: tag.name == "div"
            and "col-md-6 m-b-30" == " ".join(tag.get("class") or [])
            and tag.find("b", string=lambda s: s and "Nave 2" in s)
        ).find_all("button", class_="btn btn-primary btn-m btn_reserva")
        available = [x.text for x in results]
        for h in VALID_HOURS:
            if h in available:
                start_time = time.fromisoformat(h)
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

from main import create_poll


def test():
    params = {
        "token": "qgt54mas5tdqzkriy176z9zxwo",
        "channel_name": "sports",
        "text": "",
    }
    print(create_poll(params))


if __name__ == "__main__":
    test()

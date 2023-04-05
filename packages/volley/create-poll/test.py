from main import create_poll


def test():
    params = {
        "token": "***REMOVED***",
        "channel_name": "sports",
        "text": "",
    }
    print(create_poll(params))


if __name__ == "__main__":
    test()

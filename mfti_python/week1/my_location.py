import requests

def get_location():
    return requests.get("http://freegeoip.net/json/").json()


if __name__=="__main__":
    print(get_location())

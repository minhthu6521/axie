import datetime
import json
import time
import urllib

import requests

URL = "https://axieinfinity.com/graphql-server-v2/graphql"
BASE = {
    "query": "fragment AxieBrief on Axie {\n  "
             "id\n  genes\n  stats {\n    hp\n    morale\n    skill\n    speed\n  }\n  "
             "name\n  stage\n  class\n  breedCount\n  image\n  title\n  "
             "battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    "
             "currentPrice\n    currentPriceUSD\n    startingPrice\n    endingPrice\n    "
             "duration\n    timeLeft\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    "
             "specialGenes\n    __typename\n  }\n  __typename\n}\n\nquery "
             "GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, "
             "$from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(\n    "
             "auctionType: $auctionType\n    criteria: $criteria\n    from: $from\n    "
             "sort: $sort\n    size: $size\n    owner: $owner\n  ) {\n    total\n    "
             "results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n",
    "variables": {}
}

HTML_URL = "https://www.axielegend.com/"


def get_details(param):
    body = BASE
    body["variables"] = param
    res = requests.post(URL, data=json.dumps(body), headers={"Content-Type": "application/json"})
    res_json = json.loads(res.content)
    return res_json["data"]["axies"]["results"]


REAL_PRICE = lambda x: float(x["auction"]["currentPriceUSD"])


def get_all():
    params = open("params.json")
    params = json.loads(params.read())
    for param in params:
        print("-------------------------------")
        print(f"Request for {param['name']} started")
        param = param["content"]
        details = get_details(param)
        if (REAL_PRICE(details[1]) - REAL_PRICE(details[0])) >= (REAL_PRICE(details[1]) / 10):
            import winsound
            duration = 1000  # milliseconds
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            html_params = {
                "parts": ",".join(param["criteria"]["parts"]),
                "classes": ",".join([c.lower() for c in param["criteria"]["classes"]]),
                "hp": param["criteria"]["hp"][0],
                "speed": param["criteria"]["speed"][0],
            }
            html_params = urllib.parse.urlencode(html_params)
            print(HTML_URL + html_params)
            print(f"Difference:{REAL_PRICE(details[1]) - REAL_PRICE(details[0])}")
        print("Request end")
        print("-------------------------------")


def run():
    while (True):
        print("#################################################")
        print(f"Request sent at: {datetime.datetime.now()}")
        get_all()
        print("#################################################")
        time.sleep(300)


if __name__ == '__main__':
    run()

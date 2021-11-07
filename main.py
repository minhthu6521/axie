import json
import time
import urllib

import requests

URL = "https://axieinfinity.com/graphql-server-v2/graphql"
PARAMS = {
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
    "variables": {
        "from": 0,
        "size": 30, "auctionType": "Sale", "sort": "PriceAsc",
        "criteria": {
            "breedCount": [0, 7],
            "numMystic": [0, 1, 2, 3, 4, 5, 6],
            "pureness": [1, 2, 3, 4, 5, 6],
            "classes": ["Dusk"],
            "hp": [27, 61],
            "morale": [27, 61],
            "speed": [27, 61],
            "skill": [27, 61],
            "parts": ["tail-gravel-ant", "horn-kestrel"]
        }
    }
}

HTML_URL = "https://www.axielegend.com/"
HTML_PARAMS = {
    "parts": PARAMS["variables"]["criteria"]["parts"],
    "classes": PARAMS["variables"]["criteria"]["classes"],
    "hp": PARAMS["variables"]["criteria"]["hp"][0],
    "speed": PARAMS["variables"]["criteria"]["speed"][0],
}


def get_details():
    res = requests.post(URL, data=json.dumps(PARAMS), headers={"Content-Type": "application/json"})
    res_json = json.loads(res.content)
    return res_json["data"]["axies"]["results"]


REAL_PRICE = lambda x: float(x["auction"]["currentPriceUSD"])


def run():
    while (True):
        details = get_details()
        if (REAL_PRICE(details[1]) - REAL_PRICE(details[0])) >= (REAL_PRICE(details[1]) / 10):
            import winsound
            duration = 1000  # milliseconds
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            params = urllib.parse.urlencode(HTML_PARAMS)
            print("-------------------------------")
            print(HTML_URL + params)
            print(f"Difference:{REAL_PRICE(details[1]) - REAL_PRICE(details[0])}")
            print("-------------------------------")
        time.sleep(300)


if __name__ == '__main__':
    run()

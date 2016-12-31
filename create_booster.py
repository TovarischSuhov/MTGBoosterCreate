#!/usr/bin/env python3

import argparse
import requests
import json
import random
import os
import pycurl

def main():
    random.seed()
    parser = argparse.ArgumentParser(description="Creates boosters from selected block or set")
    parser.add_argument("-b", "--block", type=str, help="Sets block to create booster")
    parser.add_argument("-n", "--count", type=int, default=1, help="Sets number of boosters to create")
    args = parser.parse_args()

    sets = json.loads(requests.get('https://api.magicthegathering.io/v1/sets', data = {"block": args.block}).text)["sets"]
    i = 0
    while i < args.count:
        i += 1;
        s = sets[random.randint(0, len(sets)-1)]
        dirname = "/tmp/booster_" + str(i)
        try:
            os.makedirs(dirname)
        except:
            print("Directory already exists")
        k = 0
        for j in s["booster"]:
            k += 1
            cards = json.loads(requests.get('https://api.magicthegathering.io/v1/cards', data = { "set": s["code"], "rarity": j}).text)["cards"]
            c = cards[random.randint(0,len(cards)-1)]
            picture = requests.get(c["imageUrl"])
            path = dirname + "/" + str(k) + ".jpg"
            fin = open(path, "w+b")
            fin.write(picture.content)
            fin.close()
            

if __name__ == "__main__":
    main()
#!/usr/bin/env python3

import argparse
import requests
import json
import random
import os
import shutil

def main():
    random.seed()
    parser = argparse.ArgumentParser(description="Creates boosters from selected block or set")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-b", "--block", type=str, help="Sets block to create booster")
    group.add_argument("-s", "--set", type=str, help="Sets set code to create booster")
    parser.add_argument("-n", "--count", type=int, default=1, help="Sets number of boosters to create")
    args = parser.parse_args()
    sets = []
    if not args.block:
        sets = json.loads(requests.get('https://api.magicthegathering.io/v1/sets', data = {"block": args.block}).text)["sets"]
    i = 0
    olddir = os.getcwd()
    while i < args.count:
        i += 1;
        s = {}
        if not sets:
            s = sets[random.randint(0, len(sets)-1)]
        else:
            s= json.loads(requests.get('https://api.magicthegathering.io/v1/sets/' + args.set).text)["set"]
        dirname = "/tmp/booster"
        shutil.rmtree(dirname)
        try:
            os.makedirs(dirname)
        except:
            print("Directory already exists")
        k = 0
        for j in s["booster"]:
            if j == "land" or j == "marketing":
                continue
            k += 1
            rr = ''
            if isinstance(j, list):
                for a in j:
                    rr += a + ","
                rr = rr[:-1]
            else:
                rr = j
            cards = json.loads(requests.get('https://api.magicthegathering.io/v1/cards', data = { "set": s["code"], "rarity": rr}).text)["cards"]
            c = cards[random.randint(0,len(cards)-1)]
            picture = requests.get(c["imageUrl"])
            path = dirname + "/" + str(k) + ".jpg"
            fin = open(path, "w+b")
            fin.write(picture.content)
            fin.close()
        shutil.copy("template.tex", dirname)
        os.chdir(dirname)
        os.system("pdflatex " + "template.tex")
        os.chdir(olddir)
        shutil.copy(dirname + "/template.pdf", "booster" + str(i) + ".pdf")

if __name__ == "__main__":
    main()

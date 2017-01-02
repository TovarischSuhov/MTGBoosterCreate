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
        sets = []
    else:
        sets = json.loads(requests.get('https://api.magicthegathering.io/v1/sets', data = {"block": args.block}).text)["sets"]
    i = 0
    olddir = os.getcwd()
    dirname = "/tmp/booster"
    try:
        shutil.rmtree(dirname)
        os.makedirs(dirname)
    except:
        print("Directory already exists")
    os.chdir(dirname)
    tex = open(dirname + "/template.tex", "w")
    tex.write("\\documentclass[a4paper, 10pt]{extarticle}\n\
\\usepackage[left=5mm, top=5mm, right=5mm, bottom=5mm, nohead, nofoot]{geometry}\n\
\\usepackage{graphicx}\n\
\\begin{document}\n")
    while i < args.count:
        i += 1;
        s = {}
        if not sets:
            s= json.loads(requests.get('https://api.magicthegathering.io/v1/sets/' + args.set).text)["set"]
        else:
            s = sets[random.randint(0, len(sets)-1)]
        if not args.block:
            tex.write("\\center\n\\Huge{Set "+ s["code"] +"}\n\\\\")
        else:    
            tex.write("\\center\n\\Huge{Block " + args.block + " Set "+ s["code"] +"}\n\\\\")
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
            path = dirname + "/" + str(i) + "_" + str(k) + ".jpg"
            fin = open(path, "w+b")
            fin.write(picture.content)
            fin.close()
            tex.write("\\includegraphics[width=63mm,height=88mm]{" + str(i) + "_"  + str(k) + ".jpg}\n")
            if k % 3 == 0:
                tex.write("\\\\\n")
        tex.write("\\newpage\n")
    tex.write("\\end{document}")
    tex.close()
    os.system("pdflatex " + "template.tex")
    os.chdir(olddir)
    shutil.copy(dirname + "/template.pdf", "boosters.pdf")

if __name__ == "__main__":
    main()

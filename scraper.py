import requests
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import os
import json
import csv

@dataclass
class Item:
    opt1: str
    opt2: str
    opt3: str

@dataclass
class Scraper:

    def fetch(self, url):
        with requests.Session() as s:
            r = s.get(url)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
        return r

    def parse(self, r):
        locator = ''
        opt1_loc = ''
        opt2_loc = ''
        opt3_loc = ''
        tree = HTMLParser(r.text)
        staging = tree.css(locator)
        items = []
        for sub in staging:
            try:
                opt1 = sub.css_first(opt1_loc)
                opt2 = sub.css_first(opt2_loc)
                opt3 = sub.css_first(opt3_loc)
                items.append(asdict(Item(opt1 = opt1, opt2=opt2, opt3=opt3)))
            except:
                continue
        return items

    def download_img(self, img_urls, folder_name):
        for url in img_urls:
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            if url != None:
                with requests.Session() as s:
                    r = s.get(url)
                with open(f"{folder_name}/{url.split('/')[-1]}", 'wb') as f:
                    f.write(r.content)
            print('Image downloaded successfully!')

    def to_csv(self, datas, filename, headers):
        try:
            for data in datas:
                try:
                    file_exists = os.path.isfile(filename)
                    with open(filename, 'a', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)
                        if not file_exists:
                            writer.writeheader()
                        if data != None:
                            writer.writerow(data)
                        else:
                            continue
                except Exception as e:
                    print(e)
                    continue
        except:
            pass
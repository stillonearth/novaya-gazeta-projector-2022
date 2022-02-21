import requests
from pyquery import PyQuery as pq
from progress.bar import Bar
import json


def parse_rks(page):
    url = "https://reestr.rublacklist.net/?page={}".format(page)
    result = pq(requests.get(url).text)
    links = []
    for record in result("table tbody tr"):
        date = pq(pq(record)("td")[1]).text()
        url = pq(pq(record)("td")[2]).text()
        dep = pq(pq(record)("td")[4]).text()
        links.append((date, url, dep))
    return links

def fetch_rks():
    links = []
    for page in Bar('BlocksByTimeRKS', check_tty=False).iter(range(12000, 22000)):
        new_list = parse_rks(page)
        links += new_list
        
        with open('data/03-rks.json', 'w') as fp:
            json.dump(links, fp,  indent=4)
        
        if len(new_list) < 50: continue 
        page += 1
    return links

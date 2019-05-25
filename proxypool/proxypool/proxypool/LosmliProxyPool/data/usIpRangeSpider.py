import csv

import requests
from lxml import etree


def download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    response = requests.get(url, headers=headers)
    selector = etree.HTML(response.content)
    return selector


def parse(html):
    tr_list = html.xpath('//table/tbody/tr')
    for tr in tr_list:
        item = {}
        item['from'] = tr.xpath('./td[1]/text()')[0]
        item['to'] = tr.xpath('./td[2]/text()')[0]
        item['num'] = tr.xpath('./td[3]/text()')[0]
        yield item


def main():
    url = 'https://lite.ip2location.com/united-states-ip-address-ranges'
    html = download(url)
    csvfile = open("US-20190109.csv", "w", encoding='utf-8', newline='')
    fieldnames = ['from', 'to', 'num']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for item in parse(html):
        writer.writerow(dict(item))
    csvfile.close()


if __name__ == '__main__':
    main()

import csv

import requests
from lxml import etree


def download(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    proxies = {"http": 'http://139.162.14.11:3128'}
    response = requests.get(url, headers=headers, proxies=proxies)
    selector = etree.HTML(response.content)
    return selector


def parse(html):
    tr_list = html.xpath('//table/tbody/tr')
    for tr in tr_list:
        item = {}
        item['useragent'] = tr.xpath('./td[1]/a/text()')[0]
        item['version'] = tr.xpath('./td[2]/text()')[0]
        item['os'] = tr.xpath('./td[3]/text()')[0]
        item['type'] = tr.xpath('./td[4]/text()')[0]
        item['polularity'] = tr.xpath('./td[5]/text()')[0]
        yield item


def main():
    csvfile = open("chrome-useragent.csv", "w", encoding='utf-8', newline='')
    fieldnames = ['useragent', 'version', 'os', 'type', 'polularity']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    url = 'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/%d'
    for page in range(1, 12):
        html = download(url % page)
        for item in parse(html):
            writer.writerow(dict(item))
    csvfile.close()


if __name__ == '__main__':
    main()

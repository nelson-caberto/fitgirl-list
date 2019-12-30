from lxml import html
import requests
import csv
from time import sleep

def getRepacks(pageNumber):
    global repacks
    response = requests.get(f'http://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={pageNumber}#lcp_instance_0')
    #assert no issues with request
    repacks = html.fromstring(response.content).xpath('//ul[@class="lcp_catlist"]/li/a/@href')
    return repacks

def scrapeRepack(url):
    global scrapeData
    response = requests.get(url)
    page = html.fromstring(response.content)

    results = {}
    for data in scrapeData:
        scrape = page.xpath(scrapeData[data])
        if scrape:
            results[data] = scrape[0]
        else:
            results[data] = ''

    return results

def getLatestRepacks():
    global repacks
    response = requests.get('http://fitgirl-repacks.site/category/lossless-repack/')
    #assert no issues with request
    repacks = html.fromstring(response.content).xpath('//h1[@class="entry-title"]/a/@href')
    return repacks

scrapeData = {
    'title':'//h1[@class="entry-title"]/text()',
    'repack_date':'//time[@class="entry-date"]/@datetime',
    'l377x_url':'//a[text()="1337x"]/@href',
    'KAT_url':'//a[text()="KAT"]/@href',
    'magnet':'//a[text()="magnet"]/@href'
}

with open('latest repacks.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=scrapeData.keys())
    writer.writeheader()
    for repack in getLatestRepacks():
        print(repack)
        writer.writerow(scrapeRepack(repack))
        sleep(0.5)

with open('repacks.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=scrapeData.keys())
    writer.writeheader()
    page = 1
    while len(getRepacks(page)) > 0:
        page = page + 1
        for repack in repacks:
            print(repack)
            writer.writerow(scrapeRepack(repack))

            #be nice, dont spam
            sleep(0.5)
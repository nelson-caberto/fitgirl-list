from lxml import html
import requests
import csv
import time

def getRepacks(pageNumber):
    global repacks
    response = requests.get(f'http://fitgirl-repacks.site/all-my-repacks-a-z/?lcp_page0={pageNumber}#lcp_instance_0')
    #assert no issues with request
    repacks = html.fromstring(response.content).xpath('//ul[@class="lcp_catlist"]/li/a/@href')
    return repacks

def scrapeRepack(url):
    response = requests.get(url)
    page = html.fromstring(response.content)

    title = page.xpath('//h1[@class="entry-title"]/text()')[0]
    repack_date = page.xpath('//time[@class="entry-date"]/@datetime')[0]
    magnet = page.xpath('//a[text()="magnet"]/@href')

    #check in case there is no magnet link
    if magnet:
        magnet = magnet[0]
    else:
        magnet = ''

    #be nice, dont spam
    time.sleep(1)

    return (title, repack_date, magnet)

with open('repacks.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title','repack date','magnet link'])
    page = 1
    while len(getRepacks(page)) > 0:
        page = page + 1
        for repack in repacks:
            print(repack)
            writer.writerow(scrapeRepack(repack))

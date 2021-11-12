#!/usr/bin/python3

import re
import os
import sys
import json
import requests
from mail import Mail
from bs4 import BeautifulSoup

base_site = "https://www.barby.co.il/"

def main():
    newShows = getData()

    if newShows:
        print('emailing the new shows:\n' + str(newShows))
        emailShows(newShows)
        allShows = get_all_shows(newShows)
        writeData(allShows)

def emailShows(newShows):
    subject = 'New Barby show%s posted!' % 's' if len(newShows) > 1 else ''

    body = ''

    for date, priceAndName in newShows.items():
        price = priceAndName['price']
        bandName = priceAndName['bandName']
        body += f"{bandName},  {date} -- {price} Shekel \n"

    Mail.send_email(subject=subject, body=body)

def get_all_shows(newShows):
    with open('barbyShows.txt', "r", encoding="utf8") as json_file:
        oldShows = json.load(json_file)

    allShows = {**oldShows, **newShows} if oldShows else newShows

    return allShows

def getData():
    newShows = {}

    with open('barbyShows.txt', "r", encoding="utf8") as json_file:
        oldShows = json.load(json_file)

    response = requests.get(base_site, headers={'User-Agent': 'Mozilla/5.0'})

    html = response.content
    soup = BeautifulSoup(html, 'lxml')

    bandDivs = soup.find_all('td', class_="defaultRowHeight")

    for band in bandDivs:
        # For some reason some have Big
        nameBig   = band.find('div', class_="inlineDefNameBig")
        nameNoBig = band.find('div', class_="inlineDefName")
        bandName  = nameBig.text if nameBig else nameNoBig.text
        time      = band.find('div', class_="def_titel2A").text

        # This is a new show
        if time not in oldShows.keys():
            SiteDiv = band.find('div', class_='defShowListDescDiv')
            SpecificShowPage  = SiteDiv.find('a').attrs['href']
            FullSite = base_site + SpecificShowPage
            price = get_price_of_show(FullSite)
            newShows[time] = {'bandName' : bandName, 'price' : price}

    return newShows

def get_price_of_show(site):
    response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})

    html = response.content
    soup = BeautifulSoup(html, 'lxml')

    try:
        priceText = soup.find('span', class_="showCatlbPrice").text
        price = re.search(r'\d+', priceText)
        price = price.group(0)

    except:
        priceText = 'None'

    return price

def writeData(data):
    with open('barbyShows.txt', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()


#!/usr/bin/python3

import os
import sys
import json
import requests
from mail import Mail
from bs4 import BeautifulSoup

base_site = "https://www.barby.co.il/"

def main():
    try:
        allShows = getData()
        newShows = getNewShows(allShows)

        if newShows:
            emailShows(newShows)
            writeData(allShows)

    except:
        sendEmail("Failed to run Barby Notifyer", '')

def emailShows(newShows):
    subject = 'New Barby show%s posted!' % 's' if len(newShows) > 1 else ''

    body = ''

    for date, name in newShows.items():
        body += f"{name}, {date} \n"

    Mail.send_email(subject=subject, body=body)

def getNewShows(allShows):
    newShows = {}

    with open('barbyShows.txt', "r", encoding="utf8") as json_file:
        oldShows =  json.load(json_file)
    
    for date, bandName in allShows.items():
        if date not in oldShows:
            newShows[date] = bandName

    return newShows

def getData():
    response = requests.get(base_site, headers={'User-Agent': 'Mozilla/5.0'})

    print(response)
    html = response.content
    soup = BeautifulSoup(html, 'lxml')

    with open('barby.html', 'wb') as file:
        file.write(soup.prettify('utf-8'))

    bandDivs = soup.find_all('td', class_="defaultRowHeight")

    shows = {}

    for band in bandDivs:
        # For some reason some have Big
        nameBig   = band.find('div', class_="inlineDefNameBig")
        nameNoBig = band.find('div', class_="inlineDefName")
        bandName  = nameBig.text if nameBig else nameNoBig.text
        time      = band.find('div', class_="def_titel2A").text
        
        shows[time] = bandName

    return shows

# def sendEmail(subject, body):
#     Mail.send_email(subject=subject, body=body)


def writeData(data):
    with open('barbyShows.txt', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()


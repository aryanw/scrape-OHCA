#!/usr/bin/env python
__author__ = "Aryan wagadre"

from email import header
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import csv


'''
params
@input url
@input headers
@output dataentry list
'''
def scrapeFacility(URL,headers):
    result = requests.get(URL, headers=headers)
    soup = bs(result.content, "html.parser")
    results = soup.find(id="main")
    dataentry = []

    # county (can be assigned multiple counties)
    if soup.find(class_="ill_directory_category_county"):
        dataentry.append(soup.find(class_="ill_directory_category_county").a.text)
    else:
        dataentry.append(None)
    # name of facility (error prone)
    if results.find("h1"):
        dataentry.append(results.find("h1").text.strip())
    else:
        dataentry.append(None)
    #directory_email 
    if soup.find(class_="ill_directory_email"):
        dataentry.append(soup.find(class_="ill_directory_email").text)
    else:
        dataentry.append(None)
    #email
    if soup.find(class_="email"):
        if soup.find(class_="email").b:
            len3 = len(soup.find(class_="email").b.text) 
            email = soup.find(class_="email").text[len3:]
            dataentry.append(email.strip())
        else:
            dataentry.append(None)
    else:
        dataentry.append(None)
    #directory_phone
    if soup.find(class_="ill_directory_phone"):
        dataentry.append(soup.find(class_="ill_directory_phone").text)
    else:
        dataentry.append(None)
    #directory_website
    if soup.find(class_="ill_directory_web_url"):
        dataentry.append(soup.find(class_="ill_directory_web_url").text)
    else:
        dataentry.append(None)
    # facility_type (can be assigned multiple facilities)
    if soup.find(class_="ill_directory_category_facility-type"):
        dataentry.append(soup.find(class_="ill_directory_category_facility-type").a.text)
    else:
        dataentry.append(None)
    # capacity 
    if soup.find(class_="capacity"):
        len1 = len(soup.find(class_="capacity").b.text) 
        capacity = int(soup.find(class_="capacity").text[len1:])
        dataentry.append(capacity)
    else:
        dataentry.append(None)
    # unitcount
    if soup.find(class_="unitcount"):
        len2 = len(soup.find(class_="unitcount").b.text) 
        unitcount = int(soup.find(class_="unitcount").text[len2:])
        if not unitcount:
            dataentry.append(None)
        else:
            dataentry.append(unitcount)
    
    else:
        dataentry.append(None)
    # address of facility (error prone)
    if results.p:
        dataentry.append(" ".join(results.p.text.strip().split("\n")))
    else:
        dataentry.append(None)
    return dataentry   


URL = "https://www.ohca.com/facility-finder/"

UA = ""
headers = {'User-Agent': UA}
result = requests.get(URL, headers=headers)

soup = bs(result.content, "html.parser")
results = soup.find(id="ill_directory_list")
cities = results.find_all("div", class_="ill_directory_list_block ill_directory_list_city")
data = []

for city in cities:
    #get city name
    city_name = city.find('h3').text
    print("working: ",city_name)
    for li in city.find_all(class_="ill_directory_is_member"):
        url = li.a.get('href')
        data.append([city_name]+scrapeFacility(url,headers))
    sleep(.5)
  
with open("output.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)
    
# print(scrapeFacility("https://www.ohca.com/facility-finder/avamere-at-albany/",headers))

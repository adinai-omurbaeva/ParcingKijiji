import requests
from bs4 import BeautifulSoup
import math
from datetime import date, timedelta
from pandas import DataFrame
import csv
# from models import *
# from peewee import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials


url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-1/c37l1700273?ad=offering'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_='clearfix')
ad_image = []
ad_title = []
ad_location = []
ad_date = []
ad_bedrooms = []
ad_description = []
ad_price = []
ad_currency = []

"""Counting total pages"""
pages = soup.find('span', class_='resultsShowingCount-1707762110').text.split()
page_number = math.ceil(int(pages[5])/40)

"""Main Parcer"""
# for page_num in range(1, page_number+1):
#     newUrl = url.replace('page-1', 'page-'+str(page_num))
#     response = requests.get(newUrl)
#     soup = BeautifulSoup(response.text, 'lxml')
#     items = soup.find_all('div', class_='clearfix')
#     for i in items:
#         soup_image = i.find('picture')
#         soup_title = i.find('a', class_='title')
#         soup_location = i.find('div', class_='location')
#         soup_date = i.find('span', class_='date-posted')
#         soup_bedrooms = i.find('span', class_='bedrooms')
#         soup_description = i.find('div', class_='description')
#         soup_price = i.find('div', class_='price')
#         if soup_image!=None:
#             ad_image.append(soup_image.img['data-src'])
#             ad_title.append(soup_title.text.strip())
#             ad_location.append(soup_location.span.text.strip())
#             ad_date.append(soup_date.text.strip())
#             ad_bedrooms.append(soup_bedrooms.text.replace("Beds:\n",'').strip())
#             ad_description.append(soup_description.text.replace('\n', '').split('...', 1)[0].strip())
#             ad_price.append(soup_price.text.replace('\n', '').strip())

for i in items:
    soup_image = i.find('picture')
    soup_title = i.find('a', class_='title')
    soup_location = i.find('div', class_='location')
    soup_date = i.find('span', class_='date-posted')
    soup_bedrooms = i.find('span', class_='bedrooms')
    soup_description = i.find('div', class_='description')
    soup_price = i.find('div', class_='price')
    if soup_image!=None:
        ad_image.append(soup_image.img['data-src'])
        ad_title.append(soup_title.text.strip())
        ad_location.append(soup_location.span.text.strip())
        ad_date.append(soup_date.text.strip())
        ad_bedrooms.append(soup_bedrooms.text.replace("Beds:\n",'').strip())
        ad_description.append(soup_description.text.replace('\n', '').split('...', 1)[0].strip())
        ad_price.append(soup_price.text.replace('\n', '').strip())

"""Right Date data"""
for i in range(0, len(ad_date)):
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    if '/' in ad_date[i]:
        ad_date[i] = ad_date[i].replace('/', '-')
    elif 'Yesterday' in ad_date[i]:
        ad_date[i] = yesterday.strftime("%d-%m-%Y")
    else:
        ad_date[i] = today.strftime("%d-%m-%Y")

"""Getting Currency"""       
for i in range(0, len(ad_price)):
    if "$" in ad_price[i]:
        ad_currency.append('$')
        ad_price[i] = ad_price[i][1:]
    else:
        ad_currency.append(ad_price[i])

def write_to_sheet():
    gc = gspread.service_account(filename='semiotic-bloom-362118-5ec0169b15e2.json')
    # sh = gc.open("DataOx_parcing")
    sheet = gc.open("DataOx_parcing").sheet1 
    sheet.clear()
    for i in range(0, len(ad_image)):
        insertRow = [ad_image[i],ad_title[i],ad_location[i],ad_date[i],
                ad_bedrooms[i],ad_description[i], ad_price[i],ad_currency[i]]
        # sheet.insert_row(insertRow, i)
        sheet.append_row(insertRow)

write_to_sheet()

"""Writing to scv file"""
['Image', 'Title', 'Location', 'Date', 'Bedrooms', 'Description', 'Price', 'Currency']
data = {'Ad_Image': ad_image, 'Ad_Title':ad_title, 'Ad_Location':ad_location, 
        'Ad_Date':ad_date, 'Ad_Bedrooms':ad_bedrooms, 'Ad_Description':ad_description,
        'Ad_Price':ad_price, 'Ad_Currency':ad_currency}
df = DataFrame(data, columns = 
['Ad_Image','Ad_Title','Ad_Location','Ad_Date','Ad_Bedrooms','Ad_Description','Ad_Price','Ad_Currency'])
df.to_csv('Ads_kijiji.csv')
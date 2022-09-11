import requests
from bs4 import BeautifulSoup
import math
from datetime import date, timedelta
from pandas import DataFrame
import csv
# from models import *
# from peewee import *
import gspread
from gspread import BackoffClient
from oauth2client.service_account import ServiceAccountCredentials


url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-1/c37l1700273?ad=offering'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
items = soup.find_all('div', class_='clearfix')

"""Counting total pages"""
pages = soup.find('span', class_='resultsShowingCount-1707762110').text.split()
page_number = math.ceil(int(pages[5])/40)


"""Connection to Google Sheets"""
gc = gspread.service_account(filename='semiotic-bloom-362118-5ec0169b15e2.json', 
                            client_factory=BackoffClient)
sheet = gc.open("DataOx_parcing").sheet1 
sheet.clear()

"""Main Parcer"""
for page_num in range(1, page_number+1):
    newUrl = url.replace('page-1', 'page-'+str(page_num))
    response = requests.get(newUrl)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='clearfix')
    
    for i in items:
        soup_image = i.find('picture')
        soup_title = i.find('a', class_='title')
        soup_location = i.find('div', class_='location')
        soup_date = i.find('span', class_='date-posted')
        soup_bedrooms = i.find('span', class_='bedrooms')
        soup_description = i.find('div', class_='description')
        soup_price = i.find('div', class_='price')
        if soup_image!=None:
            """Right Date data"""
            today = date.today()
            yesterday = date.today() - timedelta(days=1)
            this_date = soup_date.text.strip()
            if '/' in this_date:
                this_date = this_date.replace('/', '-')
            elif 'Yesterday' in this_date:
                this_date = yesterday.strftime("%d-%m-%Y")
            else:
                this_date = today.strftime("%d-%m-%Y")
            """Getting Currency"""
            this_price = soup_price.text.replace('\n', '').strip()   
            this_currency = ''
            if "$" in this_price:
                this_currency = this_price.replace('$', '')
            else:
                this_currency = this_price
            
            insertRow = [soup_image.img['data-src'], soup_title.text.strip(),
                    soup_location.span.text.strip(), this_date, 
                    soup_bedrooms.text.replace("Beds:\n",'').strip(), 
                    soup_description.text.replace('\n', '').split('...', 1)[0].strip(), 
                    this_price, this_currency]
            sheet.append_row(insertRow)
    # print(page_num)


""" Code for previous version. Not working with new version, 
    but can pe upgraded, if local file needed """
# """Writing to scv file"""
# data = {'Image': ad_image, 'Title':ad_title, 'Location':ad_location, 
#         'Date':ad_date, 'Bedrooms':ad_bedrooms, 'Description':ad_description,
#         'Price':ad_price, 'Currency':ad_currency}
# df = DataFrame(data, columns = 
# ['Image','Title','Location','Date','Bedrooms','Description','Price','Currency'])
# df.to_csv('Ads_kijiji.csv')
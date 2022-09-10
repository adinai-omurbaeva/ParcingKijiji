import requests
from bs4 import BeautifulSoup
import math
from datetime import date, timedelta
from pandas import DataFrame
import csv


url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-1/c37l1700273?ad=offering'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
# soup = BeautifulSoup(response.content,"html.parser")
items = soup.find_all('div', class_='clearfix')

with open('Ads_kijiji.csv', mode='w') as csv_file:
   fieldnames = ['Image', 'Title', 'Location', 'Date', 'Bedrooms', 'Description', 'Price', 'Currency']
   writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
   writer.writeheader()

ad_image = []
ad_title = []
ad_location = []
ad_date = []
ad_bedrooms = []
ad_description = []
ad_price = []
ad_currency = []
for i in items:
    soup_image = i.find('img')
    soup_title = i.find('a', class_='title')
    soup_location = i.find('div', class_='location')
    soup_date = i.find('span', class_='date-posted')
    soup_bedrooms = i.find('span', class_='bedrooms')
    soup_description = i.find('div', class_='description')
    soup_price = i.find('div', class_='price')
    if soup_image!=None:
        ad_image.append(soup_image['data-src'])
        ad_title.append(soup_title.text.strip())
        ad_location.append(soup_location.span.text.strip())
        ad_date.append(soup_date.text.strip())
        ad_bedrooms.append(soup_bedrooms.text.replace("Beds:\n",'').strip())
        ad_description.append(soup_description.text.replace('\n', '').split('...', 1)[0].strip())
        ad_price.append(soup_price.text.replace('\n', '').strip())

for i in range(0, len(ad_date)):
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    if '/' in ad_date[i]:
        ad_date[i] = ad_date[i].replace('/', '-')
    elif 'Yesterday' in ad_date[i]:
        ad_date[i] = yesterday.strftime("%d-%m-%Y")
    else:
        ad_date[i] = today.strftime("%d-%m-%Y")
for i in range(0, len(ad_price)):
    if "$" in ad_price[i]:
        ad_currency.append('$')
        ad_price[i] = ad_price[i][1:]
    else:
        ad_currency.append(ad_price[i])


"""Counting total pages"""
pages = soup.find('span', class_='resultsShowingCount-1707762110').text.split()
page_number = math.ceil(int(pages[5])/40)


# for page_num in range(1, page_number+1):
#     newUrl = url.replace('page-1', 'page-'+str(page_num))
#     response = requests.get(newUrl)
#     soup = BeautifulSoup(response.text, 'lxml')
#     items = soup.find_all('div', class_='clearfix')
#     for i in items:
#         soup_image = i.find('img')
#         soup_title = i.find('a', class_='title')
#         soup_location = i.find('div', class_='location')
#         soup_date = i.find('span', class_='date-posted')
#         soup_bedrooms = i.find('span', class_='bedrooms')
#         soup_description = i.find('div', class_='description')
#         soup_price = i.find('div', class_='price')
#         if soup_image!=None:
#             ad_image.append(soup_image['data-src'])
#             ad_title.append(soup_title.text.strip())
#             ad_location.append(soup_location.text.strip())
#             ad_date.append(soup_date.text.strip())
#             ad_bedrooms.append(soup_bedrooms.text.strip())
#             ad_description.append(soup_description.text.strip())
#             ad_price.append(soup_description.text.strip())

['Image', 'Title', 'Location', 'Date', 'Bedrooms', 'Description', 'Price', 'Currency']
data = {'Ad_Image': ad_image, 'Ad_Title':ad_title, 'Ad_Location':ad_location, 
        'Ad_Date':ad_date, 'Ad_Bedrooms':ad_bedrooms, 'Ad_Description':ad_description,
        'Ad_Price':ad_price, 'Ad_Currency':ad_currency}
df = DataFrame(data, columns = 
['Ad_Image','Ad_Title','Ad_Location','Ad_Date','Ad_Bedrooms','Ad_Description','Ad_Price','Ad_Currency'])
df.to_csv('Ads_kijiji.csv')
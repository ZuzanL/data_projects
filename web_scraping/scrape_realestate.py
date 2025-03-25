from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.exceptions import RequestException
import json

# SCRAPING MULTIPLE PAGES
base_url = 'https://www.sreality.cz/hledani/prodej,pronajem/byty,domy'
page = 1
max_pages = 100

property_data = []

while True:
    #Break if page number is greater than max_pages
    if page > max_pages:
        break
    
    # Request the page(specific page number)
    url = f"{base_url}?strana={page}"
    response = requests.get(url)

    #Break the loop if request fails = all pages have been scraped
    try:
        response = requests.get(url)
        response.raise_for_status()
    except RequestException as e:
        print(f'Request failed: {e}')
        break

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all properties and their information on the page
    properties = soup.find_all('div', class_='css-173t8lh')

    #Break the loop if no more products are found
    if not properties:
        break

    for product in properties:
        name = product.find('p', class_='css-d7upve')
        if name:
            p_name = name.get_text()
        else:
            p_name = "N/A"  

        address = product.select_one('p.css-d7upve:nth-of-type(2)') # Selects the second p with class css-d7upve
        if address:
            p_address = address.get_text(strip=True)
        else:
            p_address = "N/A"

        price = product.find('p', class_='css-ca9wwd')
        if price:
            p_price = price.get_text()
        else:
            p_price = "N/A"

        
        # CREATING A DICTIONARY TO WRITE INTO JSON FILE
        property_data.append(
            {
                'name': p_name,
                'adress': p_address,
                'price': p_price
            }
        )

    page += 1


# CREATING JSON FILE
with open('real_estate.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(property_data, jsonfile, ensure_ascii=False, indent=4)
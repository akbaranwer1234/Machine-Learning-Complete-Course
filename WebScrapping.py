import requests
from bs4 import BeautifulSoup
import csv
import json
import time


def scrape_realtor_data(location):
    base_url = f'https://www.realtor.com/realestateandhomes-search/{location}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    try:
        response = requests.get(base_url, headers=headers)
        # print(response.content)
        response.raise_for_status()
        # base_url = response.url
        # print(base_url)

        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)

        property_titles = [title.text.strip() for title in soup.select('.card-address')]
        property_prices = [price.text.strip() for price in soup.select('.card-price')]
        property_urls = ['https://www.realtor.com'+url['href'] for url in soup.select('.LinkComponent_anchor__0C2xC')]
        
        # print(len(property_titles))
        # print(len(property_prices))
        # print(len(property_urls))

        data = [{'Title': title, 'Price': price, 'URL': url} for title, price, url in zip(property_titles, property_prices, property_urls)]

        csv_file_path = f'realtor_data_{location}.csv'
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Price', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        json_file_path = f'realtor_data_{location}.json'
        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)

        print(f'Realtor.com data successfully scraped and saved to {csv_file_path} and {json_file_path}')

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

scrape_realtor_data('55113')
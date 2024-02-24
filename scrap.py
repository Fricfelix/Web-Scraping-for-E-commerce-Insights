import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.jumia.com.ng/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with requests.Session() as session:
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    diff_products_layer = soup.find('div', class_='col16 -df -j-bet -pbs')
    second_diff_products_layer = diff_products_layer.find('div', class_='flyout-w -fsh0 -fs0')
    inner_layer_diff_products = second_diff_products_layer.find('div', class_='flyout')
    categories_links = inner_layer_diff_products.find_all('a', class_='itm')

    with open('Jumia_product_data_2-24-2024.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product Category', 'Product Name', 'Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for link in categories_links:
            category_link = link.get('href')
            if category_link:
                if category_link.startswith('/'):
                    category_link = url + category_link

                category_text = link.span.text
                print("Category:", category_text)

                page_number = 1
                while True:
                    category_response = session.get(f"{category_link}?page={page_number}#catalog-listing", headers=headers)
                    category_soup = BeautifulSoup(category_response.content, 'lxml')

                    products = category_soup.find_all('a', class_='core')

                    for product in products:
                        product_name_elem = product.find('h3', class_='name')
                        if product_name_elem:
                            product_name = product_name_elem.text.strip()
                            product_price_elem = product.find('div', class_='prc')
                            if product_price_elem:
                                product_price = product_price_elem.text.strip()
                                print("Product:", product_name)
                                print("Price:", product_price)
                                writer.writerow({'Product Category': category_text, 'Product Name': product_name, 'Price': product_price})

                    next_page_link = category_soup.select_one('a.pg[aria-label="Next Page"]')
                    if not next_page_link:
                        break  # No more pages to scrape
                    page_number += 1

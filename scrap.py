import requests
from bs4 import BeautifulSoup

url = 'https://www.jumia.com.ng/'

# Set up headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Create a session to make the request
with requests.Session() as session:
    # Send a GET request to the initial URL
    response = session.get(url, headers=headers)

    # Parse the HTML content of the initial page
    soup = BeautifulSoup(response.content, 'lxml')

    # # Find all pagination links
    diff_products_layer = soup.find('div', class_='col16 -df -j-bet -pbs')
    second_diff_products_layer = diff_products_layer.find('div',class_='flyout-w -fsh0 -fs0')
    inner_layer_diff_products = second_diff_products_layer.find('div',class_='flyout')
    categories_links = inner_layer_diff_products.find_all('a',class_='itm')
    print(categories_links)

    # # Iterate through each pagination link
    # for link in pagination_links:
    #     # Extract the URL of the pagination link
    #     page_url = link['href']

    #     # Send a GET request to the pagination URL
    #     page_response = session.get(page_url, headers=headers)

    #     # Parse the HTML content of the pagination page
    #     page_soup = BeautifulSoup(page_response.content, 'html.parser')

    #     # Extract and process the desired information from the pagination page
    #     # Example: extract product names, prices, ratings, etc.

    #     # Repeat the process for each pagination link

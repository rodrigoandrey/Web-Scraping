from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

''' Python 3.9.1 '''
''' Create your virtual enviroment and install all requirements '''
''' Requirements in requirements.txt '''
''' I'll be using GoogleChrome for this app '''
''' It is necessary to install the webdriver for the browser you will be using.
    You can download the correct webdriver and put in the '/driver/' folder.
    Selenium documentation: https://pypi.org/project/selenium/ '''


# WEBDRIVER CLASS
class ChromeAuto:
    def __init__(self):
        self.driver_path = './driver/chromedriver.exe'  # need to change if you will be using another browser
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-data-dir=profile')  # Create a '/profile/' folder for caching
        self.driver = webdriver.Chrome(
            self.driver_path,
            options=self.options
        )

    def open_webdriver(self, url):
        self.driver.get(url)

    def close_webdriver(self):
        self.driver.quit()
        
    @staticmethod  # Method to create the search url in Amazon website
    def get_url(term):
        template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'
        fixed_term = term.replace(' ', '+')
        complete_url = template.format(fixed_term)

        # Paginator
        complete_url += '&page={}'

        return complete_url

    @staticmethod  # Method to extract what I need in the Amazon website (Product Name and Price)
    def extract_item(items):
        # Name
        _item = items
        product_name = _item.h2.a
        product_name = product_name.text.strip()

        # Price
        try:
            price_parent = _item.find('span', 'a-price')
            product_price = price_parent.find('span', 'a-offscreen').text

        except AttributeError:
            return

        product = {'Product_Name': product_name, 'Product_Price': product_price}

        return product


# MAIN IMPLEMENTATION OF THE PROGRAM
if __name__ == '__main__':

    # Starts Webdriver.
    chrome = ChromeAuto()
    records = []
    search_term = 'iphone'  # I'll be using 'iphone' as search term. Can be change (Ex: 'Galaxy s10').
    url = chrome.get_url(search_term)

    # Paginator (Amazon can go to 20 pages, if you want, you can set the maximum range to 21).
    for page in range(1, 2):  # Paginator Loop
        chrome.driver.get(url.format(page))
        soup = BeautifulSoup(chrome.driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:  # Extractor Loop
            record = chrome.extract_item(item)
            if record:
                records.append(record)

    chrome.close_webdriver()


# Saving data in excel file using Pandas.
    df = pd.DataFrame(records)

    df.to_excel(f'./files/{search_term}.xlsx')
    print(df)

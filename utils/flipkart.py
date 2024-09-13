from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller


def flipkart_search(query):
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # searching
    driver.get(f"https://www.flipkart.com/search?q={query}")
    
    # saving response
    content = driver.page_source
    soup = bs(content, 'lxml')
    
    products_found = []
    # Extract all product list
    for product_lists in soup.find_all('div', attrs={'class': '_75nlfW'}):
        # extract 4 product lists
        for products_4 in product_lists.find_all('div', attrs={'data-id': True}):
            # defining variables
            image_extracted = None
            price_extracted = None
            product_extracted = None
            
            # finding product image 
            image_tag = products_4.find_all('img')
            if image_tag:
                image_extracted = image_tag[0].get('src', '') 

            # finding price
            if image_extracted is not None:
                price_tag = products_4.find('div', attrs={'class': 'Nx9bqj'})
                if price_tag:
                     price_extracted = price_tag.get_text(strip=True) 

            # product name
            if price_extracted is not None:
                product_tag = products_4.find('a', title=True)
                if product_tag:
                    product_extracted = product_tag.get_text(strip=True)
            
            # adding to list
            if product_extracted is not None:
                products_found.append({
                    "image": image_extracted,
                    "price": price_extracted,
                    "product": product_extracted
                    })

    # extracting done
    print("done")
    if len(product_lists) > 1:
        return products_found
    else:
        return None
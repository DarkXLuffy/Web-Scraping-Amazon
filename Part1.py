import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


output=[]
# URL to scrape
url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"


d={"url":[], "name":[],"price":[],"rating":[],"number_of_review":[] }
# Function to scrape product details from a given URL
def scrape_product_details(url):
    if url==None:
        return
    # Send a GET request to the URL
    status_code=0
    while(status_code !=200):
        response = requests.get(url)
        status_code=response.status_code
        print(response)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the product containers on the page
    product_containers = soup.find_all("div", {"data-component-type": "s-search-result"})

    # Iterate over each product container
    for container in product_containers:
        # Extract the product details
        # product_url = "https://www.amazon.in" + container.find("a", {"class": "a-link-normal"}).['href]
        try:
            product_url = "https://www.amazon.in" + container.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style"}).get('href')
        except AttributeError:    
            try:
                product_url = "https://www.amazon.in" + container.find("a", {"class": "a-link-normal s-underline-text s-underline-link-text s-link-style"}).get('href')
            except:
                continue 
        
        try:
            product_name = container.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text
        except AttributeError:
            try:
                product_name = container.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).string.strip
            except:
                product_name= ""

        try:
            product_price = container.find("span", {"class": "a-price-whole"}).text
        except AttributeError:
            try:
                product_price = container.find("span", {"class": "a-price-whole"}).string.strip()
            except:   
                product_price=""
        
        try:
            product_rating = container.find("span", {"class": "a-icon-alt"}).text
        except AttributeError:
            try:
                product_rating = container.find("span", {"class": "a-icon-alt"}).string.strip()
            except:
                product_rating=""
        
        try:
            product_reviews = container.find("span", {"class": "a-size-base s-underline-text"}).text
        except AttributeError:
            try:
                product_reviews = container.find("span", {"class": "a-size-base s-underline-text"}).string.strip()
            except:
                product_reviews=""
        
        
        # Print the product details
        print("Product URL:", product_url)
        print("Product Name:", product_name)
        print("Product Price:", product_price)
        print("Product Rating:", product_rating)
        print("Number of Reviews:", product_reviews)
        print("---------------------------")
        d["url"].append(product_url)
        d["name"].append(product_name)
        d["price"].append(product_price)
        d["rating"].append(product_rating)
        d["number_of_review"].append(product_reviews)
    
    
    output.append(len(product_containers))
    try:
        next_url="https://www.amazon.in" + soup.find("a",attrs={"class":"s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"}).get('href')
        print(next_url)
        scrape_product_details(next_url)
    except Exception as e:
        print(e)

# Scrape product details from multiple pagess
# for page_number in range(1, 21):
#     page_url = url + f"{page_number}"
#     print("Scraping page:", page_number)
scrape_product_details(url)
for i in range(len(output)):
    print("Page", i+1, "--", output[i])

amazon_df = pd.DataFrame.from_dict(d)
amazon_df=amazon_df.drop_duplicates(subset=None, keep='first', inplace=False)

amazon_df.to_csv("amazon_data_final.csv", header=True, index=False)
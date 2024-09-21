import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

def get_property_name(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    elements = driver.find_elements(By.CSS_SELECTOR, ".Box-bx23rg-0.col-span-2.Flex-sc-9pwi7j-0.cffChp") # CLASS name
    for element in elements:
        text = element.text
        lines = text.split('\n')
        for l in lines:
            if "About" in l: # Extract line that contains 'About'
                return l.replace("About ", "") # Remove 'About' and return only the Property Name
    
def get_details(lst):
    details = ['','']
    for i in lst:
        if 'RM' in i:
            details[0] = i
        elif 'sq.ft.' in i:
            details[1] = i
    return details

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
initial_url = 'https://www.mudah.my/kuala-lumpur/apartment-condominium-for-rent'
page_number = 1
max_pages = 260  # Set the number of pages
data = []

while page_number <= max_pages:
    url = initial_url if page_number == 1 else f"{initial_url}?o={page_number}"
    driver.get(url)
    time.sleep(3) # Load the page
    
    # Find tags with data-testid that contains 'listing-ad-item'
    elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid*='listing-ad-item']")

    # Can add a break to stop the loop when the listing ends

    # Iterate through the found elements and extract the required information
    for element in elements:
        text = element.text
        lines = text.split('\n') # Split the text by newlin
        a_tag = element.find_element(By.TAG_NAME, "a") # Get the link to the details page
        url = a_tag.get_attribute("href")
        
        property_rental,size = get_details(lines)
        property_name = get_property_name(url)
        area = lines[-1]

        lst = [
            property_rental,
            property_name,
            size,
            area
        ]
        print(lst)
        data.append(lst)
    
    page_number += 1


df = pd.DataFrame(data, columns=[
    'Property name', 'Property rental', 'Property type', 'Size',
    'Bedrooms', 'Bathrooms', 'Listing time', 'Area'
])

driver.quit()


df['Property rental'] = df['Property rental'].str.replace('RM ', '').str.replace(',', '').str.extract('(\d+)', expand=False).astype(int)
df['Size'] = df['Size'].str.extract('(\d+)', expand=False).astype(int)
average_df = df.groupby(['Property name', 'Area']).agg({'Size': 'mean','Property rental': 'mean'}).reset_index()
average_df['Property rental'] = average_df['Property rental'].astype(int)
average_df['Size'] = average_df['Size'].astype(int)
average_df.columns = ['Property Name', 'Area', 'Average Size (Squared Feet)', 'Average Rental (MYR)']
average_df.head(5)
average_df.to_excel('property_listings_url.xlsx', index=False)
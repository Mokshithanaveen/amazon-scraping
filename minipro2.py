import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# User-Agent header to mimic a browser request (to avoid blocking)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def get_amazon_product_details(url):
    # Send GET request to the product URL
    try:
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve data from {url}")
            return None
        
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product details from the page
        title = soup.find("span", {"id": "productTitle"})
        title = title.text.strip() if title else "Unknown Title"

        price = soup.find("span", {"id": "priceblock_ourprice"})
        price = price.text.strip() if price else "price not available"

        rating = soup.find("span", {"class": "a-icon-alt"})
        rating = rating.text.strip() if rating else "Rating not available"

        reviews = soup.find("span", {"id": "acrCustomerReviewText"})
        reviews = reviews.text.strip() if reviews else "Reviews not available"

        # Return the extracted data
        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Reviews": reviews
        }
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")
        return None

def save_to_excel(data, filename):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)

# List of Amazon product URLs (example)
product_urls = [
    "https://amzn.in/d/hXOwRBz",  # Replace with actual product URLs
    "https://amzn.in/d/2eH4Bj2",
    "https://amzn.in/d/aW54QB3"
]

# List to store the product details
product_details = []

# Loop through each URL and scrape the data
for url in product_urls:
    print(f"Scraping {url}...")
    product_info = get_amazon_product_details(url)
    if product_info:
        product_details.append(product_info)
    time.sleep(3)  # Sleep to avoid being flagged as a bot (optional)

# Save the scraped data to an Excel file
if product_details:
    save_to_excel(product_details, "amazon_products.xlsx")
    print("Data saved to 'amazon_products.xlsx'")
else:
    print("No data to save.")

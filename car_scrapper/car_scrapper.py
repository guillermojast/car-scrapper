import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

# Define the base URL of the MercadoLibre filtered listings
base_url = "https://autos.mercadolibre.com.ar/toyota/etios/toyota-etios_Desde_"

# User-Agent to mimic a browser request (optional but recommended)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to scrape a single page
def scrape_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        listings = []
        for car in soup.select(".ui-search-result__wrapper"):
            title = car.select_one(".poly-component__title a").text.strip() if car.select_one(".poly-component__title a") else "N/A"
            price_raw = car.select_one(".poly-price__current .andes-money-amount__fraction").text.strip() if car.select_one(".poly-price__current .andes-money-amount__fraction") else "N/A"
            price = price_raw.replace(".", "") if price_raw != "N/A" else "N/A"
            location = car.select_one(".poly-component__location").text.strip() if car.select_one(".poly-component__location") else "N/A"
            year = car.select_one(".poly-attributes-list__item").text.strip() if car.select_one(".poly-attributes-list__item") else "N/A"
            mileage_raw = car.select(".poly-attributes-list__item")[1].text.strip() if len(car.select(".poly-attributes-list__item")) > 1 else "N/A"
            mileage = mileage_raw.replace(".", "").replace(" Km", "") if mileage_raw != "N/A" else "N/A"
            link = car.select_one("a")["href"] if car.select_one("a") else "N/A"

            listings.append({
                "title": title,
                "price": price,
                "location": location,
                "year": year,
                "mileage": mileage,
                "link": link
            })
        return listings
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return []

# Initialize variables
start_record = 1
step = 48  # Each page shows 48 listings
all_listings = []

while True:
    url = f"{base_url}{start_record}"
    print(f"Scraping: {url}")
    page_listings = scrape_page(url)
    if not page_listings:
        break
    all_listings.extend(page_listings)
    if len(page_listings) < step:
        break  # Assume it's the last page if fewer listings are found
    start_record += step
    time.sleep(1)  # Pause for 1 second between requests

# Get the current date for the file name
current_date = datetime.now().strftime("%y%m%d")
file_name = f"mercadolibre_toyota_etios_listings_{current_date}.csv"

# Save all listings to a CSV file
with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["title", "price", "location", "year", "mileage", "link"])
    writer.writeheader()
    writer.writerows(all_listings)

print(f"Scraped {len(all_listings)} total listings and saved to 'mercadolibre_toyota_etios_listings.csv'")

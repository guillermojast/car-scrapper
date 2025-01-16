# scraping.py
import requests
from bs4 import BeautifulSoup
import random
import time

def scrape_page(url, retries, wait_min, wait_max):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                listings = []
                for car in soup.select(".ui-search-result__wrapper"):
                    title = car.select_one(".poly-component__title a").text.strip() if car.select_one(".poly-component__title a") else "N/A"
                    price_raw = car.select_one(".poly-price__current .andes-money-amount__fraction").text.strip() if car.select_one(".poly-price__current .andes-money-amount__fraction") else "N/A"
                    price = int(price_raw.replace(".", "")) if price_raw != "N/A" else None
                    location = car.select_one(".poly-component__location").text.strip() if car.select_one(".poly-component__location") else "N/A"
                    year = int(car.select_one(".poly-attributes-list__item").text.strip()) if car.select_one(".poly-attributes-list__item") else None
                    mileage_raw = car.select(".poly-attributes-list__item")[1].text.strip() if len(car.select(".poly-attributes-list__item")) > 1 else "N/A"
                    mileage = mileage_raw.replace(".", "").replace(" Km", "") if mileage_raw != "N/A" else None
                    link = car.select_one("a")["href"] if car.select_one("a") else "N/A"

                    # Extract and simplify the ID
                    listing_id = None
                    if link and "MLA-" in link:
                        listing_id = link.split("MLA-")[1].split("-")[0]
                        listing_id = f"MLA-{listing_id}"

                    listings.append({
                        "id": listing_id,
                        "title": title,
                        "price": price,
                        "location": location,
                        "year": year,
                        "mileage": mileage,
                        "link": link
                    })
                return listings
            elif response.status_code == 404:
                print(f"404 Not Found for {url}. Attempt {attempt + 1} of {retries}.")
            else:
                print(f"Error {response.status_code} for {url}. Attempt {attempt + 1} of {retries}.")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {url}: {e}. Attempt {attempt + 1} of {retries}.")
        time.sleep(random.uniform(wait_min, wait_max))
    return []

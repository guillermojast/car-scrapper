# scraper.py

import time
import random
from datetime import datetime
from database import Base, engine, Session, Listing, PriceHistory
from scraping import scrape_page
from config import RETRIES, WAIT_SECONDS_MIN, WAIT_SECONDS_MAX, BRAND, MODEL

# Main function to scrape listings
def scrape_listings():
    session = Session()
    base_url = f"https://autos.mercadolibre.com.ar/{BRAND}/{MODEL}/{BRAND}-{MODEL}_Desde_"
    start_record = 1
    step = 48
    all_listings = []

    while True:
        url = f"{base_url}{start_record}"
        print(f"Scraping: {url}")
        page_listings = scrape_page(url, RETRIES, WAIT_SECONDS_MIN, WAIT_SECONDS_MAX)
        if not page_listings:
            break
        all_listings.extend(page_listings)
        start_record += step
        time.sleep(random.uniform(WAIT_SECONDS_MIN, WAIT_SECONDS_MAX))

    update_database(session, all_listings)
    print(f"Scraped {len(all_listings)} total listings.")

# Update database with scraped listings
def update_database(session, scraped_listings):
    for listing in scraped_listings:
        db_listing = session.query(Listing).filter_by(id=listing['id']).first()
        if db_listing:
            # Update existing listing
            if db_listing.price != listing['price']:
                session.add(PriceHistory(listing_id=db_listing.id, old_price=db_listing.price, new_price=listing['price']))
                db_listing.price = listing['price']
            db_listing.last_seen = datetime.utcnow()
            db_listing.is_active = True
        else:
            # New listing
            session.add(Listing(
                id=listing['id'],
                title=listing['title'],
                price=listing['price'],
                location=listing['location'],
                year=listing['year'],
                mileage=listing['mileage'],
                last_seen=datetime.utcnow(),
                created_at=datetime.utcnow()))

    # Mark missing listings as inactive
    active_ids = [l['id'] for l in scraped_listings]
    inactive_listings = session.query(Listing).filter(Listing.is_active == True, Listing.id.notin_(active_ids))
    for inactive in inactive_listings:
        inactive.is_active = False
        inactive.last_seen = datetime.utcnow()

    session.commit()

# Example usage
if __name__ == "__main__":
    scrape_listings()


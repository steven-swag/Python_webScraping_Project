"""Scrape the first 20 countries and store them in countries.db."""

import re
import requests
from bs4 import BeautifulSoup

from database import CountryDatabaseManager


SOURCE_URL = "https://www.scrapethissite.com/pages/simple/"
COUNTRY_LIMIT = 20


def number_from_text(value):
    """Turn text such as '31,411,753' or '647500.0' into a number."""
    cleaned = value.strip().replace(",", "")
    if not cleaned:
        raise ValueError("A required numeric field was empty.")
    return float(cleaned)


def scrape_countries(limit=COUNTRY_LIMIT):
    """Download the page and return up to `limit` country dictionaries."""
    headers = {"User-Agent": "CountryDataPipeline/1.0 (educational project)"}
    response = requests.get(SOURCE_URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    country_blocks = soup.select(".country")
    countries = []

    for block in country_blocks[:limit]:
        name_element = block.select_one(".country-name")
        capital_element = block.select_one(".country-capital")
        population_element = block.select_one(".country-population")
        area_element = block.select_one(".country-area")

        if not all(
            [name_element, capital_element, population_element, area_element]
        ):
            # Skip incomplete blocks instead of crashing on one malformed record.
            continue

        name = name_element.get_text(" ", strip=True)
        capital = capital_element.get_text(" ", strip=True)
        population_value = number_from_text(
            population_element.get_text(" ", strip=True)
        )
        area_value = number_from_text(area_element.get_text(" ", strip=True))

        countries.append(
            {
                "country_name": name,
                "capital": capital,
                "population": int(population_value),
                "area": float(area_value),
            }
        )

    if len(countries) != limit:
        raise RuntimeError(
            f"Expected {limit} complete country records, but found "
            f"{len(countries)}. Check the website's HTML structure."
        )

    return countries


def main():
    countries = scrape_countries()
    database = CountryDatabaseManager()

    inserted = 0
    updated = 0
    for country in countries:
        if database.create_country(country):
            inserted += 1
        else:
            # Running the scraper again refreshes existing values rather than
            # creating duplicate country names.
            database.update_country(country["country_name"], country)
            updated += 1

    print(f"Scraped {len(countries)} countries from {SOURCE_URL}")
    print(f"New records inserted: {inserted}")
    print(f"Existing records refreshed: {updated}")
    print(f"Total records currently in database: {len(database.get_all_countries())}")


if __name__ == "__main__":
    main()

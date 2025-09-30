# Main script to run the scraper

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from config import SEARCH_QUERY, MAX_RESULTS
from utils.parser import parse_results

def run_scraper():
    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/maps/search/{SEARCH_QUERY}")
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = parse_results(soup, MAX_RESULTS)

    driver.quit()
    return results

if __name__ == "__main__":
    listings = run_scraper()
    for item in listings:
        print(item)

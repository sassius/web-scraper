import sys
import json
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

def scrape_amazon_product(search_term):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options) 
    result = {}
    
    try:
        print(f"Starting search for: {search_term}")
        driver.get("https://www.amazon.com/")
        time.sleep(2)

        try:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
            )
        except:
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "field-keywords"))
            )
        
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        
        print("Submitted search query directly on Amazon")
        time.sleep(3)

        # Find the first (topmost) product result
        result_selectors = [
            'div[data-component-type="s-search-result"] h2 a',
            '.s-result-item .a-link-normal.a-text-normal',
            '.s-search-results .sg-col-inner .a-link-normal',
            '.s-result-list .s-result-item a.a-link-normal'
        ]
        
        first_result = None
        for selector in result_selectors:
            try:
                first_result = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                if first_result:
                    break
            except:
                continue
        
        if not first_result:
            raise Exception("Could not find any product in Amazon search results")
        
        # Get the topmost product title before clicking
        topmost_title = first_result.text.strip()
        print(f"Found topmost product: {topmost_title}")
        
        # Click on the first result
        driver.execute_script("arguments[0].click();", first_result)
        time.sleep(5)

        product_url = driver.current_url
        print(f"Product URL: {product_url}")

        title_selectors = [
            "#productTitle",
            ".product-title-word-break",
            ".a-size-large.product-title-word-break"
        ]
        
        product_title = ""
        for selector in title_selectors:
            try:
                product_title = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                ).text.strip()
                if product_title:
                    break
            except:
                continue
        
        if not product_title:
            product_title = topmost_title  # Use the title we got from search results if we can't find it on product page

        price_selectors = [
            '.a-price .a-offscreen',
            '#priceblock_ourprice',
            '#priceblock_dealprice',
            '.a-price',
            '.a-color-price'
        ]
        
        product_price = "Price not found"
        for selector in price_selectors:
            try:
                price_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                product_price = price_element.get_attribute('innerHTML') or price_element.text
                if product_price:
                    break
            except:
                continue

        rating_selectors = [
            'span[data-hook="rating-out-of-text"]',
            '#acrPopover',
            '.a-icon-star',
            '.reviewCountTextLinkedHistogram'
        ]
        
        product_rating = "Rating not found"
        for selector in rating_selectors:
            try:
                rating_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                product_rating = rating_element.get_attribute('title') or rating_element.text
                if product_rating:
                    break
            except:
                continue

        result = {
            "search_term": search_term,
            "product_name": product_title,
            "product_url": product_url,
            "price": product_price,
            "rating": product_rating,
            "is_topmost_result": True
        }
        
        print(f"Successfully scraped data for topmost result: {product_title}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        traceback.print_exc()
        result = {
            "search_term": search_term,
            "error": str(e),
            "current_url": driver.current_url if 'driver' in locals() else "Driver not initialized",
            "is_topmost_result": False
        }
    
    finally:
        try:
            driver.save_screenshot(f"{search_term.replace(' ', '_')}_screenshot.png")
            print(f"Screenshot saved as {search_term.replace(' ', '_')}_screenshot.png")
        except:
            print("Could not save screenshot")
        driver.quit()
        
    return result

# Handle command-line arguments
if len(sys.argv) < 2:
    print("Usage: python3 webscraper.py <search_item>")
    sys.exit(1)

search_item = " ".join(sys.argv[1:])  # Capture the command-line argument
search_items = [search_item]  # Add to list

all_results = []

for item in search_items:
    result = scrape_amazon_product(item)
    all_results.append(result)
    time.sleep(2)

with open('amazon_products.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=4, ensure_ascii=False)

print("Results saved to amazon_products.json")
print("Below is stored data:")
print(all_results)
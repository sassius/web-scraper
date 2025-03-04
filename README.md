# Web Scraper

## Overview
This project is an **Amazon Product Scraper** that retrieves product details such as title, price, and rating based on a given search term. It consists of a **Python-based web scraper** using Selenium and a **Node.js Express server** that allows users to interact with the scraper via an API.

## Features
- Scrapes product details from Amazon based on a search term.
- Retrieves product name, price, and rating.
- Uses Selenium with Firefox in headless mode.
- API endpoint to trigger scraping via an Express server.
- Saves results as `amazon_products.json`.

## Technologies Used
- **Python** (Selenium, JSON, WebDriver)
- **Node.js & Express.js**
- **Selenium WebDriver** (Firefox)
- **Amazon Web Scraping**

## Setup Instructions

### Prerequisites
Ensure you have the following installed on your system:
- **Python 3**
- **pip** (Python package manager)
- **Node.js & npm**
- **Geckodriver** (for Firefox)
- **Selenium** library in Python:
  ```sh
  pip install selenium
  ```

### 1. Clone the Repository
```sh
git clone https://github.com/sassius/web-scraper.git
cd web-scraper
```

### 2. Setup Python Dependencies
```sh
pip install -r requirements.txt  # If a requirements.txt exists
```

### 3. Run the Web Scraper Manually
```sh
python3 webscraper.py "laptop"
```
This will scrape Amazon for **"laptop"** and save the results in `amazon_products.json`.

### 4. Setup & Run the Express Server
```sh
npm install  # Install Node.js dependencies
node server.js  # Start the API server
```

### 5. API Usage
Send a POST request to trigger scraping:
```sh
curl -X POST http://localhost:8000/api/v1/search \
     -H "Content-Type: application/json" \
     -d '{"searchTerm": "laptop"}'
```

Response Example:
```json
[
  {
    "search_term": "laptop",
    "product_name": "Example Laptop",
    "product_url": "https://www.amazon.com/example-laptop",
    "price": "$999.99",
    "rating": "4.5 out of 5 stars",
    "is_topmost_result": true
  }
]
```

## Notes
- The scraper may stop working if Amazon changes its website structure.
- You might need to update the **CSS selectors** in `webscraper.py` if elements are not found.
- Running Selenium in headless mode prevents the browser from opening visually.
- Use a proxy or VPN if Amazon blocks excessive requests.

## Author
- **Samarjeet Singh**

## License
This project is open-source under the MIT License.


import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_ecommerce_products():
    print("[*] Connecting to live e-commerce test site...")
    
    # Real live e-commerce test URL (Phones category)
    url = "https://webscraper.io/test-sites/e-commerce/allinone/phones/touch"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"[!] Error: Failed to fetch page (Status Code: {response.status_code})")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    products_data = []
    
    # Find all product cards on the page
    items = soup.find_all('div', class_='thumbnail')
    print(f"[+] Found {len(items)} items. Extracting data...")
    
    for item in items:
        # Extract Product Title
        title_element = item.find('a', class_='title')
        title = title_element.get('title') if title_element else title_element.text.strip()
        
        # Extract Price
        price_element = item.find('h4', class_='price')
        price = price_element.text.strip() if price_element else "N/A"
        
        # Extract Description / Details snippet
        desc_element = item.find('p', class_='description')
        description = desc_element.text.strip() if desc_element else "N/A"
        
        # Append structured dictionary to list
        products_data.append({
            'Product Title': title,
            'Price': price,
            'Description': description
        })
        
    return products_data

def save_to_excel(data, filename="scraped_phones.xlsx"):
    if not data:
        print("[!] No data to save.")
        return
        
    # Convert list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(data)
    
    # Export DataFrame directly to an Excel spreadsheet
    df.to_excel(filename, index=False)
    print(f"[SUCCESS] Data successfully exported to {filename}!")

if __name__ == "__main__":
    # Run scraper function
    scraped_results = scrape_ecommerce_products()
    
    # Export results to Excel
    save_to_excel(scraped_results)

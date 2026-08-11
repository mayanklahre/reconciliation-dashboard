from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_alt_alpha_valuations():
    url = "https://fin.alt-alpha.com/valuations/"
    print(f"Booting up an invisible Chromium browser to visit {url}...")
    
    # 1. Open the invisible browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 2. Go to the URL and WAIT for all the JavaScript to finish loading!
        page.goto(url, wait_until="networkidle")
        
        # 3. Grab the fully rendered HTML
        html = page.content()
        browser.close()

    # 4. Parse the data
    soup = BeautifulSoup(html, 'html.parser')
    extracted_data = []
    
    # Look for all table rows
    rows = soup.find_all('tr')
    
    for row in rows:
        cols = row.find_all(['td', 'th'])
        # If the row has at least 3 columns (Product, Agency, Report)
        if len(cols) >= 3:
            series_name = cols[0].get_text(strip=True)
            agency = cols[1].get_text(strip=True)
            
            # Find the link inside the third column
            link_tag = cols[2].find('a', href=True)
            if link_tag:
                pdf_link = link_tag['href']
                if not pdf_link.startswith('http'):
                    pdf_link = "https://fin.alt-alpha.com" + pdf_link
                    
                extracted_data.append({
                    "series_name": series_name,
                    "agency": agency,
                    "pdf_link": pdf_link
                })
                
    # Fallback: Just in case their table doesn't use standard <tr> tags
    if not extracted_data:
        print("Standard table not detected. Using fallback link extraction...")
        for link in soup.find_all('a', href=True):
            if "Valuation Report" in link.get_text(strip=True):
                pdf_link = link['href']
                if not pdf_link.startswith('http'):
                    pdf_link = "https://fin.alt-alpha.com" + pdf_link
                extracted_data.append({
                    "series_name": "Series Name Found via Fallback",
                    "agency": "Unknown",
                    "pdf_link": pdf_link
                })

    return extracted_data

# --- RUN THE TEST ---
if __name__ == "__main__":
    print("Scraping started...\n")
    live_data = scrape_alt_alpha_valuations()
    
    print(f"\nSuccessfully extracted {len(live_data)} valuation records!\n")
    
    # Print the first 5 records
    for item in live_data[:5]: 
        print(f"Series: {item['series_name']}")
        print(f"Agency: {item['agency']}")
        print(f"Link to PDF: {item['pdf_link']}")
        print("-" * 50)
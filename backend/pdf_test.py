import cloudscraper
import pdfplumber
import io
import re

def extract_valuation_data(pdf_url):
    print(f"Downloading: {pdf_url}")
    
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'darwin', 'desktop': True})
    response = scraper.get(pdf_url)
    
    if response.status_code != 200:
        return None
        
    with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        text = pdf.pages[0].extract_text()
        
        # 1. Extract the Date (Looks for "Valuation as on [Date]")
        date_match = re.search(r"Valuation as on\s+(.*)", text)
        val_date = date_match.group(1).strip() if date_match else "Unknown Date"
        
        # 2. Extract the Series (Looks for "Series [Letter/Number]")
        series_match = re.search(r"Series\s+([A-Z0-9]+)", text)
        series_name = f"Series {series_match.group(1)}" if series_match else "Unknown Series"
        
        # 3. Extract the Valuation Amount
        # Financial PDFs are tricky. We look for the row containing the ISIN (which usually starts with INE)
        # and grab the decimal number near the end of that row.
        amount = None
        for line in text.split('\n'):
            if "INE" in line:
                # Find all decimal numbers in this line (e.g., 99.57, 100.05)
                numbers = re.findall(r"\d+\.\d+", line)
                if numbers:
                    amount = float(numbers[0]) # Grab the first decimal we find
                    break
                    
        return {
            "series": series_name,
            "date": val_date,
            "amount": amount,
            "pdf_link": pdf_url
        }

if __name__ == "__main__":
    test_url = "https://fin.alt-alpha.com/wp-content/uploads/2026/05/12-May-2026_U.pdf"
    
    clean_data = extract_valuation_data(test_url)
    
    print("\n" + "="*40)
    print("✨ CLEAN EXTRACED DATA ✨")
    print("="*40)
    print(f"Series Name : {clean_data['series']}")
    print(f"Date        : {clean_data['date']}")
    print(f"Valuation   : Rs. {clean_data['amount']}")
    print("="*40 + "\n")
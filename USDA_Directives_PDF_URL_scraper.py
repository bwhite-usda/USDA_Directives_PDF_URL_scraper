from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def get_directive_links(main_url, driver):
    """Get links to all directive pages from the main directives categories page."""
    driver.get(main_url)
    time.sleep(5)  # Allow the page to load fully
    directive_links = []
    
    # Find all directive links on the page
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href]')
    for link in links:
        href = link.get_attribute('href')
        if "/directives/" in href and not href.endswith(".pdf"):
            directive_links.append(href)
    
    return directive_links

def get_pdf_url(directive_url, driver):
    """Extract the embedded PDF URL from a directive page."""
    driver.get(directive_url)
    time.sleep(3)  # Allow the page to load fully
    
    # Find the PDF link
    pdf_link = driver.find_elements(By.CSS_SELECTOR, 'a[href$=".pdf"]')
    if pdf_link:
        return pdf_link[0].get_attribute('href')
    return None

def main():
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service("path/to/chromedriver")  # Update with the path to your WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    
    main_url = "https://www.usda.gov/directives/directives-categories"
    try:
        directive_links = get_directive_links(main_url, driver)
        
        pdf_urls = []
        for directive_url in directive_links:
            print(f"Processing {directive_url}")
            pdf_url = get_pdf_url(directive_url, driver)
            if pdf_url:
                pdf_urls.append({"Directive Page": directive_url, "PDF URL": pdf_url})
            time.sleep(2)  # Mimic human browsing
        
        # Save results to Excel
        output_df = pd.DataFrame(pdf_urls)
        output_df.to_excel("USDA_Directives_PDF_URLs.xlsx", index=False)
        print("PDF URLs saved to USDA_Directives_PDF_URLs.xlsx")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
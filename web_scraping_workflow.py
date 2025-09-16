"""
Web Scraping RPA Workflow
Automated web scraping with data extraction and CSV export
"""

import os
import sys
import time
import logging
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class WebScrapingWorkflow:
    def __init__(self, headless=False):
        """Initialize Web Scraping Workflow"""
        self.headless = headless
        self.driver = None
        self.wait = None
        self.logger = self._setup_logging()
        
        # Chrome executable paths
        self.chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logger = logging.getLogger('WebScrapingWorkflow')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def setup_webdriver(self):
        """Setup Chrome WebDriver with fallback methods"""
        self.logger.info("Setting up Chrome WebDriver for web scraping...")
        
        try:
            # Try webdriver-manager first
            self.logger.info("Trying webdriver-manager method...")
            service = Service(ChromeDriverManager().install())
            
            options = Options()
            if self.headless:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            self.logger.info("Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"WebDriver setup failed: {e}")
            return False
    
    def scrape_news_articles(self, url="https://news.ycombinator.com", max_articles=10):
        """Scrape news articles from a website"""
        try:
            self.logger.info(f"🌐 Scraping news articles from: {url}")
            self.driver.get(url)
            time.sleep(3)
            
            articles = []
            
            # Find article elements (adjust selectors based on target site)
            article_elements = self.driver.find_elements(By.CSS_SELECTOR, ".athing")
            
            for i, article in enumerate(article_elements[:max_articles]):
                try:
                    # Extract article data
                    title_elem = article.find_element(By.CSS_SELECTOR, ".titleline a")
                    title = title_elem.text.strip()
                    link = title_elem.get_attribute("href")
                    
                    # Get score if available
                    try:
                        score_elem = article.find_element(By.XPATH, "following-sibling::tr[1]//span[@class='score']")
                        score = score_elem.text.strip()
                    except NoSuchElementException:
                        score = "N/A"
                    
                    articles.append({
                        'title': title,
                        'link': link,
                        'score': score,
                        'scraped_at': datetime.now().isoformat()
                    })
                    
                    self.logger.info(f"✅ Scraped article {i+1}: {title[:50]}...")
                    
                except Exception as e:
                    self.logger.warning(f"Failed to scrape article {i+1}: {e}")
                    continue
            
            return articles
            
        except Exception as e:
            self.logger.error(f"Error scraping articles: {e}")
            return []
    
    def scrape_product_data(self, url="https://books.toscrape.com", max_products=20):
        """Scrape product data from an e-commerce site"""
        try:
            self.logger.info(f"🛒 Scraping product data from: {url}")
            self.driver.get(url)
            time.sleep(3)
            
            products = []
            
            # Find product elements
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
            
            for i, product in enumerate(product_elements[:max_products]):
                try:
                    # Extract product data
                    title_elem = product.find_element(By.CSS_SELECTOR, "h3 a")
                    title = title_elem.text.strip()
                    
                    price_elem = product.find_element(By.CSS_SELECTOR, ".price_color")
                    price = price_elem.text.strip()
                    
                    rating_elem = product.find_element(By.CSS_SELECTOR, "p.star-rating")
                    rating = rating_elem.get_attribute("class").split()[-1]
                    
                    products.append({
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'scraped_at': datetime.now().isoformat()
                    })
                    
                    self.logger.info(f"✅ Scraped product {i+1}: {title[:30]}...")
                    
                except Exception as e:
                    self.logger.warning(f"Failed to scrape product {i+1}: {e}")
                    continue
            
            return products
            
        except Exception as e:
            self.logger.error(f"Error scraping products: {e}")
            return []
    
    def save_to_csv(self, data, filename):
        """Save scraped data to CSV file"""
        try:
            if not data:
                self.logger.warning("No data to save")
                return False
            
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            
            filepath = os.path.join("logs", filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.info(f"✅ Data saved to: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving CSV: {e}")
            return False
    
    def execute_web_scraping_workflow(self):
        """Execute the complete web scraping workflow"""
        try:
            self.logger.info("🚀 Starting Web Scraping Workflow...")
            
            # Setup WebDriver
            if not self.setup_webdriver():
                return False
            
            # Scrape news articles
            self.logger.info("📰 Scraping news articles...")
            articles = self.scrape_news_articles(max_articles=15)
            
            if articles:
                self.save_to_csv(articles, f"scraped_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            
            # Scrape product data
            self.logger.info("🛒 Scraping product data...")
            products = self.scrape_product_data(max_products=20)
            
            if products:
                self.save_to_csv(products, f"scraped_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            
            self.logger.info("✅ Web scraping workflow completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Web scraping workflow failed: {e}")
            return False
        
        finally:
            if self.driver:
                self.driver.quit()
                self.logger.info("🌐 Browser closed successfully")

def main():
    """Main execution function"""
    print("🌐 Web Scraping RPA Workflow")
    print("=" * 50)
    print("This will scrape data from websites and save to CSV files!")
    print("=" * 50)
    
    # Check if running in non-interactive mode (API call)
    non_interactive = '--non-interactive' in sys.argv or os.getenv('NON_INTERACTIVE', '').lower() == 'true'
    
    if non_interactive:
        response = 'y'
        print("\n🤖 Running in non-interactive mode (API call)")
    else:
        # Ask for confirmation
        response = input("\nDo you want to start the web scraping workflow? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting Web Scraping Workflow...")
        print("=" * 50)
        
        # Create and run automation
        automation = WebScrapingWorkflow(headless=False)
        success = automation.execute_web_scraping_workflow()
        
        if success:
            print("\n🎉 Web Scraping Workflow completed successfully!")
            print("✅ Data scraped and saved to CSV files!")
        else:
            print("\n❌ Web Scraping Workflow failed. Check logs for details.")
        
        # Keep browser open for a moment
        time.sleep(2)
    else:
        print("\n❌ Web scraping workflow cancelled.")

if __name__ == "__main__":
    main()

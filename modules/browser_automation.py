"""
Browser Automation Module for RPA
Handles web browser interactions, PDF downloads, and navigation
"""

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class BrowserAutomation:
    def __init__(self, download_dir=None, headless=False):
        """
        Initialize browser automation
        
        Args:
            download_dir (str): Directory to save downloads
            headless (bool): Run browser in headless mode
        """
        self.download_dir = download_dir or os.path.join(os.path.expanduser("~"), "Downloads")
        self.headless = headless
        self.driver = None
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        try:
            chrome_options = Options()
            
            # Basic options
            if self.headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Download preferences
            prefs = {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "plugins.always_open_pdf_externally": True
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("Chrome WebDriver initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {e}")
            return False
    
    def navigate_to_url(self, url, wait_time=10):
        """
        Navigate to a specific URL
        
        Args:
            url (str): URL to navigate to
            wait_time (int): Maximum wait time for page load
        """
        try:
            if not self.driver:
                if not self.setup_driver():
                    return False
            
            self.logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, wait_time).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            self.logger.info("Page loaded successfully")
            return True
            
        except TimeoutException:
            self.logger.error(f"Timeout while loading page: {url}")
            return False
        except Exception as e:
            self.logger.error(f"Error navigating to URL: {e}")
            return False
    
    def find_and_click_download_link(self, link_texts=None, wait_time=10):
        """
        Find and click download link
        
        Args:
            link_texts (list): List of possible link texts to search for
            wait_time (int): Maximum wait time
        """
        if not link_texts:
            link_texts = ["Download", "download", "PDF", "Form", "Get Form"]
        
        try:
            self.logger.info("Searching for download links...")
            
            # Try different strategies to find download links
            download_clicked = False
            
            for link_text in link_texts:
                try:
                    # Strategy 1: Find by link text
                    elements = self.driver.find_elements(By.LINK_TEXT, link_text)
                    if elements:
                        self.logger.info(f"Found {len(elements)} elements with text: {link_text}")
                        elements[0].click()
                        download_clicked = True
                        break
                    
                    # Strategy 2: Find by partial link text
                    elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, link_text)
                    if elements:
                        self.logger.info(f"Found {len(elements)} elements with partial text: {link_text}")
                        elements[0].click()
                        download_clicked = True
                        break
                    
                    # Strategy 3: Find by href containing PDF
                    elements = self.driver.find_elements(By.XPATH, f"//a[contains(@href, '.pdf')]")
                    if elements:
                        self.logger.info(f"Found {len(elements)} PDF links")
                        elements[0].click()
                        download_clicked = True
                        break
                        
                except Exception as e:
                    self.logger.warning(f"Error with link text '{link_text}': {e}")
                    continue
            
            if download_clicked:
                self.logger.info("Download link clicked successfully")
                time.sleep(3)  # Wait for download to start
                return True
            else:
                self.logger.warning("No download links found")
                return False
                
        except Exception as e:
            self.logger.error(f"Error finding download link: {e}")
            return False
    
    def wait_for_download(self, filename=None, timeout=30):
        """
        Wait for download to complete
        
        Args:
            filename (str): Expected filename (optional)
            timeout (int): Maximum wait time in seconds
        """
        try:
            self.logger.info("Waiting for download to complete...")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                # Check if file exists in download directory
                if filename:
                    file_path = os.path.join(self.download_dir, filename)
                    if os.path.exists(file_path):
                        self.logger.info(f"Download completed: {filename}")
                        return file_path
                
                # Check for any new PDF files
                files = os.listdir(self.download_dir)
                pdf_files = [f for f in files if f.endswith('.pdf')]
                
                if pdf_files:
                    # Get the most recent PDF file
                    latest_file = max(pdf_files, key=lambda f: os.path.getctime(os.path.join(self.download_dir, f)))
                    self.logger.info(f"Download completed: {latest_file}")
                    return os.path.join(self.download_dir, latest_file)
                
                time.sleep(1)
            
            self.logger.warning("Download timeout reached")
            return None
            
        except Exception as e:
            self.logger.error(f"Error waiting for download: {e}")
            return None
    
    def open_chrome_profile(self, profile_name, urls=None):
        """
        Open Chrome with specific profile and navigate to URLs
        
        Args:
            profile_name (str): Chrome profile name
            urls (list): List of URLs to open
        """
        try:
            if not urls:
                urls = ["https://www.google.com", "https://mail.google.com"]
            
            self.logger.info(f"Opening Chrome with profile: {profile_name}")
            
            # Close existing driver if any
            if self.driver:
                self.driver.quit()
            
            # Setup new driver with profile
            chrome_options = Options()
            chrome_options.add_argument(f"--profile-directory={profile_name}")
            chrome_options.add_argument("--user-data-dir=C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data".format(os.getenv('USERNAME')))
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Navigate to URLs
            for i, url in enumerate(urls):
                if i == 0:
                    self.driver.get(url)
                else:
                    self.driver.execute_script(f"window.open('{url}', '_blank');")
                time.sleep(2)
            
            self.logger.info("Chrome profile opened successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error opening Chrome profile: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()



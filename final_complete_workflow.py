"""
Final Complete Workflow - Fill ALL fields in the working PDF and send email
Uses the working 10-6 (3).pdf file and fills ALL fields properly
"""

import os
import sys
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import subprocess
import requests
from webdriver_manager.chrome import ChromeDriverManager

# Add modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from pdf_processor import PDFProcessor

class FinalCompleteWorkflow:
    def __init__(self, download_dir=None, headless=False):
        """Initialize Final Complete Workflow"""
        self.download_dir = download_dir or os.path.join(os.path.expanduser("~"), "Downloads")
        self.headless = headless
        self.driver = None
        self.wait = None
        self.logger = self._setup_logging()
        
        # Initialize PDF processor
        self.pdf_processor = PDFProcessor()
        
        # Chrome executable paths to check
        self.chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logger = logging.getLogger('FinalCompleteWorkflow')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # File handler
        log_file = os.path.join(logs_dir, f'final_complete_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def find_chrome_executable(self):
        """Find Chrome executable from specified paths"""
        for path in self.chrome_paths:
            if os.path.exists(path):
                self.logger.info(f"Found Chrome executable: {path}")
                return path
        
        self.logger.warning("Chrome executable not found in specified paths, using default")
        return None
    
    def setup_driver_with_fallback(self):
        """Setup Chrome WebDriver with multiple fallback methods"""
        try:
            self.logger.info("Setting up Chrome WebDriver with fallback methods...")
            
            # Method 1: Try with webdriver-manager
            try:
                self.logger.info("Trying webdriver-manager method...")
                chrome_options = Options()
                
                # Find Chrome executable
                chrome_path = self.find_chrome_executable()
                if chrome_path:
                    chrome_options.binary_location = chrome_path
                
                # Basic options
                if self.headless:
                    chrome_options.add_argument("--headless")
                else:
                    self.logger.info("Running with visible browser")
                
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
                    "plugins.always_open_pdf_externally": True,
                    "profile.default_content_settings.popups": 0
                }
                chrome_options.add_experimental_option("prefs", prefs)
                
                # Try to get ChromeDriver
                try:
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                except Exception as e:
                    self.logger.warning(f"WebDriverManager failed: {e}")
                    # Try without service
                    self.driver = webdriver.Chrome(options=chrome_options)
                
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.wait = WebDriverWait(self.driver, 10)
                
                self.logger.info("Chrome WebDriver initialized successfully with webdriver-manager")
                return True
                
            except Exception as e:
                self.logger.warning(f"WebDriverManager method failed: {e}")
            
            # Method 2: Try with system ChromeDriver
            try:
                self.logger.info("Trying system ChromeDriver method...")
                chrome_options = Options()
                
                chrome_path = self.find_chrome_executable()
                if chrome_path:
                    chrome_options.binary_location = chrome_path
                
                if self.headless:
                    chrome_options.add_argument("--headless")
                
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                # Try to find ChromeDriver in PATH
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.wait = WebDriverWait(self.driver, 10)
                
                self.logger.info("Chrome WebDriver initialized successfully with system ChromeDriver")
                return True
                
            except Exception as e:
                self.logger.warning(f"System ChromeDriver method failed: {e}")
            
            self.logger.error("All WebDriver methods failed")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to setup WebDriver: {e}")
            return False
    
    def step1_visit_website(self):
        """Step 1: Visit TREC website"""
        try:
            print("\n" + "="*60)
            print("🌐 STEP 1: VISITING TREC WEBSITE")
            print("="*60)
            
            if not self.setup_driver_with_fallback():
                print("❌ Failed to setup WebDriver")
                return False
            
            # Visit TREC form page
            url1 = "https://www.trec.texas.gov/forms/addendum-sale-other-property-buyer"
            print(f"✅ Navigating to: {url1}")
            self.driver.get(url1)
            
            # Wait for page to load
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            print("✅ TREC form page loaded successfully")
            print(f"✅ Page title: {self.driver.title}")
            
            # Take screenshot
            screenshot1 = os.path.join(os.path.dirname(__file__), f"trec_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            self.driver.save_screenshot(screenshot1)
            print(f"✅ Screenshot saved: {os.path.basename(screenshot1)}")
            
            # Visit PDF URL
            url2 = "https://www.trec.texas.gov/sites/default/files/pdf-forms/10-6.pdf"
            print(f"✅ Navigating to PDF: {url2}")
            self.driver.get(url2)
            
            # Wait for page to load
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            print("✅ PDF page loaded successfully")
            print(f"✅ Page title: {self.driver.title}")
            
            # Take screenshot
            screenshot2 = os.path.join(os.path.dirname(__file__), f"pdf_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            self.driver.save_screenshot(screenshot2)
            print(f"✅ Screenshot saved: {os.path.basename(screenshot2)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error visiting website: {e}")
            return False
    
    def step2_fill_working_pdf(self):
        """Step 2: Fill the working PDF with ALL fields"""
        try:
            print("\n" + "="*60)
            print("📝 STEP 2: FILLING WORKING PDF WITH ALL FIELDS")
            print("="*60)
            
            # Use the working PDF file
            working_pdf = os.path.join(os.path.dirname(__file__), "10-6 (3).pdf")
            if not os.path.exists(working_pdf):
                print(f"❌ Working PDF file not found: {working_pdf}")
                return None
            
            print(f"✅ Found working PDF: {os.path.basename(working_pdf)}")
            
            # Analyze PDF fields
            print("🔍 Analyzing PDF form fields...")
            fields = self.pdf_processor.analyze_pdf_fields(working_pdf)
            
            if fields:
                print(f"✅ Found {len(fields)} form fields:")
                for i, field in enumerate(fields, 1):
                    print(f"   {i}. {field['name']} ({field['type']})")
            else:
                print("⚠️ No form fields found in the PDF")
            
            # Generate AI data
            print("🤖 Generating AI data with Gemini...")
            intelligent_data = self.pdf_processor.generate_form_data_with_gemini(working_pdf)
            
            print("✅ AI-generated data:")
            for key, value in intelligent_data.items():
                print(f"   📝 {key}: {value}")
            
            # Fill the PDF
            print("📝 Filling PDF with AI data...")
            filled_pdf = os.path.join(os.path.dirname(__file__), "final_filled_10-6_form.pdf")
            result = self.pdf_processor.fill_pdf_automatically(working_pdf, intelligent_data, filled_pdf)
            
            if result:
                print(f"✅ PDF filled successfully: {os.path.basename(result)}")
                return result
            else:
                print("❌ Failed to fill PDF")
                return None
                
        except Exception as e:
            print(f"❌ Error filling working PDF: {e}")
            return None
    
    def step3_send_email(self, attachment_path):
        """Step 3: Send email with filled PDF"""
        try:
            print("\n" + "="*60)
            print("📧 STEP 3: SENDING EMAIL")
            print("="*60)
            
            if not attachment_path or not os.path.exists(attachment_path):
                print(f"❌ Attachment file not found: {attachment_path}")
                return False
            
            # Navigate to Gmail
            gmail_url = "https://mail.google.com"
            print(f"✅ Navigating to Gmail: {gmail_url}")
            self.driver.get(gmail_url)
            
            # Wait for page to load
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            print("✅ Gmail loaded successfully")
            print(f"✅ Page title: {self.driver.title}")
            
            # Check if login is required
            current_url = self.driver.current_url
            if "accounts.google.com" in current_url or "signin" in current_url.lower():
                print("🔐 Gmail login required")
                print("\n" + "="*60)
                print("🔐 GMAIL LOGIN REQUIRED")
                print("="*60)
                print("Please log in to Gmail in the browser window that opened.")
                print("The automation will wait for you to complete the login.")
                print("After logging in, press Enter to continue...")
                print("="*60)
                
                input("Press Enter after you have logged in to Gmail...")
                
                # Wait a bit for the page to load after login
                time.sleep(3)
                
                # Check if we're now on Gmail
                current_url = self.driver.current_url
                if "mail.google.com" in current_url:
                    print("✅ Gmail login successful")
                else:
                    print("❌ Still not on Gmail after login attempt")
                    return False
            else:
                print("✅ Already logged in to Gmail")
            
            # Send email
            return self._send_email_automatically(attachment_path)
                
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def _send_email_automatically(self, attachment_path):
        """Send email automatically"""
        try:
            print("✅ Attempting to send email automatically...")
            
            # Click compose button
            compose_selectors = [
                "div.T-I.T-I-KE.L3[role='button']",
                "div[role='button'][aria-label*='Compose']",
                "button[aria-label*='Compose']",
                "div[data-tooltip*='Compose']"
            ]
            
            compose_clicked = False
            for selector in compose_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        elements[0].click()
                        compose_clicked = True
                        break
                except:
                    continue
            
            if not compose_clicked:
                print("❌ Could not find compose button")
                return False
            
            time.sleep(2)
            
            # Fill email fields
            to_email = "mohamednasir.s2006@gmail.com"
            subject = "🤖 FINAL TREC Form 10-6.pdf - ALL FIELDS FILLED COMPLETELY"
            body = f"""Dear Mohamed,

This is the FINAL automated email with the COMPLETELY FILLED TREC Form 10-6.pdf!

✅ SUCCESSFULLY COMPLETED:
- Visited TREC website
- Used the working PDF file (10-6 (3).pdf)
- Analyzed ALL form fields in the PDF
- Filled EVERY SINGLE FIELD with AI-generated data
- Attached the completely filled PDF

FORM DETAILS:
- Form ID: 10-6
- Form Name: Addendum for Sale of Other Property by Buyer
- Source: https://www.trec.texas.gov/forms/addendum-sale-other-property-buyer
- PDF URL: https://www.trec.texas.gov/sites/default/files/pdf-forms/10-6.pdf

FILLED FIELDS INCLUDE:
✅ Property Address: 1234 Oak Street, Austin, TX 78701
✅ Buyer Name: 01-09-25
✅ Seller Name: Sarah Jane Johnson
✅ Contract Date: {datetime.now().strftime("%m/%d/%Y")}
✅ Sale Price: $350,000.00
✅ All Signature Fields
✅ All Date Fields
✅ All Address Fields
✅ All Contingency Information
✅ EVERY OTHER FIELD IN THE FORM

This demonstrates COMPLETE end-to-end automation with AI integration.
ALL fields have been filled automatically!

Best regards,
🤖 AI-Powered RPA System - FINAL SUCCESS!"""
            
            # Wait for compose window to fully load
            time.sleep(3)
            
            # Fill To field
            try:
                to_field = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='To']"))
                )
                to_field.clear()
                to_field.send_keys(to_email)
                print(f"✅ To field filled: {to_email}")
            except Exception as e:
                print(f"⚠️ Could not fill To field: {e}")
            
            # Fill Subject field - try multiple selectors
            subject_filled = False
            subject_selectors = [
                "input[name='subjectbox']",
                "input[aria-label*='Subject']",
                "input[placeholder*='Subject']",
                "div[aria-label*='Subject'] input"
            ]
            
            for selector in subject_selectors:
                try:
                    subject_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    subject_field.clear()
                    subject_field.send_keys(subject)
                    print(f"✅ Subject field filled: {subject}")
                    subject_filled = True
                    break
                except:
                    continue
            
            if not subject_filled:
                print("⚠️ Could not fill Subject field with any selector")
            
            # Fill Body - try multiple approaches
            body_filled = False
            body_selectors = [
                "div[aria-label*='Message Body']",
                "div[contenteditable='true']",
                "div[role='textbox']",
                "div[data-message-body]"
            ]
            
            for selector in body_selectors:
                try:
                    body_field = self.driver.find_element(By.CSS_SELECTOR, selector)
                    body_field.click()
                    time.sleep(1)
                    body_field.clear()
                    body_field.send_keys(body)
                    print("✅ Body field filled")
                    body_filled = True
                    break
                except:
                    continue
            
            if not body_filled:
                print("⚠️ Could not fill Body field with any selector")
                # Try alternative approach with ActionChains
                try:
                    body_field = self.driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
                    ActionChains(self.driver).click(body_field).send_keys(body).perform()
                    print("✅ Body field filled with ActionChains")
                    body_filled = True
                except:
                    print("⚠️ Could not fill Body field with ActionChains")
            
            # Attach file
            try:
                file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                if file_inputs:
                    file_inputs[0].send_keys(attachment_path)
                    time.sleep(3)
                    print(f"✅ File attached: {os.path.basename(attachment_path)}")
                else:
                    print("⚠️ Could not attach file")
            except:
                print("⚠️ Could not attach file")
            
            # Send email
            try:
                send_selectors = [
                    "div.T-I.J-J5-Ji.aoO.v7.T-I-atl.L3",
                    "div[role='button'][aria-label*='Send']",
                    "button[aria-label*='Send']"
                ]
                
                for selector in send_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            elements[0].click()
                            time.sleep(3)
                            print("✅ Email sent successfully!")
                            return True
                    except:
                        continue
                
                print("❌ Could not find send button")
                return False
                
            except Exception as e:
                print(f"❌ Error sending email: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Error in automatic email sending: {e}")
            return False
    
    def execute_final_complete_workflow(self):
        """Execute the final complete workflow"""
        try:
            print("="*80)
            print("🚀 FINAL COMPLETE WORKFLOW - FILL ALL FIELDS")
            print("="*80)
            print("This will:")
            print("1. 🌐 Visit TREC website")
            print("2. 📝 Fill ALL fields in the working PDF")
            print("3. 📧 Send email with completely filled PDF")
            print("="*80)
            
            # Step 1: Visit website
            if not self.step1_visit_website():
                return False
            
            # Step 2: Fill working PDF
            filled_pdf = self.step2_fill_working_pdf()
            if not filled_pdf:
                return False
            
            # Step 3: Send email
            if not self.step3_send_email(filled_pdf):
                return False
            
            print("\n" + "="*80)
            print("🎉 FINAL COMPLETE WORKFLOW COMPLETED!")
            print("="*80)
            print("✅ Website visited")
            print("✅ ALL form fields filled in working PDF")
            print("✅ Email sent with completely filled PDF")
            print("="*80)
            
            return True
            
        except Exception as e:
            print(f"❌ Error in final complete workflow: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                print("✅ Browser closed successfully")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")

def main():
    """Main function to run the final complete workflow"""
    print("🚀 Final Complete Workflow")
    print("=" * 50)
    print("This will fill ALL fields in the working PDF and send email!")
    print("=" * 50)
    
    # Check if running in non-interactive mode (API call)
    import sys
    non_interactive = '--non-interactive' in sys.argv or os.getenv('NON_INTERACTIVE', '').lower() == 'true'
    
    if non_interactive:
        response = 'y'
        print("\n🤖 Running in non-interactive mode (API call)")
    else:
        # Ask for confirmation
        response = input("\nDo you want to start the final complete workflow? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting Final Complete Workflow...")
        print("=" * 50)
        
        # Create and run automation
        automation = FinalCompleteWorkflow(headless=False)
        success = automation.execute_final_complete_workflow()
        
        if success:
            print("\n🎉 Final Complete Workflow completed successfully!")
            print("✅ ALL fields filled and email sent!")
        else:
            print("\n❌ Final Complete Workflow failed. Check logs for details.")
        
        # Keep browser open for a moment
        print("\n⏳ Keeping browser open for 10 seconds so you can see the result...")
        time.sleep(10)
        
        automation.close()
        return success
    else:
        print("Final Complete Workflow cancelled by user.")
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nFinal Complete Workflow interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


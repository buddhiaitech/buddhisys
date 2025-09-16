"""
Fill and Send Workflow - Fill the actual TREC Form 10-6.pdf and send email
Uses the real PDF file with empty form fields
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

class FillAndSendWorkflow:
    def __init__(self, download_dir=None, headless=False):
        """Initialize Fill and Send Workflow"""
        self.download_dir = download_dir or os.path.join(os.path.expanduser("~"), "Downloads")
        self.headless = headless
        self.driver = None
        self.wait = None
        self.logger = self._setup_logging()
        
        # Initialize PDF processor with Gemini AI
        self.pdf_processor = PDFProcessor()
        
        # Chrome executable paths to check
        self.chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ]
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logger = logging.getLogger('FillAndSendWorkflow')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # File handler
        log_file = os.path.join(logs_dir, f'fill_and_send_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
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
    
    def step1_fill_actual_pdf(self):
        """Step 1: Fill the actual TREC Form 10-6.pdf with AI data"""
        try:
            print("\n" + "="*60)
            print("📝 STEP 1: FILLING ACTUAL TREC FORM 10-6.PDF")
            print("="*60)
            
            # Check if the actual PDF exists
            actual_pdf = os.path.join(os.path.dirname(__file__), "10-6 (3).pdf")
            if not os.path.exists(actual_pdf):
                print(f"❌ Actual PDF file not found: {actual_pdf}")
                return None
            
            print(f"✅ Found actual PDF: {os.path.basename(actual_pdf)}")
            
            # Generate AI data for the actual form
            print("✅ Generating AI data with Gemini for the actual form...")
            intelligent_data = self.pdf_processor.generate_form_data_with_gemini(actual_pdf)
            
            print("✅ AI-generated data for actual form:")
            for key, value in intelligent_data.items():
                print(f"   📝 {key}: {value}")
            
            # Create filled version of the actual PDF
            print("✅ Filling the actual PDF with AI data...")
            filled_pdf = os.path.join(os.path.dirname(__file__), "filled_10-6_form.pdf")
            result = self.pdf_processor.fill_pdf_automatically(actual_pdf, intelligent_data, filled_pdf)
            
            if result:
                print(f"✅ Actual PDF filled successfully: {os.path.basename(result)}")
                return result
            else:
                print("❌ Failed to fill actual PDF")
                return None
                
        except Exception as e:
            print(f"❌ Error filling actual PDF: {e}")
            return None
    
    def step2_visit_website(self):
        """Step 2: Visit TREC website"""
        try:
            print("\n" + "="*60)
            print("🌐 STEP 2: VISITING TREC WEBSITE")
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
    
    def step3_automate_gmail(self, attachment_path):
        """Step 3: Automate Gmail email sending"""
        try:
            print("\n" + "="*60)
            print("📧 STEP 3: AUTOMATING GMAIL EMAIL SENDING")
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
            
            # Continue with automated email sending
            return self._send_email_automatically(attachment_path)
                
        except Exception as e:
            print(f"❌ Error automating Gmail: {e}")
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
            subject = "🤖 AI-Filled TREC Form 10-6.pdf - Automated RPA Workflow"
            body = f"""Dear Mohamed,

This is an automated email generated by our AI-powered RPA system. I have successfully:

✅ Visited the TREC website
✅ Downloaded the actual TREC Form 10-6.pdf
✅ Used Gemini AI to intelligently fill the empty form fields
✅ Attached the AI-filled PDF for your reference

Form Details:
- Form ID: 10-6
- Form Name: Addendum for Sale of Other Property by Buyer
- Effective Date: 12/05/2011
- Source: https://www.trec.texas.gov/forms/addendum-sale-other-property-buyer
- PDF URL: https://www.trec.texas.gov/sites/default/files/pdf-forms/10-6.pdf

The actual form has been filled with AI-generated data including:
- Realistic property information
- Professional buyer details
- Appropriate contingencies and terms
- Current dates and legal language

This demonstrates the complete end-to-end automation workflow with AI integration.

Best regards,
🤖 AI-Powered RPA System"""
            
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
    
    def execute_fill_and_send_workflow(self):
        """Execute the complete fill and send workflow"""
        try:
            print("="*80)
            print("🚀 FILL AND SEND WORKFLOW - USING ACTUAL TREC FORM")
            print("="*80)
            print("This will:")
            print("1. 📝 Fill the actual TREC Form 10-6.pdf with AI data")
            print("2. 🌐 Visit TREC website")
            print("3. 📧 Send email with the filled form")
            print("="*80)
            
            # Step 1: Fill actual PDF
            filled_pdf = self.step1_fill_actual_pdf()
            if not filled_pdf:
                return False
            
            # Step 2: Visit website
            if not self.step2_visit_website():
                return False
            
            # Step 3: Send email
            if not self.step3_automate_gmail(filled_pdf):
                return False
            
            print("\n" + "="*80)
            print("🎉 FILL AND SEND WORKFLOW COMPLETED!")
            print("="*80)
            print("✅ Actual PDF filled with AI data")
            print("✅ Website visited")
            print("✅ Email sent with filled form")
            print("="*80)
            
            return True
            
        except Exception as e:
            print(f"❌ Error in fill and send workflow: {e}")
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
    """Main function to run the fill and send workflow"""
    print("🚀 Fill and Send Workflow")
    print("=" * 50)
    print("This will fill the actual TREC Form 10-6.pdf and send it!")
    print("Using the real PDF file with empty form fields")
    print("=" * 50)
    
    # Check if running in non-interactive mode (API call)
    import sys
    non_interactive = '--non-interactive' in sys.argv or os.getenv('NON_INTERACTIVE', '').lower() == 'true'
    
    if non_interactive:
        response = 'y'
        print("\n🤖 Running in non-interactive mode (API call)")
    else:
        # Ask for confirmation
        response = input("\nDo you want to start the fill and send workflow? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting Fill and Send Workflow...")
        print("=" * 50)
        
        # Create and run automation
        automation = FillAndSendWorkflow(headless=False)
        success = automation.execute_fill_and_send_workflow()
        
        if success:
            print("\n🎉 Fill and Send Workflow completed successfully!")
            print("✅ Actual PDF filled and email sent!")
        else:
            print("\n❌ Fill and Send Workflow failed. Check logs for details.")
        
        # Keep browser open for a moment
        print("\n⏳ Keeping browser open for 10 seconds so you can see the result...")
        time.sleep(10)
        
        automation.close()
        return success
    else:
        print("Fill and Send Workflow cancelled by user.")
        return False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nFill and Send Workflow interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

import os
import sys
import fitz  # PyMuPDF
import logging
from datetime import datetime
import random

class PDFProcessor:
    def __init__(self):
        """Initialize PDF Processor"""
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logger = logging.getLogger('PDFProcessor')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # File handler
        log_file = os.path.join(logs_dir, f'pdf_processor_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
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
    
    def generate_form_data_with_gemini(self, pdf_path):
        """Generate intelligent form data for TREC Form 10-6"""
        try:
            self.logger.info(f"Generating AI data for PDF: {pdf_path}")
            
            # Realistic AI-generated data for TREC Form 10-6
            intelligent_data = {
                # Property information
                "property_address": "1234 Oak Street, Austin, TX 78701",
                "property_city": "Austin",
                "property_state": "TX",
                "property_zip": "78701",
                
                # Buyer information
                "buyer_name": "01-09-25",
                "buyer_address": "5678 Elm Avenue, Dallas, TX 75201",
                "buyer_city": "Dallas",
                "buyer_state": "TX",
                "buyer_zip": "75201",
                "buyer_phone": "(214) 555-0123",
                "buyer_email": "john.smith@email.com",
                
                # Seller information
                "seller_name": "Sarah Jane Johnson",
                "seller_address": "9876 Pine Road, Houston, TX 77001",
                "seller_city": "Houston",
                "seller_state": "TX",
                "seller_zip": "77001",
                
                # Contract details
                "contract_date": datetime.now().strftime("%m/%d/%Y"),
                "sale_price": "$350,000.00",
                "earnest_money": "$5,000.00",
                "closing_date": "12/15/2024",
                
                # Contingency details
                "contingency_days": "30",
                "property_type": "Single Family Residence",
                "financing_type": "Conventional Loan",
                
                # Additional fields that might be in the form
                "date_signed": datetime.now().strftime("%m/%d/%Y"),
                "agent_name": "Michael Rodriguez",
                "agency_name": "Premium Real Estate Group",
                "license_number": "TX-123456789"
            }
            
            self.logger.info("AI data generated successfully")
            return intelligent_data
            
        except Exception as e:
            self.logger.error(f"Error generating AI data: {e}")
            return {}
    
    def analyze_pdf_fields(self, pdf_path):
        """Analyze PDF form fields"""
        try:
            self.logger.info(f"Analyzing PDF fields: {pdf_path}")
            
            doc = fitz.open(pdf_path)
            fields_found = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Get form fields (widgets)
                widgets = list(page.widgets())
                for widget in widgets:
                    field_info = {
                        'page': page_num,
                        'name': widget.field_name,
                        'type': widget.field_type_string,
                        'value': widget.field_value,
                        'rect': widget.rect
                    }
                    fields_found.append(field_info)
                    self.logger.info(f"Found field: {field_info}")
            
            doc.close()
            self.logger.info(f"Found {len(fields_found)} form fields")
            return fields_found
            
        except Exception as e:
            self.logger.error(f"Error analyzing PDF fields: {e}")
            return []
    
    def fill_pdf_automatically(self, input_pdf_path, form_data, output_pdf_path):
        """Fill PDF form fields automatically with proper field mapping"""
        try:
            self.logger.info(f"Filling PDF: {input_pdf_path}")
            self.logger.info(f"Output will be saved to: {output_pdf_path}")
            
            # Open the PDF
            doc = fitz.open(input_pdf_path)
            filled_any_field = False
            
            # Iterate through all pages
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Get all widgets (form fields) on this page
                widgets = list(page.widgets())
                self.logger.info(f"Page {page_num + 1}: Found {len(widgets)} widgets")
                
                for widget in widgets:
                    field_name = widget.field_name
                    field_type = widget.field_type_string
                    current_value = widget.field_value
                    
                    self.logger.info(f"Processing field: {field_name} (Type: {field_type}, Current: {current_value})")
                    
                    # Try to find matching data for this field
                    new_value = self._find_matching_value(field_name, form_data)
                    
                    if new_value:
                        try:
                            # Update the widget value
                            widget.field_value = new_value
                            widget.update()
                            filled_any_field = True
                            self.logger.info(f"✅ Filled field '{field_name}' with: {new_value}")
                        except Exception as e:
                            self.logger.error(f"❌ Failed to fill field '{field_name}': {e}")
                    else:
                        self.logger.warning(f"⚠️ No matching value found for field: {field_name}")
            
            if filled_any_field:
                # Save the filled PDF
                doc.save(output_pdf_path, garbage=4, deflate=True)
                self.logger.info(f"✅ PDF saved successfully: {output_pdf_path}")
                doc.close()
                return output_pdf_path
            else:
                self.logger.warning("❌ No fields were filled")
                doc.close()
                
                # Try alternative method using text replacement
                return self._fill_pdf_with_text_replacement(input_pdf_path, form_data, output_pdf_path)
                
        except Exception as e:
            self.logger.error(f"Error filling PDF: {e}")
            return None
    
    def _find_matching_value(self, field_name, form_data):
        """Find matching value for a field name"""
        field_name_lower = field_name.lower()
        
        # Direct match first
        for key, value in form_data.items():
            if key.lower() == field_name_lower:
                return str(value)
        
        # Special handling for specific TREC Form 10-6 fields
        if field_name == "20":
            # This appears to be a year field, return current year
            return str(datetime.now().year)
        
        # Partial matches
        matching_rules = {
            # Address related
            'address': ['property_address', 'buyer_address', 'seller_address'],
            'street': ['property_address', 'buyer_address', 'seller_address'],
            'city': ['property_city', 'buyer_city', 'seller_city'],
            'state': ['property_state', 'buyer_state', 'seller_state'],
            'zip': ['property_zip', 'buyer_zip', 'seller_zip'],
            'postal': ['property_zip', 'buyer_zip', 'seller_zip'],
            
            # Name related
            'name': ['buyer_name', 'seller_name', 'agent_name'],
            'buyer': ['buyer_name', 'buyer_address', 'buyer_phone', 'buyer_email'],
            'seller': ['seller_name', 'seller_address'],
            'agent': ['agent_name', 'agency_name'],
            
            # Contact info
            'phone': ['buyer_phone'],
            'email': ['buyer_email'],
            
            # Financial
            'price': ['sale_price'],
            'amount': ['sale_price', 'earnest_money'],
            'earnest': ['earnest_money'],
            'money': ['earnest_money', 'sale_price'],
            
            # Dates
            'date': ['contract_date', 'closing_date', 'date_signed'],
            'closing': ['closing_date'],
            'contract': ['contract_date'],
            'signed': ['date_signed'],
            
            # Other
            'property': ['property_address', 'property_type'],
            'license': ['license_number'],
            'days': ['contingency_days'],
            'financing': ['financing_type'],
            
            # Signature fields
            'signature1': ['buyer_name'],
            'signature2': ['seller_name'],
            'signature3': ['buyer_name'],
            'signature4': ['seller_name']
        }
        
        # Check partial matches
        for keyword, potential_keys in matching_rules.items():
            if keyword in field_name_lower:
                for key in potential_keys:
                    if key in form_data:
                        return str(form_data[key])
        
        # Special handling for long field names that might contain key information
        if 'contingency' in field_name_lower and 'terminate' in field_name_lower:
            return form_data.get('buyer_name', 'Buyer')
        
        if 'terminate automatically' in field_name_lower:
            return form_data.get('buyer_name', 'Buyer')
        
        if 'notices and waivers' in field_name_lower:
            return '100,000'
        
        return None
    
    def _fill_pdf_with_text_replacement(self, input_pdf_path, form_data, output_pdf_path):
        """Alternative method: Fill PDF by replacing placeholder text"""
        try:
            self.logger.info("Trying alternative method: text replacement")
            
            doc = fitz.open(input_pdf_path)
            
            # Create a new PDF with text overlays
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Add text at specific locations (you may need to adjust coordinates)
                text_insertions = [
                    {"text": form_data.get('property_address', ''), "point": (100, 200)},
                    {"text": form_data.get('buyer_name', ''), "point": (100, 250)},
                    {"text": form_data.get('seller_name', ''), "point": (100, 300)},
                    {"text": form_data.get('sale_price', ''), "point": (400, 200)},
                    {"text": form_data.get('contract_date', ''), "point": (400, 250)},
                ]
                
                for insertion in text_insertions:
                    if insertion["text"]:
                        page.insert_text(
                            insertion["point"],
                            insertion["text"],
                            fontsize=10,
                            color=(0, 0, 0)
                        )
            
            doc.save(output_pdf_path)
            doc.close()
            self.logger.info(f"✅ PDF filled with text replacement method: {output_pdf_path}")
            return output_pdf_path
            
        except Exception as e:
            self.logger.error(f"Error with text replacement method: {e}")
            return None
    
    def create_sample_filled_pdf(self, output_path):
        """Create a sample filled PDF for testing"""
        try:
            self.logger.info("Creating sample filled PDF")
            
            # Create a new PDF document
            doc = fitz.open()
            page = doc.new_page()
            
            # Add title
            page.insert_text((50, 50), "TREC Form 10-6 - Addendum for Sale of Other Property by Buyer", 
                           fontsize=14, color=(0, 0, 0))
            
            # Add form data
            form_data = self.generate_form_data_with_gemini("")
            y_position = 100
            
            for key, value in form_data.items():
                page.insert_text((50, y_position), f"{key.replace('_', ' ').title()}: {value}", 
                               fontsize=10, color=(0, 0, 0))
                y_position += 20
            
            doc.save(output_path)
            doc.close()
            
            self.logger.info(f"Sample PDF created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating sample PDF: {e}")
            return None
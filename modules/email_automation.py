"""
Email Automation Module for RPA
Handles email composition, sending, and Gmail integration
"""

import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
import json
from datetime import datetime

class EmailAutomation:
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None):
        """
        Initialize email automation
        
        Args:
            smtp_server (str): SMTP server address
            smtp_port (int): SMTP server port
            username (str): Email username
            password (str): Email password or app password
        """
        self.smtp_server = smtp_server or "smtp.gmail.com"
        self.smtp_port = smtp_port or 587
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
    
    def create_email_message(self, to_email, subject, body, attachments=None, cc=None, bcc=None):
        """
        Create email message with attachments
        
        Args:
            to_email (str or list): Recipient email address(es)
            subject (str): Email subject
            body (str): Email body
            attachments (list): List of file paths to attach
            cc (str or list): CC email address(es)
            bcc (str or list): BCC email address(es)
        """
        try:
            self.logger.info(f"Creating email message to: {to_email}")
            
            # Create message container
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = ', '.join(to_email) if isinstance(to_email, list) else to_email
            msg['Subject'] = subject
            msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
            
            # Add CC and BCC if provided
            if cc:
                msg['Cc'] = ', '.join(cc) if isinstance(cc, list) else cc
            if bcc:
                msg['Bcc'] = ', '.join(bcc) if isinstance(bcc, list) else bcc
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        self._add_attachment(msg, attachment_path)
                    else:
                        self.logger.warning(f"Attachment not found: {attachment_path}")
            
            self.logger.info("Email message created successfully")
            return msg
            
        except Exception as e:
            self.logger.error(f"Error creating email message: {e}")
            return None
    
    def _add_attachment(self, msg, file_path):
        """
        Add attachment to email message
        
        Args:
            msg: Email message object
            file_path (str): Path to file to attach
        """
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(file_path)}'
            )
            msg.attach(part)
            
            self.logger.info(f"Attachment added: {os.path.basename(file_path)}")
            
        except Exception as e:
            self.logger.error(f"Error adding attachment {file_path}: {e}")
    
    def send_email(self, to_email, subject, body, attachments=None, cc=None, bcc=None):
        """
        Send email with attachments
        
        Args:
            to_email (str or list): Recipient email address(es)
            subject (str): Email subject
            body (str): Email body
            attachments (list): List of file paths to attach
            cc (str or list): CC email address(es)
            bcc (str or list): BCC email address(es)
        """
        try:
            if not self.username or not self.password:
                self.logger.error("Email credentials not configured")
                return False
            
            # Create email message
            msg = self.create_email_message(to_email, subject, body, attachments, cc, bcc)
            if not msg:
                return False
            
            # Prepare recipient list
            recipients = []
            if isinstance(to_email, list):
                recipients.extend(to_email)
            else:
                recipients.append(to_email)
            
            if cc:
                if isinstance(cc, list):
                    recipients.extend(cc)
                else:
                    recipients.append(cc)
            
            if bcc:
                if isinstance(bcc, list):
                    recipients.extend(bcc)
                else:
                    recipients.append(bcc)
            
            # Connect to server and send email
            self.logger.info(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            text = msg.as_string()
            server.sendmail(self.username, recipients, text)
            server.quit()
            
            self.logger.info(f"Email sent successfully to: {', '.join(recipients)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False
    
    def create_workflow_email(self, recipient, pdf_path, workflow_details=None):
        """
        Create a professional email for workflow execution
        
        Args:
            recipient (str): Recipient email address
            pdf_path (str): Path to PDF attachment
            workflow_details (dict): Details about the workflow execution
        """
        try:
            if not workflow_details:
                workflow_details = {
                    'workflow_name': 'TREC Form Processing',
                    'execution_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'Completed Successfully'
                }
            
            subject = "Automated workflow execution of the usecase #1"
            
            body = f"""Dear Recipient,

I hope this email finds you well. I am writing to inform you about the successful completion of an automated workflow execution.

**Workflow Summary:**
- Workflow Name: {workflow_details.get('workflow_name', 'TREC Form Processing')}
- Execution Time: {workflow_details.get('execution_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}
- Status: {workflow_details.get('status', 'Completed Successfully')}

**Process Details:**
- Successfully downloaded the TREC Addendum for Sale of Other Property by Buyer form
- Filled out the form with the specified data:
  - Date: 27-08-2025
  - Address: 6/66, Anna Nagar, Chennai, 602105
- Saved the completed form as 'newpdfff.pdf'
- Prepared the document for email transmission

The completed form is attached to this email for your review and records.

This automated process demonstrates the successful integration of web automation, document processing, and email communication systems.

Please let me know if you need any additional information or have any questions regarding this submission.

Best regards,
Automated Workflow System

---
This email was generated automatically by the RPA system.
Execution ID: {datetime.now().strftime('%Y%m%d_%H%M%S')}
"""
            
            attachments = [pdf_path] if pdf_path and os.path.exists(pdf_path) else None
            
            return self.create_email_message(recipient, subject, body, attachments)
            
        except Exception as e:
            self.logger.error(f"Error creating workflow email: {e}")
            return None
    
    def save_email_draft(self, email_msg, file_path):
        """
        Save email message as draft file
        
        Args:
            email_msg: Email message object
            file_path (str): Path to save draft
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"To: {email_msg['To']}\n")
                f.write(f"Subject: {email_msg['Subject']}\n")
                f.write(f"Date: {email_msg['Date']}\n\n")
                
                # Extract body text
                for part in email_msg.walk():
                    if part.get_content_type() == "text/plain":
                        f.write(part.get_payload())
                        break
            
            self.logger.info(f"Email draft saved: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving email draft: {e}")
            return False
    
    def load_email_config(self, config_path):
        """
        Load email configuration from file
        
        Args:
            config_path (str): Path to configuration file
        """
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                self.smtp_server = config.get('smtp_server', self.smtp_server)
                self.smtp_port = config.get('smtp_port', self.smtp_port)
                self.username = config.get('username', self.username)
                self.password = config.get('password', self.password)
                
                self.logger.info("Email configuration loaded successfully")
                return True
            else:
                self.logger.warning(f"Configuration file not found: {config_path}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading email configuration: {e}")
            return False
    
    def save_email_config(self, config_path):
        """
        Save email configuration to file
        
        Args:
            config_path (str): Path to save configuration
        """
        try:
            config = {
                'smtp_server': self.smtp_server,
                'smtp_port': self.smtp_port,
                'username': self.username,
                'password': self.password
            }
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            
            self.logger.info(f"Email configuration saved: {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving email configuration: {e}")
            return False



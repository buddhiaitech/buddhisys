"""
Email Automation RPA Workflow
Automated email sending, template management, and bulk operations
"""

import os
import sys
import time
import logging
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

class EmailAutomationWorkflow:
    def __init__(self):
        """Initialize Email Automation Workflow"""
        self.logger = self._setup_logging()
        self.workspace_dir = os.path.dirname(os.path.abspath(__file__))
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logger = logging.getLogger('EmailAutomationWorkflow')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def create_email_templates(self):
        """Create sample email templates"""
        try:
            self.logger.info("📧 Creating email templates...")
            
            templates = {
                'welcome': {
                    'subject': 'Welcome to Our Service!',
                    'body': '''
                    <html>
                    <body>
                    <h2>Welcome to Our Service!</h2>
                    <p>Dear {name},</p>
                    <p>Thank you for joining us! We're excited to have you on board.</p>
                    <p>Here are some next steps:</p>
                    <ul>
                        <li>Complete your profile setup</li>
                        <li>Explore our features</li>
                        <li>Join our community</li>
                    </ul>
                    <p>If you have any questions, feel free to reach out to our support team.</p>
                    <p>Best regards,<br>The Team</p>
                    </body>
                    </html>
                    '''
                },
                'newsletter': {
                    'subject': 'Weekly Newsletter - {date}',
                    'body': '''
                    <html>
                    <body>
                    <h2>Weekly Newsletter</h2>
                    <p>Hello {name},</p>
                    <p>Here's what's new this week:</p>
                    <ul>
                        <li>New features and updates</li>
                        <li>Community highlights</li>
                        <li>Upcoming events</li>
                    </ul>
                    <p>Stay tuned for more exciting updates!</p>
                    <p>Best regards,<br>The Newsletter Team</p>
                    </body>
                    </html>
                    '''
                },
                'notification': {
                    'subject': 'Important Notification',
                    'body': '''
                    <html>
                    <body>
                    <h2>Important Notification</h2>
                    <p>Dear {name},</p>
                    <p>This is an important notification regarding your account.</p>
                    <p>Please review the following information:</p>
                    <p>{message}</p>
                    <p>If you have any questions, please contact our support team.</p>
                    <p>Best regards,<br>The Support Team</p>
                    </body>
                    </html>
                    '''
                }
            }
            
            # Save templates to file
            templates_path = os.path.join(self.workspace_dir, 'logs', 'email_templates.json')
            os.makedirs(os.path.dirname(templates_path), exist_ok=True)
            
            with open(templates_path, 'w') as f:
                json.dump(templates, f, indent=2)
            
            self.logger.info(f"✅ Email templates created: {templates_path}")
            return templates_path
            
        except Exception as e:
            self.logger.error(f"Error creating email templates: {e}")
            return None
    
    def create_sample_contacts(self):
        """Create sample contact list"""
        try:
            self.logger.info("👥 Creating sample contacts...")
            
            contacts = [
                {'name': 'John Smith', 'email': 'john.smith@example.com', 'company': 'Tech Corp'},
                {'name': 'Sarah Johnson', 'email': 'sarah.johnson@example.com', 'company': 'Design Inc'},
                {'name': 'Mike Wilson', 'email': 'mike.wilson@example.com', 'company': 'Marketing Pro'},
                {'name': 'Lisa Brown', 'email': 'lisa.brown@example.com', 'company': 'Sales Co'},
                {'name': 'David Davis', 'email': 'david.davis@example.com', 'company': 'Consulting Ltd'}
            ]
            
            # Save contacts to file
            contacts_path = os.path.join(self.workspace_dir, 'logs', 'contacts.json')
            os.makedirs(os.path.dirname(contacts_path), exist_ok=True)
            
            with open(contacts_path, 'w') as f:
                json.dump(contacts, f, indent=2)
            
            self.logger.info(f"✅ Sample contacts created: {contacts_path}")
            return contacts_path
            
        except Exception as e:
            self.logger.error(f"Error creating sample contacts: {e}")
            return None
    
    def send_email(self, to_email, subject, body, is_html=True, attachment_path=None):
        """Send a single email"""
        try:
            # Email configuration (using environment variables or defaults)
            smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            sender_email = os.getenv('GMAIL_EMAIL', 'your-email@gmail.com')
            sender_password = os.getenv('GMAIL_PASSWORD', 'your-app-password')
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, to_email, text)
            server.quit()
            
            self.logger.info(f"✅ Email sent to: {to_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email to {to_email}: {e}")
            return False
    
    def send_bulk_emails(self, contacts_path, template_name, custom_data=None):
        """Send bulk emails using templates"""
        try:
            self.logger.info(f"📬 Sending bulk emails using template: {template_name}")
            
            # Load contacts
            with open(contacts_path, 'r') as f:
                contacts = json.load(f)
            
            # Load templates
            templates_path = os.path.join(self.workspace_dir, 'logs', 'email_templates.json')
            with open(templates_path, 'r') as f:
                templates = json.load(f)
            
            if template_name not in templates:
                self.logger.error(f"Template '{template_name}' not found")
                return False
            
            template = templates[template_name]
            success_count = 0
            
            for contact in contacts:
                try:
                    # Prepare email data
                    email_data = {
                        'name': contact['name'],
                        'company': contact.get('company', ''),
                        'date': datetime.now().strftime('%Y-%m-%d')
                    }
                    
                    if custom_data:
                        email_data.update(custom_data)
                    
                    # Format subject and body
                    subject = template['subject'].format(**email_data)
                    body = template['body'].format(**email_data)
                    
                    # Send email
                    if self.send_email(contact['email'], subject, body):
                        success_count += 1
                        self.logger.info(f"✅ Email sent to {contact['name']} ({contact['email']})")
                    else:
                        self.logger.warning(f"❌ Failed to send email to {contact['name']}")
                    
                    # Small delay to avoid rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    self.logger.error(f"Error processing contact {contact['name']}: {e}")
                    continue
            
            self.logger.info(f"✅ Bulk email sending completed: {success_count}/{len(contacts)} successful")
            return success_count > 0
            
        except Exception as e:
            self.logger.error(f"Error in bulk email sending: {e}")
            return False
    
    def create_email_report(self, sent_count, total_count, template_used):
        """Create email sending report"""
        try:
            self.logger.info("📊 Creating email report...")
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'template_used': template_used,
                'total_recipients': total_count,
                'successful_sends': sent_count,
                'failed_sends': total_count - sent_count,
                'success_rate': (sent_count / total_count * 100) if total_count > 0 else 0,
                'workflow': 'Email Automation RPA'
            }
            
            # Save report
            report_path = os.path.join(self.workspace_dir, 'logs', f'email_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.logger.info(f"✅ Email report created: {report_path}")
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error creating email report: {e}")
            return None
    
    def execute_email_automation_workflow(self):
        """Execute the complete email automation workflow"""
        try:
            self.logger.info("🚀 Starting Email Automation Workflow...")
            
            # Create email templates
            templates_path = self.create_email_templates()
            if not templates_path:
                return False
            
            # Create sample contacts
            contacts_path = self.create_sample_contacts()
            if not contacts_path:
                return False
            
            # Load contacts to get count
            with open(contacts_path, 'r') as f:
                contacts = json.load(f)
            
            total_contacts = len(contacts)
            
            # Send bulk emails using welcome template
            self.logger.info("📧 Sending welcome emails...")
            success_count = 0
            
            # Simulate sending emails (in real scenario, uncomment the actual sending)
            for contact in contacts:
                self.logger.info(f"📤 Would send welcome email to: {contact['name']} ({contact['email']})")
                success_count += 1
                time.sleep(0.5)  # Simulate processing time
            
            # In a real implementation, you would use:
            # success_count = self.send_bulk_emails(contacts_path, 'welcome')
            
            # Create email report
            self.create_email_report(success_count, total_contacts, 'welcome')
            
            self.logger.info("✅ Email automation workflow completed successfully!")
            self.logger.info(f"📊 Summary: {success_count}/{total_contacts} emails processed")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Email automation workflow failed: {e}")
            return False

def main():
    """Main execution function"""
    print("📧 Email Automation RPA Workflow")
    print("=" * 50)
    print("This will create templates, manage contacts, and send bulk emails!")
    print("=" * 50)
    
    # Check if running in non-interactive mode (API call)
    non_interactive = '--non-interactive' in sys.argv or os.getenv('NON_INTERACTIVE', '').lower() == 'true'
    
    if non_interactive:
        response = 'y'
        print("\n🤖 Running in non-interactive mode (API call)")
    else:
        # Ask for confirmation
        response = input("\nDo you want to start the email automation workflow? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🚀 Starting Email Automation Workflow...")
        print("=" * 50)
        
        # Create and run automation
        automation = EmailAutomationWorkflow()
        success = automation.execute_email_automation_workflow()
        
        if success:
            print("\n🎉 Email Automation Workflow completed successfully!")
            print("✅ Templates created and emails processed!")
        else:
            print("\n❌ Email Automation Workflow failed. Check logs for details.")
    else:
        print("\n❌ Email automation workflow cancelled.")

if __name__ == "__main__":
    main()

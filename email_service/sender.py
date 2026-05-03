import smtplib
import yaml
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import settings
from loguru import logger

class EmailSender:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.email_user = settings.EMAIL
        self.password = settings.APP_PASSWORD
        self.template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'email_templates.yml')
        
        self.templates = self._load_templates()
        
    def _load_templates(self):
        try:
            with open(self.template_path, 'r') as file:
                templates = yaml.safe_load(file)
                logger.info("Email templates loaded successfully.")
                return templates
        except Exception as e:
            logger.error(f"Failed to load email templates: {e}")
            raise
    
    def send_email(self, to_email: str, template_name: str, **kwargs):
        try:
            if template_name not in self.templates:
                logger.error(f"Template '{template_name}' not found.")
                return
            
            template = self.templates[template_name]
            subject = template['subject']
            body = template['body'].format(**kwargs)
            
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            logger.info(f"Connecting to SMTP server to send email to {to_email}...")
            with smtplib.SMTP_SSL(self.smtp_server, 465) as server:
                server.login(self.email_user, self.password)
                server.send_message(msg)
                logger.info(f"Email sent successfully to {to_email}.")
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
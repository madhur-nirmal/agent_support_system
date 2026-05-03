import imaplib
import email
from email.header import decode_header
from config import settings
from typing import List, Dict
from loguru import logger


class EmailReader:
    # Constructor
    def __init__(self):
        self.imap_server = settings.IMAP_SERVER
        self.email_user = settings.EMAIL
        self.password = settings.APP_PASSWORD

    # Function to establish gmail provider inbox connection through imap protocol using Secure Socket Layer (SSL)
    def connect(self):
        try:
            logger.info("Connnecting to IMAP server...")

            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email_user, self.password)

            logger.info("IMAP connection established successfully.")

            return mail
        except Exception as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            raise

    # Read Unseen/emails which are not marked as read
    def fetch_unseen_emails(self) -> List[Dict]:
        emails = []

        try:
            mail = self.connect()
            mail.select("inbox")

            logger.info("Fetching unseen emails...")
            status, messages = mail.search(None, "(UNSEEN)")
            email_ids = messages[0].split()
            logger.info(f"Found {len(email_ids)} unseen emails")

            for e_id in email_ids:
                print(e_id)
                parsed = self._fetch_single_email(mail, e_id)

                if parsed:
                    emails.append(parsed)

        except Exception as e:
            logger.error(f"Error while fetching emails: {e}")

        return emails

    # Retrieve and parse a single email by email id
    def _fetch_single_email(self, mail, e_id) -> Dict:
        try:
            status, msg_data = mail.fetch(e_id, "(RFC822)")

            raw_email = msg_data[0][1]
            parsed_email = email.message_from_bytes(raw_email)
            sender = email.utils.parseaddr(parsed_email.get("From"))[1]
            subject = self._decode_subject(parsed_email.get("Subject") or "")
            body = self._extract_body(parsed_email)

            logger.info(f"Processed email from : {sender}")

            return {"sender": sender, "subject": subject, "body": body}

        except Exception as e:
            logger.error(f"Error parsing email Id {e_id}: {e}")
            return {}

    # Decode email subject (handles encoded headers)
    def _decode_subject(self, subject: str) -> str:
        if not subject:
            return ""

        decoded, encoding = decode_header(subject)[0]

        if isinstance(decoded, bytes):
            return decoded.decode(encoding or "utf-8", errors="ignore")

        return decoded

    # Extract plain text body from email.
    def _extract_body(self, msg) -> str:
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()

                    # Extract only plain text
                    if content_type == "text/plain":
                        return part.get_payload(decode=True).decode(errors="ignore")
            else:
                return msg.get_payload(decode=True).decode(errors="ignore")

        except Exception as e:
            logger.error(f"Error extracting email body: {e}")

        return ""

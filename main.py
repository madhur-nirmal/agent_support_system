import os
from config import settings
from email_service.reader import EmailReader


def main():
    # Initialize EmailReader
    email_reader = EmailReader()

    # Fetch unseen emails
    unseen_emails = email_reader.fetch_unseen_emails()

    # Print the fetched emails
    for idx, email in enumerate(unseen_emails, start=1):
        print(f"Email {idx}:")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Body: {email['body']}\n")


if __name__ == "__main__":
    main()

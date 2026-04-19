import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EMAIL = os.getenv("EMAIL") or ""
APP_PASSWORD = os.getenv("APP_PASSWORD") or ""
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
POSTGRESQL_CONNECTION = os.getenv("POSTGRESQL_CONNECTION") or ""
ALLOWED_DOMAINS = os.getenv("ALLOWED_DOMAINS", "gmail.com").split(",")
ENV = os.getenv("ENV", "dev")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

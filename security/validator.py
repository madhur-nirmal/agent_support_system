from typing import Dict
from loguru import logger
from config import settings

def validate_sender(email: str) -> Dict:
  try:
    if not email or "@" not in email:
      return {"valid": False, "reason": "invalid_format"}
    
    local, domain = email.split("@")
    if domain not in settings.ALLOWED_DOMAINS:
      logger.warning(f"Email blocked: domain {domain} not allowed")
      return {"valid": False, "reason": "domain_not_allowed"}
    
    return {"valid": True, "reason": "ok"}
  except Exception as e:
    logger.error(f"Error validating sender: {e}")
    return {"valid": False, "reason": "exception"}
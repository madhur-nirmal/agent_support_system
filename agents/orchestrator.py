
from typing import Dict
from loguru import logger
from email_service.reader import EmailReader
from security.validator import validate_sender
from security.spam_filter import is_spam as detect_spam
from security.guardrails import Guardrails
from nlp.intent_classifier import IntentClassifier
from nlp.sentiment import SentimentAnalyzer
from nlp.entity_extractor import EntityExtractor
from nlp.language_detector import detect_language

# Core system controller
# - Fetch emails
# - Apply security checks
# - Rum NLP pipeline
class Orchestrator:
  def __init__(self):
    self.reader = EmailReader()
    self.guardrails = Guardrails()
    self.intent_model = IntentClassifier()
    self.sentiment_model = SentimentAnalyzer()
    self.entity_model = EntityExtractor()

  # Main Entry Point
  # - Fetch emails
  # - Process each email
  def process_emails(self):
    logger.info("Starting email processing pipeline")
    emails = self.reader.fetch_unseen_emails()
    results = []

    for email_data in emails:
      result = self._process_single_email(email_data)

      if result:
        results.append(result)

    return results

  # Process single email end to end
  def _process_single_email(self, email_data: Dict) -> Dict:
    try:
      sender = email_data.get("sender")
      subject = email_data.get("subject", "")
      body = email_data.get("body", "")

      logger.info(f"Processing email from : {sender}")

      # Step 1: Sender Validation
      sender_check = validate_sender(sender)

      if not sender_check["valid"]:
        logger.warning("Email blocked: invalid sender")
        return {}

      # Step 2: Spam Detection
      spam_check = detect_spam(body)

      if spam_check["spam"]:
        logger.warning("Email blocked: spam detected")
        return {}

      # Step 3: Guardrails (LLM Safety)
      guardrail_result = self.guardrails.analyze(body)

      if not guardrail_result["safe"]:
        logger.warning("Email blocked: guardrail violation")
        return {}

      clean_text = guardrail_result["sanitized_text"]

      # Step 4: NLP Processing
      intent = self.intent_model.predict(clean_text)
      sentiment = self.sentiment_model.analyze(clean_text)
      entities = self.entity_model.extract(clean_text)
      language = detect_language(clean_text)

      # Step 5: Aggregate result
      result = {
          "sender": sender,
          "subject": subject,
          "body": body,
          "intent": intent,
          "sentiment": sentiment,
          "entities": entities,
          "language": language
      }

      logger.info("Email processed successfully")

      return result

    except Exception as e:
      logger.error(f"Error processing email: {e}")
      return {}
from loguru import logger
from typing import Dict
import re
from google import genai
from config import settings

class Guardrails:
  def __init__(self):
    self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)

  # Main guardrail pipeline
  # - prompt injection detection
  # - malicious intent detection
  # - PII masking
  def analyze(self, text: str) -> Dict:
    try:
      llm_flag = self._llm_check(text)
      regex_flag = self._regex_check(text)

      safe = not (llm_flag or regex_flag)

      return {
          "safe": safe,
          "sanitized_text": self._sanitize(text)
      }

    except Exception as e:
      logger.error(f"Guardrail error: {e}")
      return {"safe": False, "sanitized_text": text}

  # LLM-based detection
  def _llm_check(self, text: str) -> bool:
    try:
      prompt = f"""
      Classify this text as:
      safe / prompt_injection / malicious

      Text:
      {text}
      """

      response = self.client.models.generate_content(
          model = settings.LLM_MODEL,
          contents = prompt
      )

      output = response.text.lower().strip()

      if "prompt_injection" in output or "malicious" in output:
        return True

      return False

    except Exception as e:
      logger.error(f"LLM guardrail error: {e}")
      return False

  # Secondary deterministic layer
  def _regex_check(self, text: str) -> bool:
    patterns = [
        r"ignore\s+previous\s+instructions",
        r"act\s+as\s+.*",
        r"bypass\s+.*",
        r"override\s+.*"
    ]

    for p in patterns:
      if re.search(p, text.lower()):
        return True

    return False

  # PII Masking
  def _sanitize(self, text: str) -> str:
    text = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+\b", "[EMAIL]", text)
    text = re.sub(r"\b\d{10}\b","[PHONE]", text)
    return text.strip()
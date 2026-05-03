from typing import Dict
import spacy
from loguru import logger
from config import model_config

# Extract named entities using spaCy.
class EntityExtractor:
  def __init__(self):
    # Load spaCy model
    self.nlp = spacy.load(model_config.SPACY_MODEL)

  # Extract entities from text
  def extract(self, text: str) -> Dict:
    try:
      doc = self.nlp(text)
      entities = []

      # Iterate over detected entities
      for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

      return {"entities": entities}

    except Exception as e:
      logger.error(f"Entity extraction error : {e}")
      return {"entities": []}
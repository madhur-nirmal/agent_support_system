from loguru import logger
from typing import Dict
from transformers import pipeline
from functools import lru_cache

@lru_cache()
def load_spam_model():
    return pipeline("text-classification", model="distilbert-base-uncased")

def detect_spam(text: str) -> Dict:
    try:
        if not text:
            return {"spam" : False}
        model = load_spam_model()
        result = model(text[:512])[0]  # Truncate to 512 tokens
        label = result['label'].lower()
        score = result['score']
        
        suspicious = any(word in text.lower() for word in ["free", "urgent", "win", "prize", "click here"])
        
        is_spam = label != 'positive' or score < 0.5 or suspicious
        
        return {"spam": is_spam}
    except Exception as e:
        logger.error(f"Error in spam detection: {e}")
        return {"spam": False}
        
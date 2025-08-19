import re
import spacy
from spacy.matcher import PhraseMatcher


def normalize(text):
    text = text.lower() # lowercase everything
    # strip out link syntax [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # remove Markdown headers (##, ###, …), bullets (-, *) and code backticks
    text = re.sub(r"^#{1,6}\s*|^[-*]\s+|`+", "", text, flags=re.MULTILINE)
    # collapse any other punctuation to spaces
    text = re.sub(r"[^\w\s]", " ", text)
    return text


import json

def load_keywords_from_config(config_path="config.json"):
    """Loads required and optional keywords from a JSON config file."""
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    required = [kw.lower() for kw in config["required_keywords"]]
    optional = [kw.lower() for kw in config["optional_keywords"]]
    
    return required, optional



def calculate_score(clean_text: str, required_keywords: list[str], optional_keywords: list[str]):
    """Calculates a score based on keywords found in the text."""
    score = 0
    found_terms = set()

    # Score required keywords
    for term in required_keywords:
        if term in clean_text:
            score += 1
            found_terms.add(term)

    # Score optional keywords
    for term in optional_keywords:
        if term in clean_text:
            score += 0.5
            found_terms.add(term)
            
    return score, found_terms
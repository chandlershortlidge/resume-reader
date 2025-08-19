import re
import json
import spacy
from spacy.matcher import PhraseMatcher
import sys

# It's more efficient to load the model once
nlp = None


def _get_nlp_model():
    """Loads the spaCy model, raising an error if it's not downloaded."""
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            python_executable = sys.executable
            # This is a user-facing script, so it's better to guide them.
            # The main app.py can catch this and display a nice error.
            raise OSError(
                f"spaCy model 'en_core_web_sm' not found.\n\n"
                f"The app is running with this Python interpreter:\n{python_executable}\n\n"
                f"Please make sure you run 'python -m spacy download en_core_web_sm' in the "
                "same activated virtual environment and restart the app."
            )
    return nlp


def normalize(text: str) -> str:
    """
    Minimal text cleaning. Most of the work will be done by spaCy.
    This function removes markdown artifacts that can interfere with parsing.
    """
    # strip out link syntax [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # remove Markdown headers (##, ###, …), bullets (-, *) and code backticks
    text = re.sub(r"^#{1,6}\s*|^[-*]\s+|`+", "", text, flags=re.MULTILINE)
    return text


def load_keywords_from_config(config_path="config.json"):
    """Loads required and optional keywords from a JSON config file."""
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Keep original casing for display, but we'll lowercase for matching.
    required = config.get("required_keywords", [])
    optional = config.get("optional_keywords", [])

    return required, optional


def calculate_score(clean_text: str, required_keywords: list[str], optional_keywords: list[str]):
    """
    Calculates a score based on keywords found in the text using spaCy's PhraseMatcher
    for more robust, multi-word matching.
    """
    nlp = _get_nlp_model()
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

    # Create sets of lowercased keywords for efficient lookup
    required_lower = {kw.lower() for kw in required_keywords}
    optional_lower = {kw.lower() for kw in optional_keywords}
    all_keywords = required_keywords + optional_keywords

    # Add patterns to the matcher. nlp.pipe is more efficient for many texts.
    patterns = [nlp.make_doc(text) for text in all_keywords]
    matcher.add("KeywordList", patterns)

    doc = nlp(clean_text)
    matches = matcher(doc)

    score = 0
    found_terms_lower = set()

    for match_id, start, end in matches:
        span = doc[start:end]
        # The text of the matched span, lowercased for comparison
        matched_text_lower = span.text.lower()

        # Avoid double counting
        if matched_text_lower in found_terms_lower:
            continue

        found_terms_lower.add(matched_text_lower)

        if matched_text_lower in required_lower:
            score += 1
        elif matched_text_lower in optional_lower:
            score += 0.5

    # Map the found lowercased terms back to their original casing for display
    all_keywords_map = {kw.lower(): kw for kw in all_keywords}
    found_terms_original_case = {all_keywords_map[term] for term in found_terms_lower}

    return score, found_terms_original_case
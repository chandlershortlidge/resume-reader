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
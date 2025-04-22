import re
import string
from difflib import SequenceMatcher
from semantic_kernel.memory.memory_query_result import MemoryQueryResult

# ----------------------------
# Step 1: Fuzzy JIRA Matching Utilities
# ----------------------------

def clean_user_query(text):
    # Normalize casing and spacing/punctuation
    text = text.upper()
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    text = re.sub(r'\s+', '-', text)  # replace whitespace with hyphen
    return text

def find_fuzzy_jira_id(user_query, known_prefixes, max_distance=2):
    cleaned_query = clean_user_query(user_query)
    candidates = re.findall(r'[A-Z]+-?\d+', cleaned_query)

    for candidate in candidates:
        if '-' in candidate:
            prefix, number = candidate.split('-')
        else:
            match = re.match(r"([A-Z]+)(\d+)", candidate)
            if not match:
                continue
            prefix, number = match.groups()

        for known_prefix in known_prefixes:
            ratio = SequenceMatcher(None, prefix, known_prefix).ratio()
            edit_distance = (1 - ratio) * max(len(prefix), len(known_prefix))
            if edit_distance <= max_distance:
                return f"{known_prefix}-{number}"

    return None

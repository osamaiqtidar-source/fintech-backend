import json, os
from functools import lru_cache

TRANSLATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations')

@lru_cache(maxsize=16)
def _load_language(lang: str):
    path = os.path.join(TRANSLATIONS_DIR, f"{lang}.json")
    if not os.path.exists(path):
        path = os.path.join(TRANSLATIONS_DIR, 'en.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def translate(key: str, lang: str = 'en') -> str:
    data = _load_language(lang)
    return data.get(key, key)

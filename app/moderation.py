import re
import unicodedata

DEFAULT_ALLOWED_WORDS = [
    "natal", "amor", "paz", "família", "esperança", "união", "alegria",
    "gratidão", "solidariedade", "amizade", "felicidade", "respeito",
    "generosidade", "luz", "harmonia", "celebração", "bondade", "confraternização"
]

DEFAULT_BLOCKED_WORDS = ["palavrão", "otario", "idiota", "droga", "violencia", "porra", "caralho", "merda"]

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize('NFD', text.strip().lower())
    text = "".join([c for c in text if unicodedata.category(c) != 'Mn'])
    text = re.sub(r'[^a-z0-9]', '', text)
    return text

def validate_word_format(raw_word: str) -> tuple[bool, str]:
    raw_word = raw_word.strip()
    if not raw_word:
        return False, "Por favor, digite uma palavra."
    if len(raw_word) > 25:
        return False, "A palavra deve ter no máximo 25 caracteres."
    if len(raw_word) < 2:
        return False, "A palavra deve ter no mínimo 2 caracteres."
    if " " in raw_word:
        return False, "Envie apenas uma palavra por vez (sem espaços)."
    if re.search(r'(http|https|www|\.com|\.br|<|>|script|select|insert|delete)', raw_word, re.IGNORECASE):
        return False, "Formato de texto inválido."
    return True, "" 
import hashlib


def hashed(text):
    txt = text.encode("utf-8")
    return hashlib.sha256(txt).hexdigest()


def hash_match(text, hash_value):
    hashed_text = hashed(text)
    if hashed_text == hash_value:
        return True
    return False

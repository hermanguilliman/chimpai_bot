import hashlib


def split_text(text: str, chunk_size: int = 4000) -> list:
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks


def get_short_id(full_id: str) -> str:
    # Генерируем короткий хеш из полного id
    return hashlib.md5(full_id.encode()).hexdigest()[:10]

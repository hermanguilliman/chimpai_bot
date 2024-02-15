def split_text(text:str, chunk_size:int=4000) -> list:
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks



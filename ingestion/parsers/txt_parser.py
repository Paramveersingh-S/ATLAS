def parse_txt(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    return {"text": text, "metadata": {"page_count": 1}}

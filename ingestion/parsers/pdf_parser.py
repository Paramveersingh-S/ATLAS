import fitz

def parse_pdf(file_path: str) -> dict:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    return {
        "text": text,
        "metadata": {
            "title": doc.metadata.get("title", ""),
            "author": doc.metadata.get("author", ""),
            "page_count": doc.page_count
        }
    }

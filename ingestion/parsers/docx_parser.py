import docx

def parse_docx(file_path: str) -> dict:
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return {
        "text": text,
        "metadata": {
            "title": doc.core_properties.title,
            "author": doc.core_properties.author,
            "page_count": 1
        }
    }

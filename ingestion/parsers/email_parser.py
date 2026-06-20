import email

def parse_email(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f)
    
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                text += part.get_payload()
    else:
        text = msg.get_payload()
        
    return {
        "text": text,
        "metadata": {
            "subject": msg["subject"],
            "from": msg["from"],
            "page_count": 1
        }
    }
